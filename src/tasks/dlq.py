"""Dead Letter Queue consumer for failed tasks"""
import logging
from typing import Dict, Any, Optional, Callable
from uuid import UUID

from src.config import settings
from src.models.database import Article, SessionLocal as BackendSession
from src.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


def _compensate_moderate(article: Article, post_id: str) -> None:
    """Compensate moderation failure: rollback to DRAFT"""
    logger.info("Compensating moderation failure: rolling back article %s status to DRAFT", post_id)
    article.status = "DRAFT"
    logger.info("Article %s status rolled back to DRAFT, can be republished", post_id)


def _compensate_preview(article: Article, post_id: str) -> None:
    """Compensate preview generation failure: remove preview_url"""
    logger.info("Compensating preview failure: removing preview_url for article %s", post_id)
    article.preview_url = None
    logger.info("Preview URL removed for article %s, status remains: %s", post_id, article.status)


def _compensate_publish(article: Article, post_id: str) -> None:
    """Compensate publication failure: mark as ERROR (critical)"""
    logger.info("Compensating publication failure: marking article %s as ERROR", post_id)
    article.status = "ERROR"


def _compensate_notify(article: Article, post_id: str) -> None:
    """Compensate notification failure: no action needed (non-critical)"""
    logger.warning("Notification failed for published article %s, no compensation needed", post_id)


def _compensate_default(article: Article, post_id: str) -> None:
    """Default compensation: mark as ERROR (general compensation)"""
    logger.warning("Unknown task type for DLQ, applying general compensation (ERROR) for article %s", post_id)
    article.status = "ERROR"


# Compensation rules: task name pattern -> compensation function
COMPENSATION_RULES: Dict[str, Callable[[Article, str], None]] = {
    "moderate": _compensate_moderate,
    "preview": _compensate_preview,
    "publish": _compensate_publish,
    "notify": _compensate_notify,
}


def _apply_compensation(task_name: str, article: Article, post_id: str) -> bool:
    """
    Apply compensation based on task type.
    Returns True if compensation was applied, False if no action needed.
    """
    task_name_lower = task_name.lower()
    
    # Find matching compensation rule
    compensation_func: Optional[Callable[[Article, str], None]] = None
    
    for pattern, func in COMPENSATION_RULES.items():
        if pattern in task_name_lower:
            compensation_func = func
            break
    
    # Apply compensation
    if compensation_func:
        compensation_func(article, post_id)
        return True
    else:
        # Default compensation for unknown task types
        _compensate_default(article, post_id)
        return True


@celery_app.task(
    name="src.tasks.dlq.handle_failed_task",
    bind=True,
    max_retries=1,  # DLQ handler should not retry much
)
def handle_failed_task(self, task_name: str, task_data: Dict[str, Any], error: str):
    """
    Handle failed task from DLQ.
    Performs compensating actions based on task type.
    """
    logger.error("Processing failed task from DLQ: %s, error: %s", task_name, error)
    
    backend_session = BackendSession()
    
    try:
        # Extract post_id from task data
        post_id = task_data.get("post_id") or task_data.get("article_id")
        if not post_id:
            logger.error("No post_id found in failed task data: %s", task_data)
            return
        
        post_uuid = UUID(post_id)
        
        # Get article
        article = backend_session.query(Article).filter(Article.id == post_uuid).first()
        if not article:
            logger.warning("Article %s not found for DLQ compensation", post_id)
            return
        
        # Perform compensation based on task type using unified logic
        compensation_applied = _apply_compensation(task_name, article, post_id)
        
        # Commit changes if compensation was applied (and requires DB update)
        if compensation_applied and task_name.lower() not in ["notify"]:
            backend_session.commit()
    
    except Exception as exc:
        logger.error("Error in DLQ handler: %s", exc)
        raise
    finally:
        backend_session.close()


def enqueue_dlq_task(task_name: str, task_data: Dict[str, Any], error: str):
    """Helper to enqueue task to DLQ"""
    handle_failed_task.apply_async(
        kwargs={
            "task_name": task_name,
            "task_data": task_data,
            "error": str(error)
        },
        queue=settings.dlq_queue
    )

