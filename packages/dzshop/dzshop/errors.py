from fastapi import HTTPException


# Failed service request
class ServiceRequestError(HTTPException):
    ...
