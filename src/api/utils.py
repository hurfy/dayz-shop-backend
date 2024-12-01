from inflection import camelize

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


def to_camelcase(data: str) -> str:
    """Alias generator for pydantic schemas"""
    return camelize(data, uppercase_first_letter=False)

