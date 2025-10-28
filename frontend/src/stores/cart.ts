import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { cartApi } from '@/api/cart'
import type { CartItem, CartItemCreate } from '@/types'
import { ElMessage } from 'element-plus'

export const useCartStore = defineStore('cart', () => {
  const cartItems = ref<CartItem[]>([])
  const loading = ref(false)

  const totalItems = computed(() => {
    return cartItems.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  const totalPrice = computed(() => {
    return cartItems.value.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  })

  // Fetch cart items
  async function fetchCartItems() {
    loading.value = true
    try {
      const response = await cartApi.getCartItems()
      cartItems.value = response.data
    } catch (error) {
      console.error('Failed to fetch cart items:', error)
    } finally {
      loading.value = false
    }
  }

  // Add to cart
  async function addToCart(data: CartItemCreate) {
    loading.value = true
    try {
      await cartApi.addToCart(data)
      await fetchCartItems()
      ElMessage.success('已添加到购物车')
    } catch (error: any) {
      const message = error.response?.data?.detail || '添加失败'
      ElMessage.error(message)
      throw error
    } finally {
      loading.value = false
    }
  }

  // Update cart item
  async function updateCartItem(id: number, quantity: number) {
    loading.value = true
    try {
      await cartApi.updateCartItem(id, { quantity })
      await fetchCartItems()
      ElMessage.success('已更新')
    } catch (error: any) {
      const message = error.response?.data?.detail || '更新失败'
      ElMessage.error(message)
      throw error
    } finally {
      loading.value = false
    }
  }

  // Remove from cart
  async function removeFromCart(id: number) {
    loading.value = true
    try {
      await cartApi.removeFromCart(id)
      await fetchCartItems()
      ElMessage.success('已移除')
    } catch (error: any) {
      const message = error.response?.data?.detail || '移除失败'
      ElMessage.error(message)
      throw error
    } finally {
      loading.value = false
    }
  }

  // Clear cart
  function clearCart() {
    cartItems.value = []
  }

  return {
    cartItems,
    loading,
    totalItems,
    totalPrice,
    fetchCartItems,
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart
  }
})

