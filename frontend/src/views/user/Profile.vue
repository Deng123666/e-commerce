<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">个人档案</h1>

    <div class="grid md:grid-cols-3 gap-6">
      <!-- Left: User Info Card -->
      <div class="md:col-span-1">
        <el-card shadow="hover">
          <div class="text-center">
            <el-avatar :size="100" :src="authStore.user?.image_url" class="mb-4">
              <el-icon :size="50"><User /></el-icon>
            </el-avatar>
            <h2 class="text-xl font-semibold mb-1">{{ authStore.user?.username }}</h2>
            <p class="text-sm text-gray-500 mb-3">{{ authStore.user?.email }}</p>
            <el-tag :type="getRoleType(authStore.user?.role || '')" size="small">
              {{ getRoleLabel(authStore.user?.role || '') }}
            </el-tag>
          </div>
        </el-card>
      </div>

      <!-- Right: Edit Form -->
      <div class="md:col-span-2">
        <el-card shadow="hover">
          <template #header>
            <div class="flex justify-between items-center">
              <span class="font-semibold">基本信息</span>
              <el-button v-if="!isEditing" type="primary" size="small" @click="startEdit">
                编辑
              </el-button>
            </div>
          </template>

          <el-form
            ref="formRef"
            :model="formData"
            :rules="rules"
            label-width="100px"
            label-position="left"
          >
            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="formData.username"
                :disabled="!isEditing"
                placeholder="请输入用户名"
              />
            </el-form-item>

            <el-form-item label="姓名" prop="name">
              <el-input
                v-model="formData.name"
                :disabled="!isEditing"
                placeholder="请输入姓名"
              />
            </el-form-item>

            <el-form-item label="姓氏" prop="surname">
              <el-input
                v-model="formData.surname"
                :disabled="!isEditing"
                placeholder="请输入姓氏"
              />
            </el-form-item>

            <el-form-item label="邮箱">
              <el-input
                :model-value="authStore.user?.email"
                disabled
                placeholder="邮箱不可修改"
              />
            </el-form-item>

            <el-form-item label="手机号" prop="phone_number">
              <el-input
                v-model="formData.phone_number"
                :disabled="!isEditing"
                placeholder="请输入手机号"
              />
            </el-form-item>

            <el-divider content-position="left">收货地址</el-divider>

            <el-form-item label="国家/地区" prop="sensitive_info.country">
              <el-input
                v-model="formData.sensitive_info.country"
                :disabled="!isEditing"
                placeholder="请输入国家/地区"
              />
            </el-form-item>

            <el-form-item label="省/州" prop="sensitive_info.state">
              <el-input
                v-model="formData.sensitive_info.state"
                :disabled="!isEditing"
                placeholder="请输入省/州"
              />
            </el-form-item>

            <el-form-item label="城市" prop="sensitive_info.city">
              <el-input
                v-model="formData.sensitive_info.city"
                :disabled="!isEditing"
                placeholder="请输入城市"
              />
            </el-form-item>

            <el-form-item label="街道地址" prop="sensitive_info.street">
              <el-input
                v-model="formData.sensitive_info.street"
                :disabled="!isEditing"
                type="textarea"
                :rows="2"
                placeholder="请输入详细街道地址"
              />
            </el-form-item>

            <el-form-item label="邮政编码" prop="sensitive_info.zip_code">
              <el-input
                v-model="formData.sensitive_info.zip_code"
                :disabled="!isEditing"
                placeholder="请输入邮政编码"
              />
            </el-form-item>

            <el-form-item v-if="isEditing">
              <el-button @click="cancelEdit">取消</el-button>
              <el-button type="primary" :loading="loading" @click="saveProfile">
                保存
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import axios from '@/api/axios'

const authStore = useAuthStore()
const formRef = ref<FormInstance>()
const isEditing = ref(false)
const loading = ref(false)

const formData = reactive({
  username: '',
  name: '',
  surname: '',
  phone_number: '',
  sensitive_info: {
    country: '',
    state: '',
    city: '',
    street: '',
    zip_code: ''
  }
})

const rules: FormRules = {
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
  phone_number: [
    { required: true, message: '请输入手机号', trigger: 'blur' }
  ]
}

const getRoleType = (role: string) => {
  const types: Record<string, any> = {
    'admin': 'danger',
    'vendor': 'warning',
    'customer': 'success'
  }
  return types[role] || 'info'
}

const getRoleLabel = (role: string) => {
  const labels: Record<string, string> = {
    'admin': '管理员',
    'vendor': '商家',
    'customer': '顾客'
  }
  return labels[role] || role
}

const loadUserData = () => {
  if (authStore.user) {
    formData.username = authStore.user.username || ''
    formData.name = authStore.user.name || ''
    formData.surname = authStore.user.surname || ''
    formData.phone_number = authStore.user.phone_number || ''
    
    if (authStore.user.sensitive_info) {
      formData.sensitive_info = {
        country: authStore.user.sensitive_info.country || '',
        state: authStore.user.sensitive_info.state || '',
        city: authStore.user.sensitive_info.city || '',
        street: authStore.user.sensitive_info.street || '',
        zip_code: authStore.user.sensitive_info.zip_code || ''
      }
    }
  }
}

const startEdit = () => {
  isEditing.value = true
  loadUserData()
}

const cancelEdit = () => {
  isEditing.value = false
  loadUserData()
}

const saveProfile = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const updateData = {
          username: formData.username,
          name: formData.name,
          surname: formData.surname,
          phone_number: formData.phone_number,
          sensitive_info: formData.sensitive_info
        }

        await axios.put(`/users/${authStore.user?.id}`, updateData)
        
        // Refresh user info
        await authStore.fetchUserInfo()
        
        ElMessage.success('个人信息更新成功')
        isEditing.value = false
      } catch (error: any) {
        const message = error.response?.data?.detail || '更新失败'
        ElMessage.error(message)
      } finally {
        loading.value = false
      }
    }
  })
}

onMounted(() => {
  loadUserData()
})
</script>

<style scoped>
:deep(.el-divider__text) {
  background-color: #fff;
  font-weight: 500;
  color: #606266;
}

:deep(.el-card) {
  border-radius: 16px !important;
  border: 1px solid #e5e7eb !important;
}

:deep(.el-input__wrapper) {
  border-radius: 10px !important;
  padding: 10px 16px !important;
  box-shadow: none !important;
  border: 1.5px solid #e5e7eb !important;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover:not(.is-disabled)) {
  border-color: #0ea5e9 !important;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #0ea5e9 !important;
  box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1) !important;
}

:deep(.el-input__wrapper.is-disabled) {
  background-color: #f9fafb !important;
  border-color: #e5e7eb !important;
}

:deep(.el-input__inner) {
  font-size: 15px;
}

:deep(.el-textarea__inner) {
  border-radius: 10px !important;
  padding: 12px 16px !important;
  border: 1.5px solid #e5e7eb !important;
  font-size: 15px;
  transition: all 0.3s ease;
}

:deep(.el-textarea__inner:hover:not(:disabled)) {
  border-color: #0ea5e9 !important;
}

:deep(.el-textarea__inner:focus) {
  border-color: #0ea5e9 !important;
  box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1) !important;
}

:deep(.el-button) {
  border-radius: 10px;
  padding: 10px 20px;
  font-weight: 500;
  transition: all 0.2s ease;
}

:deep(.el-button:hover) {
  transform: translateY(-1px);
}

:deep(.el-avatar) {
  border: 3px solid #e5e7eb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 8px;
}
</style>
