from fastapi import HTTPException


# Failed service request
class ServiceRequestError(HTTPException):
    ...


class RequestError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)

        self.status_code: int = status_code
        self.message    : str = message

    def __str__(self):
        return f"Error {self.status_code}: {self.message}"
