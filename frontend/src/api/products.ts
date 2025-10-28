import request from './axios'
import type { Product, ProductCreate, ProductFilter, PaginatedResponse } from '@/types'

export const productApi = {
  // Get all products with filters
  getProducts(filters?: ProductFilter) {
    return request.get<{ products: PaginatedResponse<Product> }>('/products/', {
      params: filters
    })
  },

  // Get product by ID
  getProduct(id: number) {
    return request.get<Product>(`/products/${id}`)
  },

  // Create product (vendor/admin only)
  createProduct(data: ProductCreate) {
    return request.post<Product>('/products/', data)
  },

  // Update product
  updateProduct(id: number, data: Partial<ProductCreate>) {
    return request.put<Product>(`/products/${id}`, data)
  },

  // Delete product
  deleteProduct(id: number) {
    return request.delete(`/products/${id}`)
  }
}

