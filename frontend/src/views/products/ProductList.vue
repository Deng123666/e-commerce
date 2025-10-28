<template>
  <div class="flex gap-6">
    <!-- Left Sidebar - Categories -->
    <aside class="w-64 flex-shrink-0">
      <div class="bg-white rounded-xl shadow-sm p-5 sticky top-20 border border-gray-100">
        <h3 class="text-lg font-semibold mb-4 text-gray-900">商品分类</h3>
        <ul class="space-y-2">
          <li>
            <button
              @click="selectCategory(null)"
              :class="[
                'w-full text-left px-4 py-2 rounded-lg transition-colors',
                selectedCategory === null
                  ? 'bg-primary-50 text-primary-600 font-medium'
                  : 'text-gray-700 hover:bg-gray-50'
              ]"
            >
              全部商品
            </button>
          </li>
          <li v-for="category in categories" :key="category.value">
            <button
              @click="selectCategory(category.value)"
              :class="[
                'w-full text-left px-4 py-2 rounded-lg transition-colors flex items-center justify-between',
                selectedCategory === category.value
                  ? 'bg-primary-50 text-primary-600 font-medium'
                  : 'text-gray-700 hover:bg-gray-50'
              ]"
            >
              <span class="flex items-center">
                <el-icon :size="18" class="mr-2">
                  <component :is="category.icon" />
                </el-icon>
                {{ category.label }}
              </span>
              <el-icon v-if="selectedCategory === category.value" :size="16">
                <Check />
              </el-icon>
            </button>
          </li>
        </ul>

        <!-- Price Filter -->
        <div class="mt-6 pt-6 border-t border-gray-200">
          <h4 class="text-sm font-semibold mb-4 text-gray-900 flex items-center">
            <el-icon class="mr-2" :size="16"><Money /></el-icon>
            价格区间
          </h4>
          <div class="space-y-3">
            <div>
              <label class="text-xs text-gray-600 mb-1.5 block font-medium">最低价</label>
              <el-input
                v-model.number="priceRange.min"
                placeholder="¥ 0"
                class="price-input"
              >
                <template #prefix>
                  <span class="text-gray-400 text-sm">¥</span>
                </template>
              </el-input>
            </div>
            <div>
              <label class="text-xs text-gray-600 mb-1.5 block font-medium">最高价</label>
              <el-input
                v-model.number="priceRange.max"
                placeholder="不限"
                class="price-input"
              >
                <template #prefix>
                  <span class="text-gray-400 text-sm">¥</span>
                </template>
              </el-input>
            </div>
            <el-button type="primary" size="default" class="w-full !rounded-lg !mt-4" @click="applyPriceFilter">
              <el-icon class="mr-1"><Check /></el-icon>
              应用筛选
            </el-button>
          </div>
        </div>

        <!-- Availability Filter -->
        <div class="mt-6 pt-6 border-t border-gray-200">
          <h4 class="text-sm font-semibold mb-3 text-gray-900">库存状态</h4>
          <el-radio-group v-model="availability" @change="fetchProducts" class="flex flex-col space-y-2">
            <el-radio :label="null">全部</el-radio>
            <el-radio :label="true">有货</el-radio>
            <el-radio :label="false">缺货</el-radio>
          </el-radio-group>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1">
      <!-- Search Bar -->
      <div class="mb-6">
        <el-input
          v-model="searchQuery"
          placeholder="搜索您想要的商品..."
          size="large"
          clearable
          @keyup.enter="handleSearch"
          @clear="handleSearch"
          class="search-input"
        >
          <template #prefix>
            <el-icon class="text-gray-400"><Search /></el-icon>
          </template>
          <template #append>
            <el-button type="primary" @click="handleSearch" class="search-btn" :icon="Search" />
          </template>
        </el-input>
      </div>

      <!-- Products Grid -->
      <div v-loading="loading" class="min-h-[400px]">
        <!-- No Results -->
        <el-empty v-if="!loading && products.length === 0" description="暂无商品">
          <el-button type="primary" @click="resetFilters">重置筛选</el-button>
        </el-empty>

        <!-- Products -->
        <div v-else>
          <!-- Sort and Count -->
          <div class="bg-white rounded-xl p-4 mb-6 flex justify-between items-center border border-gray-100">
            <div class="flex items-center">
              <el-icon class="text-primary-600 mr-2" :size="18"><Box /></el-icon>
              <span class="text-sm text-gray-600">
                共找到 <span class="font-semibold text-primary-600 text-base">{{ totalProducts }}</span> 件商品
              </span>
            </div>
            <el-select v-model="sortBy" placeholder="排序方式" size="default" @change="fetchProducts" class="sort-select">
              <el-option label="默认排序" value="default" />
              <el-option label="价格从低到高" value="price_asc" />
              <el-option label="价格从高到低" value="price_desc" />
              <el-option label="最新上架" value="newest" />
            </el-select>
          </div>

          <!-- Product Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <el-card
              v-for="product in products"
              :key="product.id"
              shadow="hover"
              :body-style="{ padding: '0px' }"
              class="cursor-pointer transition-all hover:-translate-y-1"
              @click="goToProductDetail(product.id)"
            >
              <!-- Product Image -->
              <div class="relative aspect-square bg-gray-100 overflow-hidden">
                <el-image
                  :src="product.image_url || 'https://via.placeholder.com/300'"
                  fit="cover"
                  class="w-full h-full"
                  lazy
                >
                  <template #error>
                    <div class="flex items-center justify-center h-full bg-gray-100">
                      <el-icon :size="50" class="text-gray-300">
                        <Picture />
                      </el-icon>
                    </div>
                  </template>
                </el-image>
                
                <!-- Stock Badge -->
                <div class="absolute top-2 right-2">
                  <el-tag v-if="product.is_active && product.stock > 0" type="success" size="small">
                    有货
                  </el-tag>
                  <el-tag v-else type="info" size="small">缺货</el-tag>
                </div>

                <!-- Category Badge -->
                <div class="absolute top-2 left-2">
                  <el-tag size="small">{{ getCategoryLabel(product.category) }}</el-tag>
                </div>
              </div>

              <!-- Product Info -->
              <div class="p-4">
                <h3 class="text-base font-semibold text-gray-900 mb-2 line-clamp-2 h-12">
                  {{ product.name }}
                </h3>
                <p class="text-sm text-gray-500 mb-3 line-clamp-2 h-10">
                  {{ product.description }}
                </p>
                
                <div class="flex items-center justify-between">
                  <div>
                    <span class="text-2xl font-bold text-primary-600">
                      ¥{{ product.price.toFixed(2) }}
                    </span>
                  </div>
                  <div class="text-xs text-gray-500">
                    库存: {{ product.stock }}
                  </div>
                </div>

                <!-- View Count -->
                <div class="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
                  <span class="text-xs text-gray-400 flex items-center">
                    <el-icon :size="14" class="mr-1"><View /></el-icon>
                    {{ product.view_count }} 次浏览
                  </span>
                  <el-button 
                    type="primary" 
                    size="small" 
                    :disabled="!product.is_active || product.stock === 0"
                    @click.stop="addToCart(product)"
                  >
                    加入购物车
                  </el-button>
                </div>
              </div>
            </el-card>
          </div>

          <!-- Pagination -->
          <div class="flex justify-center mt-8">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[12, 24, 36, 48]"
              :total="totalProducts"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handlePageChange"
            />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Check, Picture, View, Cellphone, Female, House, Reading, Money, Box } from '@element-plus/icons-vue'
import { productApi } from '@/api/products'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import type { Product, CategoryEnum } from '@/types'

const router = useRouter()
const route = useRoute()
const cartStore = useCartStore()
const authStore = useAuthStore()

// State
const products = ref<Product[]>([])
const loading = ref(false)
const searchQuery = ref('')
const selectedCategory = ref<string | null>(null)
const currentPage = ref(1)
const pageSize = ref(12)
const totalProducts = ref(0)
const sortBy = ref('default')
const availability = ref<boolean | null>(null)
const priceRange = ref({
  min: undefined as number | undefined,
  max: undefined as number | undefined
})

// Categories
const categories = [
  {
    label: '电子产品',
    value: 'electronics',
    icon: Cellphone
  },
  {
    label: '时尚服饰',
    value: 'fashion',
    icon: Female
  },
  {
    label: '家居用品',
    value: 'home',
    icon: House
  },
  {
    label: '图书音像',
    value: 'books',
    icon: Reading
  }
]

// Get category label
const getCategoryLabel = (category: string) => {
  const cat = categories.find(c => c.value === category)
  return cat?.label || category
}

// Fetch products from backend
const fetchProducts = async () => {
  loading.value = true
  try {
    const filters: any = {
      page: currentPage.value,
      size: pageSize.value
    }

    if (selectedCategory.value) {
      filters.category = selectedCategory.value
    }

    if (availability.value !== null) {
      filters.availability = availability.value
    }

    if (priceRange.value.min !== undefined) {
      filters.min_price = priceRange.value.min
    }

    if (priceRange.value.max !== undefined) {
      filters.max_price = priceRange.value.max
    }

    const response = await productApi.getProducts(filters)
    
    // The backend returns { products: { items: [], total: 0, ... } }
    if (response.data.products) {
      products.value = response.data.products.items || []
      totalProducts.value = response.data.products.total || 0
    } else {
      products.value = []
      totalProducts.value = 0
    }

    // Client-side search filter if search query exists
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      products.value = products.value.filter(p =>
        p.name.toLowerCase().includes(query) ||
        p.description?.toLowerCase().includes(query)
      )
      totalProducts.value = products.value.length
    }

    // Client-side sorting
    if (sortBy.value === 'price_asc') {
      products.value.sort((a, b) => a.price - b.price)
    } else if (sortBy.value === 'price_desc') {
      products.value.sort((a, b) => b.price - a.price)
    } else if (sortBy.value === 'newest') {
      products.value.sort((a, b) => 
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      )
    }

  } catch (error: any) {
    console.error('Failed to fetch products:', error)
    ElMessage.error('获取商品列表失败')
    products.value = []
    totalProducts.value = 0
  } finally {
    loading.value = false
  }
}

// Select category
const selectCategory = (category: string | null) => {
  selectedCategory.value = category
  currentPage.value = 1
  fetchProducts()
}

// Search
const handleSearch = () => {
  currentPage.value = 1
  fetchProducts()
}

// Price filter
const applyPriceFilter = () => {
  if (priceRange.value.min !== undefined && priceRange.value.max !== undefined) {
    if (priceRange.value.min > priceRange.value.max) {
      ElMessage.warning('最低价不能大于最高价')
      return
    }
  }
  currentPage.value = 1
  fetchProducts()
}

// Pagination
const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchProducts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  fetchProducts()
}

// Reset filters
const resetFilters = () => {
  selectedCategory.value = null
  searchQuery.value = ''
  priceRange.value = { min: undefined, max: undefined }
  availability.value = null
  sortBy.value = 'default'
  currentPage.value = 1
  fetchProducts()
}

// Go to product detail
const goToProductDetail = (productId: number) => {
  router.push(`/products/${productId}`)
}

// Add to cart
const addToCart = async (product: Product) => {
  if (!authStore.isAuthenticated) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }

  try {
    await cartStore.addToCart({
      product_id: product.id,
      quantity: 1
    })
  } catch (error) {
    // Error already handled in store
  }
}

// Initialize from route query
onMounted(() => {
  if (route.query.category) {
    selectedCategory.value = route.query.category as string
  }
  fetchProducts()
})

// Watch route changes
watch(() => route.query.category, (newCategory) => {
  if (newCategory) {
    selectedCategory.value = newCategory as string
    fetchProducts()
  }
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Search Input Styling */
:deep(.search-input .el-input__wrapper) {
  border-radius: 12px !important;
  padding: 12px 20px !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
  border: 2px solid transparent !important;
  background: white !important;
  transition: all 0.3s ease;
}

:deep(.search-input .el-input__wrapper:hover) {
  border-color: #0ea5e9 !important;
  box-shadow: 0 4px 12px rgba(14, 165, 233, 0.15) !important;
}

:deep(.search-input .el-input__wrapper.is-focus) {
  border-color: #0ea5e9 !important;
  box-shadow: 0 4px 16px rgba(14, 165, 233, 0.2) !important;
}

:deep(.search-input .el-input__inner) {
  font-size: 15px;
}

:deep(.search-btn) {
  border-radius: 0 10px 10px 0 !important;
  padding: 0 20px !important;
  height: 100% !important;
  font-weight: 500;
  font-size: 18px;
}

/* Price Input Styling */
:deep(.price-input .el-input__wrapper) {
  border-radius: 8px !important;
  padding: 8px 12px !important;
  box-shadow: none !important;
  border: 1.5px solid #e5e7eb !important;
  transition: all 0.2s ease;
  background: white;
}

:deep(.price-input .el-input__wrapper:hover) {
  border-color: #0ea5e9 !important;
  background: #f8fafc;
}

:deep(.price-input .el-input__wrapper.is-focus) {
  border-color: #0ea5e9 !important;
  box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important;
  background: white;
}

:deep(.price-input .el-input__inner) {
  text-align: left;
  font-size: 14px;
  font-weight: 500;
}

/* Form Item Styling */
:deep(.el-form-item__label) {
  font-size: 13px;
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 4px;
}

/* Button Styling */
:deep(.el-button) {
  border-radius: 8px;
  transition: all 0.2s ease;
}

:deep(.el-button:hover) {
  transform: translateY(-1px);
}

/* Select Styling */
:deep(.sort-select) {
  width: 160px;
}

:deep(.sort-select .el-input__wrapper) {
  border-radius: 8px !important;
  border: 1.5px solid #e5e7eb !important;
  box-shadow: none !important;
  transition: all 0.2s ease;
}

:deep(.sort-select .el-input__wrapper:hover) {
  border-color: #0ea5e9 !important;
  box-shadow: 0 2px 8px rgba(14, 165, 233, 0.1) !important;
}

:deep(.sort-select .el-input__wrapper.is-focus) {
  border-color: #0ea5e9 !important;
}

/* Card Styling */
:deep(.el-card) {
  border-radius: 12px !important;
  border: 1px solid #e5e7eb !important;
}

/* Tag Styling */
:deep(.el-tag) {
  border-radius: 6px;
}
</style>
