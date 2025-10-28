import request from './axios'
import type { Order } from '@/types'

export const orderApi = {
  // Get all orders
  getOrders() {
    return request.get<Order[]>('/orders/')
  },

  // Get order by ID
  getOrder(id: number) {
    return request.get<Order>(`/orders/${id}`)
  },

  // Get orders by status
  getOrdersByStatus(status: string) {
    return request.get<Order[]>(`/orders/status/${status}`)
  },

  // Cancel order
  cancelOrder(id: number) {
    return request.patch(`/orders/cancel/${id}`)
  }
}

