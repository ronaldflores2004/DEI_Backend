from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.notifications.models.notification import (
    Notification
)


def get_notifications(
    current_user_id: int,
    db: Session
):

    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id
            == current_user_id
        )
        .order_by(
            Notification.created_at.desc()
        )
        .all()
    )

    return notifications


def mark_as_read(
    notification_id: int,
    current_user_id: int,
    db: Session
):

    notification = (
        db.query(Notification)
        .filter(
            Notification.id
            == notification_id
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notificación no encontrada"
        )

    if notification.user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="No tienes acceso a esta notificación"
        )

    notification.is_read = True

    db.commit()

    db.refresh(notification)

    return notification
def get_notification_summary(
    current_user_id: int,
    db: Session
):

    total = (
        db.query(Notification)
        .filter(
            Notification.user_id
            == current_user_id
        )
        .count()
    )

    unread = (
        db.query(Notification)
        .filter(
            Notification.user_id
            == current_user_id,
            Notification.is_read == False
        )
        .count()
    )

    return {
        "total": total,
        "unread": unread
    }