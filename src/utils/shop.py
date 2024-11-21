PRODUCT_RESPONSES = {
    404: {
        "description": "Product not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Product with ID 42 not found"
                }
            }
        }
    },
}