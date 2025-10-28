# ⚡ 快速启动指南

这是一个5分钟快速启动指南，帮助您快速运行整个项目。

---

## 🎯 前提条件

确保已安装：
- ✅ Python 3.9+
- ✅ Node.js 16+
- ✅ PostgreSQL
- ✅ Redis

---

## 🚀 3步启动

### 步骤1: 启动后端（2分钟）

```bash
# 1. 进入后端目录
cd e-commerce

# 2. 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 创建.env文件（复制下面内容）
# 编辑 .env 文件，填入您的数据库配置
```

**创建 `e-commerce/.env` 文件**:
```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ecommerce_db
DEFAULT_DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/postgres
SECRET_KEY=your-secret-key-here-use-create_jwt_secret_key.py
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
REDIS_SESSION_URL=redis://localhost:6379
SENDGRID_API_KEY=optional
FROM_EMAIL=optional
STRIPE_SECRET_KEY=optional
STRIPE_PUBLIC_KEY=optional
STRIPE_WEBHOOK_SECRET=optional
REQUESTS_TIME_LIMIT=60
MAX_REQUESTS_PER_MINUTE=100
```

```bash
# 5. 生成JWT密钥
python create_jwt_secret_key.py
# 复制输出的密钥，粘贴到 .env 的 SECRET_KEY

# 6. 启动服务
uvicorn app.main:app --reload --port 8000
```

✅ 后端运行在: http://localhost:8000

---

### 步骤2: 启动前端（1分钟）

打开**新终端窗口**：

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖（首次运行）
npm install

# 3. 启动开发服务器
npm run dev
```

✅ 前端运行在: http://localhost:3000

---

### 步骤3: 测试功能（2分钟）

1. **打开浏览器**: http://localhost:3000

2. **注册账户**:
   - 点击"立即注册"
   - 填写信息:
     ```
     用户名: testuser
     姓名: 张三
     姓氏: 测试
     邮箱: test@example.com
     密码: Test@123456
     手机: 13800138000
     角色: 顾客
     ```
   - 提交注册

3. **验证邮箱**（如果没有配置邮件服务）:
   ```bash
   # 在PostgreSQL中执行
   psql -U postgres -d ecommerce_db
   UPDATE users SET is_verified = true WHERE email = 'test@example.com';
   \q
   ```

4. **登录**:
   - 邮箱: test@example.com
   - 密码: Test@123456

5. **浏览系统**:
   - ✅ 查看首页
   - ✅ 点击分类
   - ✅ 查看购物车
   - ✅ 个人中心

---

## 🎉 完成！

现在您可以开始开发了！

---

## 📝 常用命令

### 后端
```bash
# 启动服务
uvicorn app.main:app --reload

# 查看API文档
# 访问 http://localhost:8000/docs

# 数据库迁移
alembic upgrade head

# 创建新迁移
alembic revision --autogenerate -m "description"
```

### 前端
```bash
# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

---

## 🐛 常见问题

### 1. 数据库连接失败

```bash
# 创建数据库
psql -U postgres -c "CREATE DATABASE ecommerce_db;"

# 检查连接
psql -U postgres -d ecommerce_db -c "SELECT 1;"
```

### 2. Redis连接失败

```bash
# 启动Redis
sudo service redis start  # Linux
brew services start redis  # Mac

# 测试连接
redis-cli ping  # 应返回 PONG
```

### 3. 端口被占用

**后端端口冲突**:
```bash
# 使用其他端口
uvicorn app.main:app --reload --port 8001
```

**前端端口冲突**:
编辑 `frontend/vite.config.ts`:
```typescript
server: {
  port: 3001,  // 改成其他端口
}
```

### 4. 邮箱验证问题

临时方案：手动设置用户为已验证
```sql
UPDATE users SET is_verified = true WHERE email = '你的邮箱';
```

长期方案：配置SendGrid邮件服务

---

## 📚 更多文档

- **完整启动指南**: `START_GUIDE.md`
- **前端文档**: `frontend/README.md`
- **项目架构**: `frontend/PROJECT_OVERVIEW.md`
- **功能清单**: `frontend/COMPLETED_FEATURES.md`

---

## 💡 开发建议

1. **使用两个终端窗口**:
   - 终端1: 后端服务
   - 终端2: 前端服务

2. **查看日志**:
   - 后端日志在终端1
   - 前端日志在终端2
   - 浏览器控制台

3. **推荐工具**:
   - VS Code + Volar插件
   - Chrome DevTools
   - Vue DevTools扩展

4. **调试API**:
   - Swagger UI: http://localhost:8000/docs
   - Postman/Insomnia

---

## 🎊 恭喜！

您的开发环境已完全配置好！

开始愉快地编码吧！🚀

---

**需要帮助？**
- 查看详细文档
- 检查终端日志
- 查看浏览器控制台

