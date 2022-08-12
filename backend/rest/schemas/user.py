from typing import Optional
from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    name: str
    username: Optional[str]
    is_admin: bool

    class Config:
        orm_mode = True