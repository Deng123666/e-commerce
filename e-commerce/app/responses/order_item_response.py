from app.responses.common import default_responses, status


order_item_responses = {
  **default_responses,
  status.HTTP_201_CREATED: {
    "description": "Order item created successfully",
    "content": {
      "application/json": {
        "example": {
          "id": 1,
          "user_id": 1,
          "cart_item_id": 1,
          "status": "paid",
          "created_at": "2025-01-01T14:00",
          "updated_at": "2025-04-04T16:40"
        }
      }
    }
  },
  status.HTTP_400_BAD_REQUEST: {
    "description": "Bad request, invalid input data",
    "content": {
      "application/json": {
        "example": {
          "error": "Invalid data",
          "message": "The provided order data is not valid"
        }
      }
    }
  },
  status.HTTP_200_OK: {
    "description": "Success - Order created with order items",
    "content": {
      "application/json": {
        "example": {
          "order_id": 123,
          "total_amount": 299.99,
          "order_status": "pending",
          "order_items": [
            {
              "id": 1,
              "order_id": 123,
              "product_id": 10,
              "quantity": 2,
              "price": 149.99
            },
            {
              "id": 2,
              "order_id": 123,
              "product_id": 15,
              "quantity": 1,
              "price": 149.99
            }
          ]
        }
      }
    }
  },
  status.HTTP_404_NOT_FOUND: {
    "description": "Order is not found",
    "content": {
      "application/json": {
        "example": {
          "error": "Not found",
          "message": "Order is not found"
        }
      }
    }
  },
  status.HTTP_401_UNAUTHORIZED: {
    "description": "User is unauthorized",
    "content": {
      "application/json": {
        "example": {
          "error": "Unauthorized",
          "message": "You must provide a valid API key to access this resource."
        }
      }
    }
  }
}