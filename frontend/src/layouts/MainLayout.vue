<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <!-- Header -->
    <header class="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50 border-b border-gray-100">
      <div class="max-w-[1600px] mx-auto px-6 lg:px-12">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <div class="flex items-center cursor-pointer group" @click="router.push('/')">
            <div class="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center shadow-sm group-hover:shadow-md transition-shadow">
              <el-icon :size="20" class="text-white">
                <Shop />
              </el-icon>
            </div>
            <div class="ml-3">
              <div class="text-lg font-bold text-gray-900">星选商城</div>
              <div class="text-xs text-gray-500 -mt-0.5">Smart Shopping</div>
            </div>
          </div>

          <!-- Navigation -->
          <nav class="hidden md:flex space-x-2">
            <router-link
              to="/"
              class="nav-link"
            >
              <el-icon class="mr-1"><House /></el-icon>
              首页
            </router-link>
            <router-link
              to="/products"
              class="nav-link"
            >
              <el-icon class="mr-1"><Box /></el-icon>
              商品
            </router-link>
            <router-link
              to="/cart"
              class="nav-link"
            >
              <el-icon class="mr-1"><ShoppingCart /></el-icon>
              购物车
            </router-link>
            <router-link
              to="/orders"
              class="nav-link"
            >
              <el-icon class="mr-1"><List /></el-icon>
              订单
            </router-link>
            <router-link
              v-if="authStore.isAuthenticated"
              to="/profile"
              class="nav-link"
            >
              <el-icon class="mr-1"><User /></el-icon>
              个人档案
            </router-link>
          </nav>

          <!-- Right side -->
          <div class="flex items-center space-x-3">
            <!-- Logged in user -->
            <template v-if="authStore.isAuthenticated && authStore.user">
              <!-- User Avatar -->
              <el-tooltip :content="`${authStore.user.username} (${getRoleLabel(authStore.user.role)})`" placement="bottom">
                <el-avatar 
                  :size="36" 
                  :src="authStore.user.image_url" 
                  class="border-2 border-primary-100 cursor-pointer hover:border-primary-300 transition-colors"
                  @click="router.push('/profile')"
                >
                  <el-icon><User /></el-icon>
                </el-avatar>
              </el-tooltip>
              
              <!-- Change Password Button -->
              <el-button 
                size="default" 
                @click="showChangePasswordDialog = true"
                :icon="Lock"
              >
                修改密码
              </el-button>
              
              <!-- Logout Button -->
              <el-button 
                size="default" 
                type="danger" 
                @click="handleLogout"
                :icon="SwitchButton"
              >
                退出登录
              </el-button>
            </template>
            
            <!-- Not logged in -->
            <template v-else>
              <el-button @click="router.push('/register')" text>注册</el-button>
              <el-button type="primary" @click="router.push('/login')">登录</el-button>
            </template>
          </div>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="max-w-[1600px] mx-auto px-6 lg:px-12 py-8">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="bg-white/80 backdrop-blur-md border-t border-gray-100 mt-12">
      <div class="max-w-[1600px] mx-auto px-6 lg:px-12 py-6">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <p class="text-gray-500 text-sm">
            © 2025 星选商城. All rights reserved.
          </p>
          <div class="flex space-x-4 mt-2 md:mt-0 text-sm text-gray-500">
            <a href="#" class="hover:text-primary-600 transition">关于我们</a>
            <span>·</span>
            <a href="#" class="hover:text-primary-600 transition">联系我们</a>
            <span>·</span>
            <a href="#" class="hover:text-primary-600 transition">隐私政策</a>
          </div>
        </div>
      </div>
    </footer>

    <!-- Change Password Dialog -->
    <el-dialog
      v-model="showChangePasswordDialog"
      title="修改密码"
      width="400px"
    >
      <el-form label-position="top">
        <el-form-item label="当前密码">
          <el-input
            v-model="changePasswordForm.currentPassword"
            type="password"
            placeholder="请输入当前密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input
            v-model="changePasswordForm.newPassword"
            type="password"
            placeholder="至少8位，包含大小写字母、数字和特殊字符"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认新密码">
          <el-input
            v-model="changePasswordForm.confirmPassword"
            type="password"
            placeholder="请再次输入新密码"
            show-password
            @keyup.enter="handleChangePassword"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showChangePasswordDialog = false">取消</el-button>
        <el-button
          type="primary"
          :loading="changePasswordLoading"
          @click="handleChangePassword"
        >
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/api/auth'
import { ElMessageBox, ElMessage } from 'element-plus'
import { Shop, User, List, SwitchButton, Lock, House, Box, ShoppingCart } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const getRoleLabel = (role: string) => {
  const labels: Record<string, string> = {
    'admin': '管理员',
    'vendor': '商家',
    'customer': '顾客'
  }
  return labels[role] || role
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await authStore.logout()
  } catch (error) {
    // User cancelled
  }
}

// Change password dialog
const showChangePasswordDialog = ref(false)
const changePasswordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const changePasswordLoading = ref(false)

const handleChangePassword = async () => {
  if (!changePasswordForm.currentPassword || !changePasswordForm.newPassword || !changePasswordForm.confirmPassword) {
    ElMessage.warning('请填写完整信息')
    return
  }

  if (changePasswordForm.newPassword !== changePasswordForm.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }

  if (changePasswordForm.newPassword.length < 8) {
    ElMessage.error('新密码长度不能少于8位')
    return
  }

  // 验证新密码强度：至少包含大小写字母、数字和特殊字符
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/
  if (!passwordRegex.test(changePasswordForm.newPassword)) {
    ElMessage.error('新密码必须包含大小写字母、数字和特殊字符')
    return
  }

  changePasswordLoading.value = true
  try {
    await authApi.changePassword({
      password: changePasswordForm.currentPassword,
      new_password: changePasswordForm.newPassword
    })
    
    ElMessage.success('密码修改成功，请重新登录')
    showChangePasswordDialog.value = false
    
    // 清空表单
    changePasswordForm.currentPassword = ''
    changePasswordForm.newPassword = ''
    changePasswordForm.confirmPassword = ''
    
    // 退出登录
    await authStore.logout()
  } catch (error: any) {
    const message = error.response?.data?.message || error.message || '密码修改失败'
    ElMessage.error(message)
  } finally {
    changePasswordLoading.value = false
  }
}
</script>

<style scoped>
.nav-link {
  @apply flex items-center px-4 py-2 text-sm font-medium text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all duration-200;
}

.nav-link.router-link-active {
  @apply text-primary-600 bg-primary-50;
}

:deep(.el-dialog) {
  border-radius: 16px !important;
}

:deep(.el-dialog__header) {
  border-bottom: 1px solid #e5e7eb;
  padding: 20px 24px !important;
}

:deep(.el-dialog__body) {
  padding: 24px !important;
}

:deep(.el-dialog .el-input__wrapper) {
  border-radius: 10px !important;
  padding: 10px 16px !important;
  box-shadow: none !important;
  border: 1.5px solid #e5e7eb !important;
  transition: all 0.3s ease;
}

:deep(.el-dialog .el-input__wrapper:hover) {
  border-color: #0ea5e9 !important;
}

:deep(.el-dialog .el-input__wrapper.is-focus) {
  border-color: #0ea5e9 !important;
  box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1) !important;
}

:deep(.el-dialog .el-input__inner) {
  font-size: 15px;
}

:deep(.el-dialog .el-form-item__label) {
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 8px;
}

:deep(.el-button) {
  border-radius: 8px;
}
</style>

