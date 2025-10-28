<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4">
    <div class="max-w-md w-full">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="flex justify-center mb-4">
          <el-icon :size="48" class="text-primary-600">
            <Shop />
          </el-icon>
        </div>
        <h2 class="text-3xl font-bold text-gray-900">欢迎回来</h2>
        <p class="mt-2 text-sm text-gray-600">登录您的账户</p>
      </div>

      <!-- Login Form -->
      <el-card shadow="hover" class="rounded-lg">
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          label-position="top"
          size="large"
        >
          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="loginForm.email"
              placeholder="请输入邮箱"
              :prefix-icon="Message"
            />
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              :prefix-icon="Lock"
              show-password
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              class="w-full"
              :loading="authStore.loading"
              @click="handleLogin"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>

        <!-- Links -->
        <div class="flex justify-between items-center text-sm mt-4">
          <router-link to="/forgot-password" class="text-primary-600 hover:text-primary-700">
            忘记密码？
          </router-link>
          <div class="text-gray-600">
            还没有账户？
            <router-link to="/register" class="text-primary-600 hover:text-primary-700 font-medium">
              立即注册
            </router-link>
          </div>
        </div>
      </el-card>

      <!-- Features -->
      <div class="mt-8 grid grid-cols-3 gap-4 text-center">
        <div class="bg-white p-4 rounded-lg shadow-sm">
          <el-icon :size="24" class="text-primary-600 mb-2">
            <ShoppingBag />
          </el-icon>
          <p class="text-xs text-gray-600">海量商品</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow-sm">
          <el-icon :size="24" class="text-primary-600 mb-2">
            <CreditCard />
          </el-icon>
          <p class="text-xs text-gray-600">安全支付</p>
        </div>
        <div class="bg-white p-4 rounded-lg shadow-sm">
          <el-icon :size="24" class="text-primary-600 mb-2">
            <Van />
          </el-icon>
          <p class="text-xs text-gray-600">快速配送</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { Message, Lock, Shop, ShoppingBag, CreditCard, Van } from '@element-plus/icons-vue'

const authStore = useAuthStore()
const loginFormRef = ref<FormInstance>()

const loginForm = reactive({
  email: '',
  password: ''
})

const loginRules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码长度不能少于8位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await authStore.login(loginForm)
        // Success message and redirect handled in store
      } catch (error: any) {
        // Error message already handled in store
        console.error('Login failed:', error)
      }
    } else {
      ElMessage.warning('请正确填写登录信息')
    }
  })
}
</script>

<style scoped>
:deep(.el-card) {
  border: none;
  border-radius: 16px !important;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

:deep(.el-input__wrapper) {
  border-radius: 10px !important;
  padding: 10px 16px !important;
  box-shadow: none !important;
  border: 1.5px solid #e5e7eb !important;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  border-color: #0ea5e9 !important;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #0ea5e9 !important;
  box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1) !important;
}

:deep(.el-input__inner) {
  font-size: 15px;
}

:deep(.el-button) {
  border-radius: 10px;
  padding: 12px 24px;
  font-weight: 500;
  transition: all 0.2s ease;
}

:deep(.el-button:hover) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
}
</style>

