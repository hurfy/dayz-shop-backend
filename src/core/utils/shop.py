HTTP_RESPONSES = {
    404: {
        "description": "Object not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Object with ID ... not found"
                }
            }
        }
    },
}
