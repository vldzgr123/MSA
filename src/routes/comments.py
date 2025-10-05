from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from src.models.database import get_db
from src.models.schemas import CommentCreate, CommentResponse, CommentListResponse, SuccessResponse, ErrorResponse
from src.controllers.crud import CommentCRUD, ArticleCRUD
from src.middleware.auth import get_current_user
from src.models.database import User

router = APIRouter()


@router.post("/{slug}/comments", response_model=SuccessResponse)
async def create_comment(
    slug: str,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a comment to an article"""
    try:
        # Get article by slug
        article_crud = ArticleCRUD(db)
        article = article_crud.get_article_by_slug(slug)
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Create comment
        comment_crud = CommentCRUD(db)
        comment = comment_crud.create_comment(
            comment_data=comment_data,
            article_id=article.id,
            author_id=current_user.id
        )
        
        return SuccessResponse(
            message="Comment created successfully",
            data={"comment": CommentResponse.from_orm(comment)}
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create comment"
        )


@router.get("/{slug}/comments", response_model=SuccessResponse)
async def get_comments(
    slug: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all comments for an article"""
    try:
        # Get article by slug
        article_crud = ArticleCRUD(db)
        article = article_crud.get_article_by_slug(slug)
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Get comments
        comment_crud = CommentCRUD(db)
        comments = comment_crud.get_comments_by_article(
            article_id=article.id,
            skip=skip,
            limit=limit
        )
        count = comment_crud.get_comments_count_by_article(article.id)
        
        return SuccessResponse(
            message="Comments retrieved successfully",
            data={
                "comments": [CommentResponse.from_orm(comment) for comment in comments],
                "count": count
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve comments"
        )


@router.delete("/{slug}/comments/{comment_id}", response_model=SuccessResponse)
async def delete_comment(
    slug: str,
    comment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a comment (only by author)"""
    try:
        # Get article by slug
        article_crud = ArticleCRUD(db)
        article = article_crud.get_article_by_slug(slug)
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        # Delete comment
        comment_crud = CommentCRUD(db)
        success = comment_crud.delete_comment(
            comment_id=comment_id,
            user_id=current_user.id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        
        return SuccessResponse(
            message="Comment deleted successfully"
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete comment"
        )
