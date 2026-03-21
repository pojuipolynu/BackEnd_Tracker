from pydantic import BaseModel

class BaseSchema(BaseModel):
    message: str