from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import (
    ArticleCreate, 
    ArticleUpdate, 
    ArticleResponse, 
    ArticleListResponse,
    SuccessResponse,
    ErrorResponse
)
from app.crud import ArticleCRUD

router = APIRouter(prefix="/api/articles", tags=["articles"])


@router.post("/", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_article(
    article_data: ArticleCreate,
    db: Session = Depends(get_db)
):
    """Create a new article"""
    try:
        crud = ArticleCRUD(db)
        db_article = crud.create_article(article_data)
        
        return SuccessResponse(
            message="Article created successfully",
            data={
                "article": ArticleResponse.from_orm(db_article).dict(),
                "slug": db_article.slug
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=SuccessResponse)
def get_articles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all articles with pagination"""
    try:
        crud = ArticleCRUD(db)
        articles = crud.get_articles(skip=skip, limit=limit)
        count = crud.get_articles_count()
        
        articles_data = [ArticleResponse.from_orm(article).dict() for article in articles]
        
        return SuccessResponse(
            message="Articles retrieved successfully",
            data={
                "articles": articles_data,
                "count": count
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{slug}", response_model=SuccessResponse)
def get_article_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get article by slug"""
    try:
        crud = ArticleCRUD(db)
        article = crud.get_article_by_slug(slug)
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        return SuccessResponse(
            message="Article retrieved successfully",
            data={
                "article": ArticleResponse.from_orm(article).dict()
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{slug}", response_model=SuccessResponse)
def update_article(
    slug: str,
    article_data: ArticleUpdate,
    db: Session = Depends(get_db)
):
    """Update article by slug"""
    try:
        crud = ArticleCRUD(db)
        updated_article = crud.update_article(slug, article_data)
        
        if not updated_article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        return SuccessResponse(
            message="Article updated successfully",
            data={
                "article": ArticleResponse.from_orm(updated_article).dict()
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{slug}", response_model=SuccessResponse)
def delete_article(
    slug: str,
    db: Session = Depends(get_db)
):
    """Delete article by slug"""
    try:
        crud = ArticleCRUD(db)
        deleted = crud.delete_article(slug)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        return SuccessResponse(
            message="Article deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
