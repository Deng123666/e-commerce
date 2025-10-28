import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const instance: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 10000,
  withCredentials: true, // Important for sending cookies
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
instance.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Get token from localStorage
    const token = localStorage.getItem('accessToken')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// Response interceptor
instance.interceptors.response.use(
  (response) => {
    return response
  },
  (error: AxiosError) => {
    if (error.response) {
      const status = error.response.status
      const data: any = error.response.data

      switch (status) {
        case 401:
          ElMessage.error('未授权，请重新登录')
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          router.push('/login')
          break
        case 403:
          ElMessage.error('没有权限访问此资源')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器错误')
          break
        default:
          ElMessage.error(data.message || data.detail || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络错误，请检查您的网络连接')
    } else {
      ElMessage.error('请求配置错误')
    }
    return Promise.reject(error)
  }
)

export default instance

