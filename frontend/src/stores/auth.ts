import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { User, UserLogin, UserRegister } from '@/types'
import { ElMessage } from 'element-plus'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(localStorage.getItem('accessToken'))
  const refreshToken = ref<string | null>(localStorage.getItem('refreshToken'))
  const loading = ref(false)

  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isVendor = computed(() => user.value?.role === 'vendor')
  const isCustomer = computed(() => user.value?.role === 'customer')

  // Register
  async function register(data: UserRegister) {
    loading.value = true
    try {
      const response = await authApi.register(data)
      ElMessage.success('注册成功！请查收邮箱验证邮件（如未配置邮件服务，请联系管理员）')
      return response.data
    } catch (error: any) {
      let message = '注册失败，请稍后重试'
      
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail
        // Translate common error messages to Chinese
        if (detail.includes('Email is already registered')) {
          message = '该邮箱已被注册'
        } else if (detail.includes('Phone number is already registered')) {
          message = '该手机号已被注册'
        } else if (detail.includes('Username is already registered')) {
          message = '该用户名已被注册'
        } else {
          message = detail
        }
      }
      
      ElMessage.error(message)
      throw error
    } finally {
      loading.value = false
    }
  }

  // Login
  async function login(data: UserLogin) {
    loading.value = true
    try {
      const response = await authApi.login(data)
      const { accessToken: token, refreshToken: refresh } = response.data
      
      // Save tokens
      accessToken.value = token
      refreshToken.value = refresh
      localStorage.setItem('accessToken', token)
      localStorage.setItem('refreshToken', refresh)

      // Get user info
      await fetchUserInfo()
      
      ElMessage.success('登录成功！欢迎回来')
      router.push('/')
      return response.data
    } catch (error: any) {
      let message = '登录失败，请检查账号密码'
      
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail
        // Translate common error messages to Chinese
        if (detail.includes('Invalid email or password')) {
          message = '邮箱或密码错误'
        } else if (detail.includes('Inactive user')) {
          message = '账户已被禁用，请联系管理员'
        } else if (detail.includes('Forbidden')) {
          message = '请先验证邮箱后再登录'
        } else {
          message = detail
        }
      }
      
      ElMessage.error(message)
      throw error
    } finally {
      loading.value = false
    }
  }

  // Logout
  async function logout() {
    try {
      await authApi.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear local state
      user.value = null
      accessToken.value = null
      refreshToken.value = null
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      
      ElMessage.success('已退出登录')
      router.push('/login')
    }
  }

  // Get user info
  async function fetchUserInfo() {
    if (!accessToken.value) return
    
    try {
      const response = await authApi.getCurrentUser()
      user.value = response.data
    } catch (error: any) {
      console.error('Failed to fetch user info:', error)
      // If failed to get user info, clear tokens
      if (error.response?.status === 401) {
        ElMessage.warning('登录已过期，请重新登录')
      }
      // Clear state but don't show logout message
      user.value = null
      accessToken.value = null
      refreshToken.value = null
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    }
  }

  // Check auth status on app load
  async function checkAuth() {
    if (accessToken.value) {
      await fetchUserInfo()
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    loading,
    isAuthenticated,
    isAdmin,
    isVendor,
    isCustomer,
    register,
    login,
    logout,
    fetchUserInfo,
    checkAuth
  }
})

