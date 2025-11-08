from sqlalchemy import update, delete
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import Role
from app.models.order import Order
from sqlalchemy.future import select
from app.models.product import Product
from app.models.cart_item import CartItem
from app.models.order_item import OrderItem
from app.services.order_service import OrderService
from app.services.email_service import EmailService
from app.utils.distributed_lock import DistributedLock


class OrderItemService:
  async def create_order_item(db: AsyncSession, current_user):
    result = await db.execute(
      select(CartItem, Product)
      .join(Product, CartItem.product_id == Product.id)
      .filter(CartItem.user_id == current_user.id))

    cart_items = result.all()

    if not cart_items:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is empty")

    # 使用分布式锁保护整个订单创建过程，防止并发问题
    lock_key = f"order:create:{current_user.id}"
    lock = DistributedLock(lock_key, timeout=30, retry_times=5, retry_delay=0.2)
    
    if not await lock.acquire():
      raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Another order is being processed. Please try again later.")
    
    try:
      # 重新查询购物车和商品，确保获取最新数据
      result = await db.execute(
        select(CartItem, Product)
        .join(Product, CartItem.product_id == Product.id)
        .filter(CartItem.user_id == current_user.id))
      
      cart_items = result.all()
      
      if not cart_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is empty")

      order = await OrderService.create_order(db, current_user)

      # 为每个商品获取分布式锁，保护库存扣减
      for cart_item, product in cart_items:
        product_lock_key = f"product:stock:{product.id}"
        product_lock = DistributedLock(product_lock_key, timeout=10, retry_times=3, retry_delay=0.1)
        
        if not await product_lock.acquire():
          raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Product {product.id} is being processed. Please try again later.")
        
        try:
          # 重新查询商品库存，确保获取最新数据
          product_query = await db.execute(
            select(Product).where(Product.id == product.id)
          )
          current_product = product_query.scalars().first()
          
          if not current_product:
            raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail=f"Product {product.id} not found")
          
          if current_product.stock < cart_item.quantity:
            raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST,
              detail=f"Insufficient stock for product {product.id}. Available: {current_product.stock}, Requested: {cart_item.quantity}")

          new_stock = current_product.stock - cart_item.quantity
          is_active = False if new_stock == 0 else current_product.is_active

          await db.execute(
            update(Product)
            .where(Product.id == current_product.id)
            .values(stock=new_stock, is_active=is_active))
        finally:
          await product_lock.release()

      order_items = [
        OrderItem(
          order_id=order.id,
          product_id=cart_item.product_id,
          quantity=cart_item.quantity,
          price=cart_item.price)

        for cart_item, _ in cart_items
      ]
      db.add_all(order_items)

      await db.execute(delete(CartItem).where(CartItem.user_id == current_user.id))

      try:
        await db.commit()
      except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Database error")

      # 使用Celery异步发送邮件
      try:
        from app.tasks.email_tasks import send_order_placement_email
        send_order_placement_email.delay(current_user.email)
      except Exception:
        # 如果Celery不可用，同步发送（降级处理）
        await EmailService.order_placement_message(current_user.email)
      
      return order_items
    finally:
      await lock.release()

  @staticmethod
  async def get_order_item_by_id(db: AsyncSession, order_item_id: int, current_user):
    query = select(OrderItem).where(OrderItem.id == order_item_id)
    result = await db.execute(query)
    order_item = result.scalars().first()

    if not order_item:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Order item not found.")

    query = select(Order).where(Order.id == order_item.order_id)
    result = await db.execute(query)
    order = result.scalars().first()

    admin = current_user.role == Role.admin

    if order.user_id == current_user.id or admin:
      return order_item

    else:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this order item.")