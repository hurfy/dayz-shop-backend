from inflection import camelize


def to_camelcase(data: str) -> str:
    """Alias generator for pydantic schemas"""
    return camelize(data, uppercase_first_letter=False)