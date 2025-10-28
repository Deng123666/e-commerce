# 🚀 项目启动完整指南

这个文档将指导您如何从零开始启动整个电商系统（后端 + 前端）。

## 📋 前置要求

确保您的系统已安装：

- ✅ Python 3.9+
- ✅ Node.js 16+
- ✅ PostgreSQL 12+
- ✅ Redis 6+

## 🔧 第一步：后端设置

### 1. 创建并激活Python虚拟环境

```bash
cd e-commerce

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 2. 安装后端依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件在 `e-commerce` 目录：

```env
# 数据库配置
DATABASE_URL=postgresql+asyncpg://用户名:密码@localhost:5432/ecommerce_db
DEFAULT_DATABASE_URL=postgresql+asyncpg://用户名:密码@localhost:5432/postgres

# JWT配置
SECRET_KEY=你的密钥（运行create_jwt_secret_key.py生成）
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis配置
REDIS_SESSION_URL=redis://localhost:6379

# 邮件配置（SendGrid）
SENDGRID_API_KEY=你的SendGrid API密钥
FROM_EMAIL=你的发件邮箱

# Stripe支付配置（可选）
STRIPE_SECRET_KEY=你的Stripe密钥
STRIPE_PUBLIC_KEY=你的Stripe公钥
STRIPE_WEBHOOK_SECRET=你的Webhook密钥

# 限流配置
REQUESTS_TIME_LIMIT=60
MAX_REQUESTS_PER_MINUTE=100
```

### 4. 生成JWT密钥

```bash
python create_jwt_secret_key.py
```

复制生成的密钥到 `.env` 文件的 `SECRET_KEY`。

### 5. 启动数据库服务

```bash
# PostgreSQL
# Linux:
sudo service postgresql start
# Mac:
brew services start postgresql
# Windows: 启动PostgreSQL服务

# Redis
# Linux:
sudo service redis start
# Mac:
brew services start redis
# Windows: 启动Redis服务
```

### 6. 运行数据库迁移

```bash
alembic upgrade head
```

### 7. 启动后端服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端将运行在：http://localhost:8000

API文档：http://localhost:8000/docs

---

## 🎨 第二步：前端设置

### 1. 进入前端目录

```bash
cd ../frontend  # 从e-commerce目录
```

### 2. 安装前端依赖

```bash
npm install
# 或
yarn install
# 或
pnpm install
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
echo "VITE_API_BASE_URL=http://localhost:8000" > .env
```

### 4. 启动前端开发服务器

```bash
npm run dev
```

前端将运行在：http://localhost:3000

---

## ✅ 第三步：验证系统

### 1. 打开浏览器访问

http://localhost:3000

### 2. 测试注册功能

1. 点击"立即注册"
2. 填写注册信息：
   ```
   用户名: testuser
   姓名: 张
   姓氏: 三
   邮箱: test@example.com
   密码: Test@123456
   手机号: 13800138000
   角色: 顾客
   ```
3. 提交注册

### 3. 测试登录功能

1. 使用注册的邮箱和密码登录
2. **注意**：如果未配置邮件服务，需要手动验证邮箱：

```sql
-- 在PostgreSQL中执行
UPDATE users SET is_verified = true WHERE email = 'test@example.com';
```

### 4. 查看API文档

访问：http://localhost:8000/docs

可以直接在这里测试所有API接口。

---

## 🔍 常见问题排查

### 问题1: 数据库连接失败

**错误**: `could not connect to server`

**解决**:
```bash
# 检查PostgreSQL是否运行
sudo service postgresql status

# 检查数据库是否存在
psql -U postgres -c "\l"

# 创建数据库（如果不存在）
psql -U postgres -c "CREATE DATABASE ecommerce_db;"
```

### 问题2: Redis连接失败

**错误**: `Error connecting to Redis`

**解决**:
```bash
# 检查Redis是否运行
redis-cli ping
# 应返回: PONG

# 如果未运行，启动Redis
sudo service redis start
```

### 问题3: 前端API请求跨域错误

**错误**: `CORS policy blocked`

**解决**: 检查后端 `app/main.py` 的CORS配置：
```python
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### 问题4: 邮箱验证问题

**临时解决**: 在数据库中手动设置用户为已验证：
```sql
UPDATE users SET is_verified = true WHERE email = '你的邮箱';
```

**长期方案**: 配置SendGrid邮件服务

---

## 📂 项目目录结构

```
fastapi-shop/
├── e-commerce/           # 后端项目
│   ├── app/             # 应用代码
│   ├── alembic/         # 数据库迁移
│   ├── requirements.txt # Python依赖
│   └── .env            # 环境变量
│
├── frontend/            # 前端项目
│   ├── src/            # 源代码
│   ├── package.json    # Node依赖
│   └── .env           # 环境变量
│
└── START_GUIDE.md     # 本文档
```

---

## 🎯 快速启动命令总结

### 终端1 - 后端
```bash
cd e-commerce
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### 终端2 - 前端
```bash
cd frontend
npm run dev
```

---

## 🌟 下一步

系统启动成功后，您可以：

1. ✨ 浏览商品（功能开发中）
2. 🛒 添加购物车（功能开发中）
3. 📦 创建订单（功能开发中）
4. 👤 管理个人信息（功能开发中）

**当前已实现的功能**：
- ✅ 用户注册
- ✅ 用户登录
- ✅ JWT认证
- ✅ 路由守卫

---

## 📚 开发资源

- **后端API文档**: http://localhost:8000/docs
- **前端开发指南**: `frontend/README.md`
- **后端开发指南**: `e-commerce/README.md`

---

## 💡 开发建议

1. **使用两个终端**: 一个运行后端，一个运行前端
2. **保持服务运行**: 开发时保持两个服务都在运行状态
3. **查看日志**: 出现问题时先查看终端日志
4. **使用开发工具**: 浏览器开发者工具、Vue DevTools等

---

## 🎉 祝您使用愉快！

如有问题，请检查：
1. 终端日志输出
2. 浏览器开发者工具控制台
3. 本文档的常见问题部分

Happy Coding! 🚀

