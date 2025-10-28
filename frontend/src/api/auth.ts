import request from './axios'
import type { UserRegister, UserLogin, AuthResponse, User, ChangePassword } from '@/types'

export const authApi = {
  // Register
  register(data: UserRegister) {
    return request.post<User>('/auth/register', data)
  },

  // Login
  login(data: UserLogin) {
    return request.post<AuthResponse>('/auth/login', data)
  },

  // Logout
  logout() {
    return request.get('/auth/logout')
  },

  // Verify email
  verifyEmail(token: string) {
    return request.post('/auth/verify-email', { token })
  },

  // Get current user
  getCurrentUser() {
    return request.get<User>('/users/me')
  },

  // Change password
  changePassword(data: ChangePassword) {
    return request.post('/auth/change_password', data)
  }
}

