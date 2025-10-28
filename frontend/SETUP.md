# 前端项目启动指南

## 📦 安装依赖

在 `frontend` 目录下运行：

```bash
npm install
```

或使用其他包管理器：

```bash
yarn install
# 或
pnpm install
```

## ⚙️ 环境配置

创建 `.env` 文件（可以复制 `.env.example`）：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置后端 API 地址：

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 🚀 启动开发服务器

```bash
npm run dev
```

应用将在 http://localhost:3000 启动

## 🔗 与后端联调

### 1. 确保后端服务运行

在 `e-commerce` 目录下：

```bash
# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 启动 FastAPI 服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. CORS 配置

确保后端 `app/main.py` 中的 CORS 配置包含前端地址：

```python
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### 3. 测试连接

1. 访问 http://localhost:3000
2. 点击"注册"
3. 填写注册信息并提交
4. 查看浏览器开发者工具的 Network 标签，确认请求发送到后端

## 📝 功能测试

### 注册功能

1. 访问注册页面：http://localhost:3000/register
2. 填写信息：
   - 用户名：至少3个字符
   - 姓名：至少3个字符
   - 姓氏：至少1个字符
   - 邮箱：有效的邮箱格式
   - 密码：至少8位，包含大小写字母、数字和特殊字符
   - 手机号：任意格式（后端验证较宽松）
   - 角色：选择"顾客"或"商家"
3. 提交注册
4. 注册成功后会提示查收验证邮件

### 登录功能

1. 访问登录页面：http://localhost:3000/login
2. 输入邮箱和密码
3. 点击登录
4. 登录成功后会跳转到首页
5. 导航栏会显示用户头像和购物车图标

### 注意事项

⚠️ **邮箱验证**: 
- 后端需要配置 SendGrid 才能发送验证邮件
- 如果未配置邮件服务，可以临时在数据库中手动设置 `is_verified=true`

⚠️ **数据库**: 
- 确保 PostgreSQL 数据库已运行
- 确保后端已执行数据库迁移

## 🛠️ 开发工具推荐

### VS Code 插件

- Volar (Vue 3 支持)
- TypeScript Vue Plugin (Volar)
- Tailwind CSS IntelliSense
- ESLint
- Prettier

### 浏览器插件

- Vue.js devtools
- React Developer Tools (用于调试 Element Plus)

## 📖 技术文档

- [Vue 3 文档](https://cn.vuejs.org/)
- [Vite 文档](https://cn.vitejs.dev/)
- [Vue Router 文档](https://router.vuejs.org/zh/)
- [Pinia 文档](https://pinia.vuejs.org/zh/)
- [Element Plus 文档](https://element-plus.org/zh-CN/)
- [Tailwind CSS 文档](https://tailwindcss.com/docs)

## ❓ 常见问题

### 1. 端口被占用

如果 3000 端口被占用，可以修改 `vite.config.ts`：

```typescript
server: {
  port: 3001,  // 改成其他端口
  // ...
}
```

### 2. API 请求失败

检查：
- 后端是否运行在 8000 端口
- CORS 配置是否正确
- 浏览器控制台的错误信息

### 3. 登录后立即退出

可能原因：
- Token 验证失败
- 用户信息获取失败
- 检查浏览器控制台的错误信息

### 4. 样式不生效

```bash
# 重新安装依赖
rm -rf node_modules package-lock.json
npm install

# 清除 Vite 缓存
npm run dev -- --force
```

## 🎨 自定义配置

### 修改主题色

编辑 `tailwind.config.js` 中的 primary 颜色：

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // 修改这里的颜色值
        500: '#0ea5e9',
        // ...
      }
    }
  }
}
```

### 修改 API 代理

编辑 `vite.config.ts` 中的 proxy 配置：

```typescript
proxy: {
  '/api': {
    target: 'http://your-backend-url',
    changeOrigin: true,
  }
}
```

## 📞 获取帮助

如有问题，请检查：
1. 浏览器开发者工具的 Console 和 Network 标签
2. 后端日志
3. 本文档的常见问题部分

Good luck! 🎉

