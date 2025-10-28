# 📦 添加商品数据指南

商品列表页已经实现完成！现在需要添加一些商品数据才能看到效果。

---

## 🎯 方法一：使用Swagger UI添加（推荐）

### 步骤：

1. **确保后端正在运行**
   ```bash
   cd e-commerce
   uvicorn app.main:app --reload --port 8000
   ```

2. **打开Swagger UI**
   
   访问：http://localhost:8000/docs

3. **登录获取Token**

   a. 先注册一个商家账户（如果还没有）
   - 在前端注册时选择"商家"角色
   - 或在Swagger中使用 `POST /auth/register`
   
   b. 登录获取Token
   - 找到 `POST /auth/login`
   - 点击 "Try it out"
   - 输入：
     ```json
     {
       "email": "vendor@example.com",
       "password": "Vendor@123456"
     }
     ```
   - 点击 Execute
   - 复制返回的 `accessToken`

4. **设置Authorization**

   - 点击页面右上角的 "Authorize" 按钮
   - 在弹出框中输入：`Bearer <你的accessToken>`
   - 点击 Authorize

5. **创建商品**

   - 找到 `POST /products/`
   - 点击 "Try it out"
   - 输入商品数据（示例）：

   **电子产品示例**：
   ```json
   {
     "name": "iPhone 15 Pro Max",
     "description": "全新一代iPhone，配备A17 Pro芯片，钛金属设计，超强性能",
     "price": 9999,
     "stock": 50,
     "category": "electronics",
     "image_url": "https://images.unsplash.com/photo-1592286927505-4ffd2560e4c8?w=400"
   }
   ```

   **时尚服饰示例**：
   ```json
   {
     "name": "Nike Air Jordan 1 运动鞋",
     "description": "经典复刻款，黑红配色，限量发售",
     "price": 1299,
     "stock": 30,
     "category": "fashion",
     "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"
   }
   ```

   **家居用品示例**：
   ```json
   {
     "name": "北欧简约沙发",
     "description": "现代简约风格，舒适透气，适合客厅使用",
     "price": 3599,
     "stock": 15,
     "category": "home",
     "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400"
   }
   ```

   **图书音像示例**：
   ```json
   {
     "name": "Vue.js设计与实现",
     "description": "深入理解Vue3响应式原理，掌握组件化开发",
     "price": 89,
     "stock": 100,
     "category": "books",
     "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400"
   }
   ```

6. **点击 Execute 创建商品**

7. **重复步骤5-6**，多创建几个商品

---

## 🎯 方法二：使用Python脚本批量添加

创建文件 `e-commerce/add_sample_products.py`：

```python
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import AsyncSessionLocal
from app.models.product import Product, CategoryEnum

async def add_sample_products():
    async with AsyncSessionLocal() as db:
        products = [
            # 电子产品
            Product(
                name="iPhone 15 Pro Max",
                description="全新一代iPhone，配备A17 Pro芯片，钛金属设计，超强性能",
                price=9999.00,
                stock=50,
                category=CategoryEnum.electronics,
                vendor_id=1,  # 需要改成你的用户ID
                is_active=True,
                image_url="https://images.unsplash.com/photo-1592286927505-4ffd2560e4c8?w=400"
            ),
            Product(
                name="MacBook Pro 16寸",
                description="M3 Max芯片，18GB内存，512GB存储，专业级性能",
                price=18999.00,
                stock=30,
                category=CategoryEnum.electronics,
                vendor_id=1,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400"
            ),
            Product(
                name="Sony WH-1000XM5 降噪耳机",
                description="顶级降噪效果，30小时续航，支持LDAC高清音频",
                price=2499.00,
                stock=80,
                category=CategoryEnum.electronics,
                vendor_id=1,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"
            ),
            
            # 时尚服饰
            Product(
                name="Nike Air Jordan 1 运动鞋",
                description="经典复刻款，黑红配色，限量发售",
                price=1299.00,
                stock=30,
                category=CategoryEnum.fashion,
                vendor_id=1,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"
            ),
            Product(
                name="Adidas Ultraboost 22",
                description="能量回弹中底，轻质透气鞋面",
                price=899.00,
                stock=60,
                category=CategoryEnum.fashion,
                vendor_id=1,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400"
            ),
            
            # 家居用品
            Product(
                name="北欧简约沙发",
                description="现代简约风格，舒适透气，适合客厅使用",
                price=3599.00,
                stock=15,
                category=CategoryEnum.home,
                vendor_id=1,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400"
            ),
            Product(
                name="智能台灯",
                description="护眼LED，无线充电，触摸调光",
                price=299.00,
                stock=100,
                category=CategoryEnum.home,
                vendor_id=1,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400"
            ),
            
            # 图书音像
            Product(
                name="Vue.js设计与实现",
                description="深入理解Vue3响应式原理，掌握组件化开发",
                price=89.00,
                stock=100,
                category=CategoryEnum.books,
                vendor_id=1,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400"
            ),
            Product(
                name="Python编程：从入门到实践",
                description="Python基础教程，适合初学者",
                price=79.00,
                stock=150,
                category=CategoryEnum.books,
                vendor_id=1,
                is_active=True,
                image_url="https://images.unsplash.com/photo-1589998059171-988d887df646?w=400"
            ),
        ]
        
        for product in products:
            db.add(product)
        
        await db.commit()
        print(f"成功添加 {len(products)} 个商品！")

if __name__ == "__main__":
    asyncio.run(add_sample_products())
```

**注意**：将 `vendor_id=1` 改成你的用户ID（在数据库中查询或使用你注册的用户ID）。

**运行脚本**：
```bash
cd e-commerce
source venv/bin/activate  # Windows: venv\Scripts\activate
python add_sample_products.py
```

---

## 🎯 方法三：直接在数据库中添加

```sql
-- 连接到数据库
psql -U postgres -d ecommerce_db

-- 查看你的用户ID
SELECT id, email, role FROM users;

-- 插入商品（替换 vendor_id 为你的用户ID）
INSERT INTO products (name, description, price, stock, category, vendor_id, is_active, image_url, view_count, created_at, updated_at)
VALUES 
('iPhone 15 Pro Max', '全新一代iPhone，配备A17 Pro芯片', 9999.00, 50, 'electronics', 1, true, 'https://images.unsplash.com/photo-1592286927505-4ffd2560e4c8?w=400', 0, NOW(), NOW()),
('Nike Air Jordan 1', '经典复刻款运动鞋', 1299.00, 30, 'fashion', 1, true, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400', 0, NOW(), NOW()),
('北欧简约沙发', '现代简约风格沙发', 3599.00, 15, 'home', 1, true, 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400', 0, NOW(), NOW()),
('Vue.js设计与实现', 'Vue3深度解析', 89.00, 100, 'books', 1, true, 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400', 0, NOW(), NOW());

-- 查看添加的商品
SELECT id, name, price, category FROM products;
```

---

## ✅ 验证商品数据

### 1. 在Swagger UI中查看

访问 http://localhost:8000/docs
- 找到 `GET /products/`
- 点击 "Try it out"
- 点击 "Execute"
- 查看返回的商品列表

### 2. 在前端查看

访问 http://localhost:3000/products

如果一切正常，你应该能看到：
- ✅ 左侧分类导航
- ✅ 顶部搜索框
- ✅ 商品卡片网格
- ✅ 商品图片、名称、价格、库存
- ✅ 分页控件

---

## 🎨 图片资源说明

示例中使用了 Unsplash 的图片链接作为商品图片。这些是真实的图片URL，可以正常显示。

你也可以：
1. 使用其他图片URL
2. 上传图片到图床（如阿里云OSS、腾讯云COS）
3. 暂时留空，会显示占位图

---

## 🔍 功能测试清单

添加商品后，测试以下功能：

- [ ] 查看全部商品
- [ ] 点击分类筛选
- [ ] 搜索商品名称
- [ ] 价格区间筛选
- [ ] 库存状态筛选
- [ ] 排序（价格、时间）
- [ ] 分页功能
- [ ] 点击商品查看详情
- [ ] 添加到购物车（需先登录）

---

## 💡 提示

1. **用户角色**：只有"商家"或"管理员"角色可以创建商品
2. **邮箱验证**：确保用户已验证邮箱才能登录
3. **图片URL**：确保图片URL可访问，否则会显示占位图
4. **库存管理**：`stock > 0` 时 `is_active` 自动设为 `true`

---

## 🎉 完成！

添加商品后，刷新前端页面 http://localhost:3000/products 即可看到效果！

如有问题，请检查：
- 后端是否正常运行
- 数据库中是否有商品数据
- 用户是否已登录（查看购物车功能需要）
- 浏览器控制台是否有错误信息

