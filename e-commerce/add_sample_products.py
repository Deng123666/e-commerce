"""
快速添加示例商品数据
运行方式：python add_sample_products.py
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.models.product import Product, CategoryEnum
from app.models.user import User
from app.schemas.user import Role


async def get_first_vendor_or_admin():
    """获取第一个商家或管理员用户ID"""
    async with AsyncSessionLocal() as db:
        # 先查找商家
        result = await db.execute(
            select(User).where(User.role == Role.vendor).limit(1)
        )
        vendor = result.scalar_one_or_none()
        
        if vendor:
            return vendor.id
        
        # 如果没有商家，查找管理员
        result = await db.execute(
            select(User).where(User.role == Role.admin).limit(1)
        )
        admin = result.scalar_one_or_none()
        
        if admin:
            return admin.id
        
        # 如果都没有，返回第一个用户
        result = await db.execute(select(User).limit(1))
        first_user = result.scalar_one_or_none()
        
        if first_user:
            return first_user.id
        
        return None


async def add_sample_products():
    """添加示例商品"""
    
    # 获取vendor_id
    vendor_id = await get_first_vendor_or_admin()
    
    if not vendor_id:
        print("❌ 错误：数据库中没有用户！")
        print("请先注册一个用户（建议选择'商家'角色）")
        return
    
    print(f"✅ 使用用户ID: {vendor_id} 作为商品供应商")
    
    async with AsyncSessionLocal() as db:
        # 检查是否已有商品
        result = await db.execute(select(Product))
        existing = result.scalars().all()
        
        if existing:
            print(f"⚠️  警告：数据库中已有 {len(existing)} 个商品")
            response = input("是否继续添加？(y/n): ")
            if response.lower() != 'y':
                print("取消添加")
                return
        
        products = [
            # 电子产品
            Product(
                name="iPhone 15 Pro Max",
                description="全新一代iPhone，配备A17 Pro芯片，钛金属设计，超强性能。6.7英寸超视网膜XDR显示屏，支持120Hz自适应刷新率。",
                price=9999.00,
                stock=50,
                category=CategoryEnum.electronics,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1592286927505-4ffd2560e4c8?w=400"
            ),
            Product(
                name="MacBook Pro 16英寸",
                description="M3 Max芯片，18GB统一内存，512GB SSD存储。专业级性能，适合开发和设计工作。",
                price=18999.00,
                stock=30,
                category=CategoryEnum.electronics,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400"
            ),
            Product(
                name="Sony WH-1000XM5 降噪耳机",
                description="顶级降噪效果，30小时续航，支持LDAC高清音频。自适应声音控制，多点连接。",
                price=2499.00,
                stock=80,
                category=CategoryEnum.electronics,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"
            ),
            Product(
                name="iPad Pro 12.9英寸",
                description="M2芯片，Liquid Retina XDR显示屏，支持Apple Pencil 2。",
                price=7999.00,
                stock=40,
                category=CategoryEnum.electronics,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400"
            ),
            Product(
                name="Samsung Galaxy S24 Ultra",
                description="200MP主摄，骁龙8 Gen 3处理器，5000mAh大电池。",
                price=8999.00,
                stock=35,
                category=CategoryEnum.electronics,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400"
            ),
            
            # 时尚服饰
            Product(
                name="Nike Air Jordan 1 运动鞋",
                description="经典复刻款，黑红配色，限量发售。优质皮革材质，舒适耐穿。",
                price=1299.00,
                stock=30,
                category=CategoryEnum.fashion,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"
            ),
            Product(
                name="Adidas Ultraboost 22",
                description="能量回弹中底，轻质透气鞋面。适合跑步和日常穿着。",
                price=899.00,
                stock=60,
                category=CategoryEnum.fashion,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400"
            ),
            Product(
                name="Levi's 501 经典牛仔裤",
                description="经典直筒版型，100%纯棉面料，永不过时的款式。",
                price=599.00,
                stock=100,
                category=CategoryEnum.fashion,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1542272604-787c3835535d?w=400"
            ),
            Product(
                name="The North Face 冲锋衣",
                description="防水透气，三合一设计，适合户外探险。",
                price=1599.00,
                stock=45,
                category=CategoryEnum.fashion,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400"
            ),
            Product(
                name="Converse 经典帆布鞋",
                description="经典百搭款，多色可选，舒适轻便。",
                price=399.00,
                stock=120,
                category=CategoryEnum.fashion,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1515955656352-a1fa3ffcd111?w=400"
            ),
            
            # 家居用品
            Product(
                name="北欧简约沙发",
                description="现代简约风格，舒适透气，适合客厅使用。优质面料，结实耐用。",
                price=3599.00,
                stock=15,
                category=CategoryEnum.home,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400"
            ),
            Product(
                name="智能护眼台灯",
                description="护眼LED，无线充电，触摸调光。支持色温调节，自动感光。",
                price=299.00,
                stock=100,
                category=CategoryEnum.home,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400"
            ),
            Product(
                name="宜家办公椅",
                description="人体工学设计，可调节高度和角度，久坐不累。",
                price=899.00,
                stock=50,
                category=CategoryEnum.home,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=400"
            ),
            Product(
                name="北欧风餐桌",
                description="实木材质，简约设计，可容纳4-6人。",
                price=2199.00,
                stock=20,
                category=CategoryEnum.home,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1617806118233-18e1de247200?w=400"
            ),
            Product(
                name="智能扫地机器人",
                description="激光导航，自动规划路径，支持拖地功能。",
                price=1999.00,
                stock=35,
                category=CategoryEnum.home,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400"
            ),
            
            # 图书音像
            Product(
                name="Vue.js设计与实现",
                description="深入理解Vue3响应式原理，掌握组件化开发。霍春阳（HcySunYang）著。",
                price=89.00,
                stock=100,
                category=CategoryEnum.books,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400"
            ),
            Product(
                name="Python编程：从入门到实践",
                description="Python基础教程，适合初学者。包含大量实例和项目。",
                price=79.00,
                stock=150,
                category=CategoryEnum.books,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1589998059171-988d887df646?w=400"
            ),
            Product(
                name="深入理解计算机系统",
                description="CSAPP经典教材，计算机专业必读。",
                price=139.00,
                stock=80,
                category=CategoryEnum.books,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400"
            ),
            Product(
                name="算法导论",
                description="算法领域的经典教材，麻省理工学院出版。",
                price=128.00,
                stock=60,
                category=CategoryEnum.books,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400"
            ),
            Product(
                name="JavaScript高级程序设计",
                description="红宝书第4版，全面讲解JavaScript核心技术。",
                price=99.00,
                stock=90,
                category=CategoryEnum.books,
                vendor_id=vendor_id,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400"
            ),
        ]
        
        print(f"\n开始添加 {len(products)} 个商品...")
        
        for i, product in enumerate(products, 1):
            db.add(product)
            print(f"  [{i}/{len(products)}] {product.name} - ¥{product.price}")
        
        await db.commit()
        print(f"\n✅ 成功添加 {len(products)} 个商品！")
        print("\n📝 商品统计:")
        print(f"  - 电子产品: {sum(1 for p in products if p.category == CategoryEnum.electronics)} 个")
        print(f"  - 时尚服饰: {sum(1 for p in products if p.category == CategoryEnum.fashion)} 个")
        print(f"  - 家居用品: {sum(1 for p in products if p.category == CategoryEnum.home)} 个")
        print(f"  - 图书音像: {sum(1 for p in products if p.category == CategoryEnum.books)} 个")
        print("\n🎉 现在可以访问前端查看商品列表了！")
        print("   前端地址: http://localhost:3000/products")


if __name__ == "__main__":
    print("="*60)
    print("          快速添加示例商品数据")
    print("="*60)
    asyncio.run(add_sample_products())

