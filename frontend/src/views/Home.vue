<template>
  <div>
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-primary-600 to-indigo-600 text-white rounded-2xl p-12 mb-8">
      <div class="max-w-3xl">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">欢迎来到我们的商城</h1>
        <p class="text-xl mb-8 text-primary-100">发现优质商品，享受购物乐趣</p>
        <el-button type="info" size="large" @click="router.push('/products')" plain>
          开始购物
          <el-icon class="ml-2"><Right /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- Categories -->
    <div class="mb-12">
      <h2 class="text-2xl font-bold mb-6">推荐商品分类</h2>
      <el-row :gutter="20">
        <el-col :xs="12" :sm="6" v-for="category in categories" :key="category.value">
          <el-card 
            shadow="hover" 
            class="cursor-pointer hover:shadow-lg transition-shadow mb-4"
            @click="handleCategoryClick(category.value)"
          >
            <div class="text-center py-4">
              <el-icon :size="48" :color="category.color" class="mb-3">
                <component :is="category.icon" />
              </el-icon>
              <h3 class="text-lg font-semibold text-gray-800">{{ category.label }}</h3>
              <p class="text-sm text-gray-500 mt-1">{{ category.description }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- Features -->
    <div class="grid md:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <el-icon :size="32" class="text-green-500">
              <CircleCheck />
            </el-icon>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">品质保证</h3>
            <p class="text-gray-600">所有商品均经过严格筛选，确保品质</p>
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <el-icon :size="32" class="text-blue-500">
              <Van />
            </el-icon>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">快速配送</h3>
            <p class="text-gray-600">专业物流团队，快速送达</p>
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <el-icon :size="32" class="text-purple-500">
              <Service />
            </el-icon>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">贴心服务</h3>
            <p class="text-gray-600">7x24小时客服支持，随时为您服务</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Right, CircleCheck, Van, Service, Cellphone, Female, House, Reading } from '@element-plus/icons-vue'
import { CategoryEnum } from '@/types'

const router = useRouter()

const categories = [
  {
    label: '电子产品',
    value: CategoryEnum.ELECTRONICS,
    icon: Cellphone,
    color: '#0ea5e9',
    description: '手机、电脑等'
  },
  {
    label: '时尚服饰',
    value: CategoryEnum.FASHION,
    icon: Female,
    color: '#ec4899',
    description: '服装、鞋包等'
  },
  {
    label: '家居用品',
    value: CategoryEnum.HOME,
    icon: House,
    color: '#8b5cf6',
    description: '家具、装饰等'
  },
  {
    label: '图书音像',
    value: CategoryEnum.BOOKS,
    icon: Reading,
    color: '#f59e0b',
    description: '图书、音乐等'
  }
]

const handleCategoryClick = (category: string) => {
  router.push({
    name: 'Products',
    query: { category }
  })
}
</script>

