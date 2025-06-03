from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    text: str
    category_id: Optional[int]  # теперь можно указать категорию


class QuestionResponse(BaseModel):
    id: int
    text: str
    category: Optional[CategoryBase]  # возвращаем вложенную категорию

    class Config:
        orm_mode = True


class MessageResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True
