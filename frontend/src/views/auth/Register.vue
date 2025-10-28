<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4 py-12">
    <div class="max-w-2xl w-full">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="flex justify-center mb-4">
          <el-icon :size="48" class="text-primary-600">
            <Shop />
          </el-icon>
        </div>
        <h2 class="text-3xl font-bold text-gray-900">创建账户</h2>
        <p class="mt-2 text-sm text-gray-600">加入我们，开始购物之旅</p>
      </div>

      <!-- Register Form -->
      <el-card shadow="hover" class="rounded-lg">
        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          label-position="top"
          size="large"
        >
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="用户名" prop="username">
                <el-input
                  v-model="registerForm.username"
                  placeholder="请输入用户名"
                  :prefix-icon="User"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="手机号" prop="phone_number">
                <el-input
                  v-model="registerForm.phone_number"
                  placeholder="请输入手机号"
                  :prefix-icon="Phone"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="姓名" prop="name">
                <el-input
                  v-model="registerForm.name"
                  placeholder="请输入姓名"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="姓氏" prop="surname">
                <el-input
                  v-model="registerForm.surname"
                  placeholder="请输入姓氏"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="请输入邮箱"
              :prefix-icon="Message"
            />
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码（至少8位，包含大小写字母、数字和特殊字符）"
              :prefix-icon="Lock"
              show-password
            />
          </el-form-item>

          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              :prefix-icon="Lock"
              show-password
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <el-form-item label="角色" prop="role">
            <el-radio-group v-model="registerForm.role">
              <el-radio label="customer">顾客</el-radio>
              <el-radio label="vendor">商家</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              class="w-full"
              :loading="authStore.loading"
              @click="handleRegister"
            >
              注册
            </el-button>
          </el-form-item>
        </el-form>

        <!-- Link to login -->
        <div class="text-center text-sm mt-4">
          <span class="text-gray-600">已有账户？</span>
          <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-medium ml-1">
            立即登录
          </router-link>
        </div>
      </el-card>

      <!-- Info -->
      <div class="mt-6 text-center text-xs text-gray-500">
        <p>注册即表示您同意我们的服务条款和隐私政策</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { User, Phone, Message, Lock, Shop } from '@element-plus/icons-vue'
import { UserRole } from '@/types'

const router = useRouter()
const authStore = useAuthStore()
const registerFormRef = ref<FormInstance>()

const registerForm = reactive({
  username: '',
  name: '',
  surname: '',
  email: '',
  password: '',
  confirmPassword: '',
  phone_number: '',
  role: 'customer' as UserRole
})

const validatePassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else if (!/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*\-./]).{8,}$/.test(value)) {
    callback(new Error('密码必须至少8位，包含大小写字母、数字和特殊字符'))
  } else {
    callback()
  }
}

const validateConfirmPassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const registerRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在 3 到 50 个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 3, max: 100, message: '姓名长度在 3 到 100 个字符', trigger: 'blur' }
  ],
  surname: [
    { required: true, message: '请输入姓氏', trigger: 'blur' },
    { min: 1, max: 100, message: '姓氏长度在 1 到 100 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ],
  phone_number: [
    { required: true, message: '请输入手机号', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const { confirmPassword, ...data } = registerForm
        await authStore.register(data)
        // Redirect to login after successful registration
        setTimeout(() => {
          router.push('/login')
        }, 2000)
      } catch (error: any) {
        // Error message already handled in store
        console.error('Register failed:', error)
      }
    } else {
      ElMessage.warning('请正确填写注册信息')
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

:deep(.el-radio-group) {
  width: 100%;
}

:deep(.el-radio) {
  margin-right: 24px;
  font-size: 15px;
}
</style>

