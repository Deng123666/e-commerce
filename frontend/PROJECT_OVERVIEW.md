# 📱 前端项目架构说明

## 🏗️ 技术架构

### 核心技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | 3.4+ | 前端框架 |
| TypeScript | 5.3+ | 类型系统 |
| Vite | 5.0+ | 构建工具 |
| Vue Router | 4.2+ | 路由管理 |
| Pinia | 2.1+ | 状态管理 |
| Element Plus | 2.5+ | UI组件库 |
| Tailwind CSS | 3.4+ | 样式框架 |
| Axios | 1.6+ | HTTP客户端 |

---

## 📁 目录结构详解

```
frontend/src/
│
├── api/                    # API接口层
│   ├── axios.ts           # Axios实例配置、拦截器
│   ├── auth.ts            # 认证相关API
│   ├── products.ts        # 商品相关API
│   ├── cart.ts            # 购物车相关API
│   └── orders.ts          # 订单相关API
│
├── assets/                 # 静态资源
│   └── (images, fonts, etc.)
│
├── components/            # 可复用组件
│   └── (common components)
│
├── layouts/               # 布局组件
│   └── MainLayout.vue     # 主布局（Header + Footer）
│
├── router/                # 路由配置
│   └── index.ts           # 路由定义、路由守卫
│
├── stores/                # Pinia状态管理
│   ├── auth.ts           # 用户认证状态
│   └── cart.ts           # 购物车状态
│
├── types/                 # TypeScript类型定义
│   └── index.ts          # 全局类型定义
│
├── views/                 # 页面组件
│   ├── auth/             # 认证相关页面
│   │   ├── Login.vue     # 登录页
│   │   └── Register.vue  # 注册页
│   ├── products/         # 商品相关页面
│   │   ├── ProductList.vue
│   │   └── ProductDetail.vue
│   ├── cart/             # 购物车页面
│   ├── orders/           # 订单相关页面
│   ├── user/             # 用户中心
│   ├── Home.vue          # 首页
│   └── NotFound.vue      # 404页面
│
├── App.vue                # 根组件
├── main.ts                # 应用入口
└── style.css              # 全局样式
```

---

## 🔄 数据流架构

```
┌─────────────────────────────────────────────────┐
│                   用户界面                        │
│              (Vue Components)                    │
└──────────────────┬──────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────┐
│                 状态管理层                        │
│                  (Pinia)                         │
│  ┌─────────────┐  ┌──────────────┐             │
│  │  Auth Store │  │  Cart Store  │             │
│  └─────────────┘  └──────────────┘             │
└──────────────────┬──────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────┐
│                  API层                           │
│              (API Services)                      │
│  ┌─────────┐  ┌──────────┐  ┌────────┐         │
│  │  auth   │  │ products │  │  cart  │         │
│  └─────────┘  └──────────┘  └────────┘         │
└──────────────────┬──────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────┐
│              Axios拦截器                         │
│        (请求/响应统一处理)                        │
└──────────────────┬──────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────┐
│               后端API                            │
│         (FastAPI Backend)                        │
└─────────────────────────────────────────────────┘
```

---

## 🔐 认证流程

### 登录流程

```
用户输入凭据
    ↓
表单验证
    ↓
调用 authStore.login()
    ↓
发送 POST /auth/login
    ↓
接收 { accessToken, refreshToken }
    ↓
存储到 localStorage 和 Cookie
    ↓
获取用户信息 GET /users/me
    ↓
更新 Pinia state
    ↓
路由跳转到首页
```

### 请求认证流程

```
发起API请求
    ↓
Axios请求拦截器
    ↓
从localStorage读取accessToken
    ↓
添加到请求头: Authorization: Bearer {token}
    ↓
发送请求到后端
    ↓
后端验证token
    ↓
401? → 跳转登录页
200? → 返回数据
```

### Token过期处理

```
API返回401
    ↓
Axios响应拦截器捕获
    ↓
清除本地token
    ↓
显示"未授权"提示
    ↓
跳转到登录页
```

---

## 🛣️ 路由设计

### 路由结构

```
/                           # 主布局
├── /                       # 首页 (公开)
├── /products               # 商品列表 (公开)
├── /products/:id           # 商品详情 (公开)
├── /cart                   # 购物车 (需登录)
├── /orders                 # 订单列表 (需登录)
└── /profile                # 个人中心 (需登录)

/login                      # 登录页 (独立布局)
/register                   # 注册页 (独立布局)
/*                          # 404页面
```

### 路由守卫逻辑

```typescript
beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth
  const isAuthenticated = authStore.isAuthenticated

  if (requiresAuth && !isAuthenticated) {
    // 需要登录但未登录 → 跳转登录页
    next('/login')
  } else if (to.name === 'Login' && isAuthenticated) {
    // 已登录访问登录页 → 跳转首页
    next('/')
  } else {
    next()
  }
})
```

---

## 💾 状态管理设计

### Auth Store

**状态**:
- `user`: 当前用户信息
- `accessToken`: 访问令牌
- `refreshToken`: 刷新令牌
- `loading`: 加载状态

**计算属性**:
- `isAuthenticated`: 是否已登录
- `isAdmin`: 是否是管理员
- `isVendor`: 是否是商家
- `isCustomer`: 是否是顾客

**方法**:
- `register()`: 用户注册
- `login()`: 用户登录
- `logout()`: 退出登录
- `fetchUserInfo()`: 获取用户信息
- `checkAuth()`: 检查认证状态

### Cart Store

**状态**:
- `cartItems`: 购物车商品列表
- `loading`: 加载状态

**计算属性**:
- `totalItems`: 商品总数量
- `totalPrice`: 商品总价格

**方法**:
- `fetchCartItems()`: 获取购物车
- `addToCart()`: 添加商品
- `updateCartItem()`: 更新数量
- `removeFromCart()`: 移除商品
- `clearCart()`: 清空购物车

---

## 🎨 样式系统

### Tailwind CSS工具类

主要使用的工具类：

**布局**:
- `flex`, `grid`, `container`
- `mx-auto`, `px-4`, `py-8`
- `max-w-7xl`, `min-h-screen`

**间距**:
- `mb-4`, `mt-6`, `p-4`, `space-x-4`

**颜色**:
- `bg-white`, `text-gray-700`
- `text-primary-600`, `bg-primary-500`

**响应式**:
- `sm:`, `md:`, `lg:`, `xl:`

### Element Plus组件定制

```vue
<style scoped>
:deep(.el-button) {
  /* 深度选择器自定义Element Plus组件 */
}
</style>
```

---

## 🔧 开发最佳实践

### 1. 组件通信

**父→子**: Props
```vue
<Child :prop-name="value" />
```

**子→父**: Emits
```vue
emit('update:modelValue', newValue)
```

**跨组件**: Pinia Store
```typescript
const authStore = useAuthStore()
authStore.user
```

### 2. API调用

**在Store中调用**:
```typescript
async function fetchData() {
  loading.value = true
  try {
    const response = await api.getData()
    data.value = response.data
  } catch (error) {
    ElMessage.error('获取失败')
  } finally {
    loading.value = false
  }
}
```

### 3. 错误处理

**统一在Axios拦截器处理**:
```typescript
instance.interceptors.response.use(
  response => response,
  error => {
    // 统一错误提示
    ElMessage.error(error.message)
    return Promise.reject(error)
  }
)
```

### 4. 类型安全

**定义接口类型**:
```typescript
interface User {
  id: number
  name: string
  email: string
}

const user = ref<User | null>(null)
```

### 5. 代码复用

**组合式函数 (Composables)**:
```typescript
// useProduct.ts
export function useProduct() {
  const product = ref<Product | null>(null)
  
  async function fetchProduct(id: number) {
    // ...
  }
  
  return { product, fetchProduct }
}
```

---

## 📊 性能优化

### 1. 路由懒加载

```typescript
component: () => import('@/views/Products.vue')
```

### 2. 组件懒加载

```vue
<script setup>
const AsyncComponent = defineAsyncComponent(
  () => import('./HeavyComponent.vue')
)
</script>
```

### 3. 图片懒加载

```vue
<el-image lazy :src="imageUrl" />
```

### 4. 防抖/节流

```typescript
import { debounce } from 'lodash-es'

const handleSearch = debounce((value) => {
  // 搜索逻辑
}, 300)
```

---

## 🧪 测试建议

### 单元测试 (Vitest)

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

describe('Login.vue', () => {
  it('renders properly', () => {
    const wrapper = mount(Login)
    expect(wrapper.text()).toContain('登录')
  })
})
```

### E2E测试 (Playwright)

```typescript
test('user can login', async ({ page }) => {
  await page.goto('http://localhost:3000/login')
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'password')
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL('http://localhost:3000/')
})
```

---

## 📦 构建部署

### 构建生产版本

```bash
npm run build
```

生成的文件在 `dist/` 目录。

### 环境变量

**开发环境**: `.env.development`
**生产环境**: `.env.production`

### Nginx配置示例

```nginx
server {
  listen 80;
  server_name example.com;
  root /var/www/frontend/dist;
  index index.html;

  location / {
    try_files $uri $uri/ /index.html;
  }

  location /api {
    proxy_pass http://backend:8000;
    proxy_set_header Host $host;
  }
}
```

---

## 🔮 未来规划

- [ ] 商品列表与筛选功能
- [ ] 购物车完整功能
- [ ] 订单管理系统
- [ ] 用户个人中心
- [ ] 商家管理后台
- [ ] 管理员后台
- [ ] 支付集成
- [ ] 实时通知
- [ ] 多语言支持
- [ ] 主题切换

---

## 📞 技术支持

如有问题，请参考：
- Vue 3 官方文档
- Element Plus 文档
- Pinia 文档
- 项目内的其他文档

Happy Coding! 🎉

