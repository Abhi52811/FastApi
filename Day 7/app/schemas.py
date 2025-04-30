from datetime import datetime
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_At: datetime

    # The Config inner class in a Pydantic model lets you customize how the model behaves.
    class Config:
        # This tell->"this model might receive data from an ORM model (like SQLAlchemy) — not a dict. So access fields using obj.field instead of dict['field'].”
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str 

class UserOut(BaseModel):
    id: int 
    email: EmailStr
    created_At: datetime
    class Config:
        orm_mode = True