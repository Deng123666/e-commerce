<template>
  <div v-loading="loading" class="max-w-6xl mx-auto">
    <el-empty v-if="!loading && !product" description="商品不存在">
      <el-button type="primary" @click="router.push('/products')">返回商品列表</el-button>
    </el-empty>

    <div v-else-if="product" class="bg-white rounded-lg shadow-sm p-8">
      <!-- Back Button -->
      <el-button
        class="mb-6"
        :icon="ArrowLeft"
        @click="router.back()"
      >
        返回
      </el-button>

      <div class="grid md:grid-cols-2 gap-8">
        <!-- Left: Image -->
        <div>
          <div class="aspect-square bg-gray-100 rounded-lg overflow-hidden">
            <el-image
              :src="product.image_url || 'https://via.placeholder.com/600'"
              fit="contain"
              class="w-full h-full"
            >
              <template #error>
                <div class="flex items-center justify-center h-full bg-gray-100">
                  <el-icon :size="100" class="text-gray-300">
                    <Picture />
                  </el-icon>
                </div>
              </template>
            </el-image>
          </div>
        </div>

        <!-- Right: Info -->
        <div>
          <!-- Category -->
          <el-tag class="mb-4">{{ getCategoryLabel(product.category) }}</el-tag>

          <!-- Title -->
          <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ product.name }}</h1>

          <!-- Stats -->
          <div class="flex items-center gap-4 mb-6 text-sm text-gray-500">
            <span class="flex items-center">
              <el-icon class="mr-1"><View /></el-icon>
              {{ product.view_count }} 次浏览
            </span>
            <span>•</span>
            <span>商品编号: {{ product.id }}</span>
          </div>

          <!-- Price -->
          <div class="bg-gray-50 rounded-lg p-6 mb-6">
            <div class="text-sm text-gray-500 mb-2">价格</div>
            <div class="flex items-baseline">
              <span class="text-4xl font-bold text-primary-600">¥{{ product.price.toFixed(2) }}</span>
            </div>
          </div>

          <!-- Stock -->
          <div class="mb-6">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-gray-700">库存状态</span>
              <el-tag v-if="product.is_active && product.stock > 0" type="success">
                有货 (剩余 {{ product.stock }} 件)
              </el-tag>
              <el-tag v-else type="info">缺货</el-tag>
            </div>
          </div>

          <!-- Quantity -->
          <div class="mb-6">
            <div class="text-sm font-medium text-gray-700 mb-2">数量</div>
            <el-input-number
              v-model="quantity"
              :min="1"
              :max="product.stock"
              :disabled="!product.is_active || product.stock === 0"
              size="large"
            />
          </div>

          <!-- Actions -->
          <div class="flex gap-4">
            <el-button
              type="primary"
              size="large"
              class="flex-1"
              :disabled="!product.is_active || product.stock === 0"
              :loading="addingToCart"
              @click="handleAddToCart"
            >
              <el-icon class="mr-2"><ShoppingCart /></el-icon>
              加入购物车
            </el-button>
            <el-button
              size="large"
              :icon="Star"
              @click="handleAddToWishlist"
            >
              收藏
            </el-button>
          </div>

          <!-- Time -->
          <div class="mt-6 pt-6 border-t border-gray-200 text-sm text-gray-500">
            <div class="mb-2">
              <span class="font-medium">上架时间:</span>
              {{ formatDate(product.created_at) }}
            </div>
            <div>
              <span class="font-medium">更新时间:</span>
              {{ formatDate(product.updated_at) }}
            </div>
          </div>
        </div>
      </div>

      <!-- Description -->
      <div class="mt-12 pt-8 border-t border-gray-200">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">商品描述</h2>
        <div class="prose max-w-none text-gray-600">
          <p>{{ product.description || '暂无描述' }}</p>
        </div>
      </div>

      <!-- Additional Info -->
      <div class="mt-8 grid md:grid-cols-3 gap-6">
        <div class="bg-blue-50 rounded-lg p-4">
          <div class="flex items-center mb-2">
            <el-icon :size="24" class="text-blue-600 mr-2"><Van /></el-icon>
            <h3 class="font-semibold text-gray-900">免费配送</h3>
          </div>
          <p class="text-sm text-gray-600">满99元免运费</p>
        </div>
        <div class="bg-green-50 rounded-lg p-4">
          <div class="flex items-center mb-2">
            <el-icon :size="24" class="text-green-600 mr-2"><CircleCheck /></el-icon>
            <h3 class="font-semibold text-gray-900">正品保证</h3>
          </div>
          <p class="text-sm text-gray-600">100%正品保障</p>
        </div>
        <div class="bg-purple-50 rounded-lg p-4">
          <div class="flex items-center mb-2">
            <el-icon :size="24" class="text-purple-600 mr-2"><Service /></el-icon>
            <h3 class="font-semibold text-gray-900">售后服务</h3>
          </div>
          <p class="text-sm text-gray-600">7天无理由退换</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ArrowLeft,
  Picture,
  View,
  ShoppingCart,
  Star,
  Van,
  CircleCheck,
  Service
} from '@element-plus/icons-vue'
import { productApi } from '@/api/products'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import type { Product } from '@/types'

const router = useRouter()
const route = useRoute()
const cartStore = useCartStore()
const authStore = useAuthStore()

const product = ref<Product | null>(null)
const loading = ref(false)
const quantity = ref(1)
const addingToCart = ref(false)

const categories = [
  { label: '电子产品', value: 'electronics' },
  { label: '时尚服饰', value: 'fashion' },
  { label: '家居用品', value: 'home' },
  { label: '图书音像', value: 'books' }
]

const getCategoryLabel = (category: string) => {
  const cat = categories.find(c => c.value === category)
  return cat?.label || category
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchProduct = async () => {
  const productId = parseInt(route.params.id as string)
  if (isNaN(productId)) {
    ElMessage.error('无效的商品ID')
    return
  }

  loading.value = true
  try {
    const response = await productApi.getProduct(productId)
    product.value = response.data
  } catch (error) {
    console.error('Failed to fetch product:', error)
    ElMessage.error('获取商品详情失败')
  } finally {
    loading.value = false
  }
}

const handleAddToCart = async () => {
  if (!authStore.isAuthenticated) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  if (!product.value) return

  addingToCart.value = true
  try {
    await cartStore.addToCart({
      product_id: product.value.id,
      quantity: quantity.value
    })
  } catch (error) {
    // Error already handled in store
  } finally {
    addingToCart.value = false
  }
}

const handleAddToWishlist = () => {
  if (!authStore.isAuthenticated) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  ElMessage.info('收藏功能开发中...')
}

onMounted(() => {
  fetchProduct()
})
</script>

<style scoped>
.prose p {
  line-height: 1.8;
  white-space: pre-wrap;
}
</style>
