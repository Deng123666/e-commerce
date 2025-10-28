# E-Commerce Frontend

基于 Vue 3 + TypeScript + Vite 的电商前端项目

## 技术栈

- **框架**: Vue 3 (Composition API)
- **语言**: TypeScript
- **构建工具**: Vite
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **UI 框架**: Element Plus
- **样式**: Tailwind CSS
- **HTTP 客户端**: Axios

## 功能特性

- ✅ 用户注册/登录
- ✅ JWT 认证
- ✅ 响应式设计
- ✅ 路由守卫
- 🚧 商品浏览
- 🚧 购物车
- 🚧 订单管理
- 🚧 个人中心

## 快速开始

### 安装依赖

```bash
npm install
# 或
yarn install
# 或
pnpm install
```

### 开发模式

```bash
npm run dev
```

应用将在 http://localhost:3000 启动

### 构建生产版本

```bash
npm run build
```

### 预览生产版本

```bash
npm run preview
```

## 项目结构

```
frontend/
├── public/             # 静态资源
├── src/
│   ├── api/           # API 接口
│   ├── assets/        # 资源文件
│   ├── components/    # 公共组件
│   ├── layouts/       # 布局组件
│   ├── router/        # 路由配置
│   ├── stores/        # Pinia 状态管理
│   ├── types/         # TypeScript 类型定义
│   ├── views/         # 页面组件
│   ├── App.vue        # 根组件
│   ├── main.ts        # 入口文件
│   └── style.css      # 全局样式
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## 环境变量

创建 `.env` 文件并配置：

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 开发说明

### API 代理

Vite 配置了 API 代理，所有 `/api` 开头的请求会被代理到后端服务器：

```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, '')
  }
}
```

### 认证流程

1. 用户登录成功后，access token 存储在 localStorage
2. refresh token 存储在 HttpOnly Cookie (由后端设置)
3. Axios 拦截器自动在请求头添加 Authorization
4. Token 过期时自动跳转到登录页

### 路由守卫

- 需要认证的路由会检查 token 状态
- 未登录用户访问受保护路由会重定向到登录页
- 已登录用户访问登录/注册页会重定向到首页

## 待实现功能

- [ ] 商品列表与筛选
- [ ] 商品详情页
- [ ] 购物车功能
- [ ] 订单管理
- [ ] 个人信息编辑
- [ ] 商家管理后台
- [ ] 管理员后台

## License

MIT

