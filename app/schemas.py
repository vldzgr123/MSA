from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Article title")
    description: str = Field(..., min_length=1, max_length=500, description="Article description")
    body: str = Field(..., min_length=1, description="Article body content")
    tag_list: Optional[List[str]] = Field(default=[], description="List of tags")

    @validator('tag_list')
    def validate_tags(cls, v):
        if v is not None:
            for tag in v:
                if not isinstance(tag, str) or not tag.strip():
                    raise ValueError('All tags must be non-empty strings')
        return v


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    body: Optional[str] = Field(None, min_length=1)
    tag_list: Optional[List[str]] = Field(None)

    @validator('tag_list')
    def validate_tags(cls, v):
        if v is not None:
            for tag in v:
                if not isinstance(tag, str) or not tag.strip():
                    raise ValueError('All tags must be non-empty strings')
        return v


class ArticleResponse(ArticleBase):
    id: UUID
    slug: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    articles: List[ArticleResponse]
    count: int


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: Optional[List[dict]] = None


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None
