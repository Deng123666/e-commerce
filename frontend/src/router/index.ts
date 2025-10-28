import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { requiresAuth: false, title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { requiresAuth: false, title: '注册' }
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        meta: { requiresAuth: false, title: '首页' }
      },
      {
        path: 'products',
        name: 'Products',
        component: () => import('@/views/products/ProductList.vue'),
        meta: { requiresAuth: false, title: '商品列表' }
      },
      {
        path: 'products/:id',
        name: 'ProductDetail',
        component: () => import('@/views/products/ProductDetail.vue'),
        meta: { requiresAuth: false, title: '商品详情' }
      },
      {
        path: 'cart',
        name: 'Cart',
        component: () => import('@/views/cart/Cart.vue'),
        meta: { requiresAuth: true, title: '购物车' }
      },
      {
        path: 'orders',
        name: 'Orders',
        component: () => import('@/views/orders/OrderList.vue'),
        meta: { requiresAuth: true, title: '我的订单' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/user/Profile.vue'),
        meta: { requiresAuth: true, title: '个人中心' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面不存在' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.meta.requiresAuth
  const isAuthenticated = authStore.isAuthenticated

  // Set page title
  document.title = to.meta.title ? `${to.meta.title} - E-Commerce` : 'E-Commerce'

  // Check authentication
  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else if ((to.name === 'Login' || to.name === 'Register') && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router

