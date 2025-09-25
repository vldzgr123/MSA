from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import Article
from app.schemas import ArticleCreate, ArticleUpdate
from slugify import slugify
from typing import List, Optional
import uuid


class ArticleCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_article(self, article_data: ArticleCreate) -> Article:
        """Create a new article"""
        slug = slugify(article_data.title)
        
        # Ensure slug is unique
        original_slug = slug
        counter = 1
        while self.db.query(Article).filter(Article.slug == slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        db_article = Article(
            title=article_data.title,
            description=article_data.description,
            body=article_data.body,
            tag_list=article_data.tag_list or [],
            slug=slug
        )
        
        try:
            self.db.add(db_article)
            self.db.commit()
            self.db.refresh(db_article)
            return db_article
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Article with this slug already exists")

    def get_article_by_slug(self, slug: str) -> Optional[Article]:
        """Get article by slug"""
        return self.db.query(Article).filter(Article.slug == slug).first()

    def get_articles(self, skip: int = 0, limit: int = 100) -> List[Article]:
        """Get all articles with pagination"""
        return self.db.query(Article).offset(skip).limit(limit).all()

    def get_articles_count(self) -> int:
        """Get total count of articles"""
        return self.db.query(Article).count()

    def update_article(self, slug: str, article_data: ArticleUpdate) -> Optional[Article]:
        """Update article by slug"""
        db_article = self.get_article_by_slug(slug)
        if not db_article:
            return None
        
        # Update fields if provided
        if article_data.title is not None:
            db_article.title = article_data.title
            # Generate new slug if title changed
            new_slug = slugify(article_data.title)
            if new_slug != slug:
                # Check if new slug is unique
                original_slug = new_slug
                counter = 1
                while self.db.query(Article).filter(Article.slug == new_slug).first():
                    new_slug = f"{original_slug}-{counter}"
                    counter += 1
                db_article.slug = new_slug
        
        if article_data.description is not None:
            db_article.description = article_data.description
        
        if article_data.body is not None:
            db_article.body = article_data.body
        
        if article_data.tag_list is not None:
            db_article.tag_list = article_data.tag_list
        
        try:
            self.db.commit()
            self.db.refresh(db_article)
            return db_article
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Article with this slug already exists")

    def delete_article(self, slug: str) -> bool:
        """Delete article by slug"""
        db_article = self.get_article_by_slug(slug)
        if not db_article:
            return False
        
        self.db.delete(db_article)
        self.db.commit()
        return True
