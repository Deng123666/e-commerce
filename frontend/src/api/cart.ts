import request from './axios'
import type { CartItem, CartItemCreate } from '@/types'

export const cartApi = {
  // Get all cart items
  getCartItems() {
    return request.get<CartItem[]>('/cart_items/')
  },

  // Get cart item by ID
  getCartItem(id: number) {
    return request.get<CartItem>(`/cart_items/${id}`)
  },

  // Add item to cart
  addToCart(data: CartItemCreate) {
    return request.post<CartItem>('/cart_items/', data)
  },

  // Update cart item
  updateCartItem(id: number, data: { quantity: number }) {
    return request.patch<CartItem>(`/cart_items/${id}`, data)
  },

  // Remove item from cart
  removeFromCart(id: number) {
    return request.delete(`/cart_items/${id}`)
  }
}

