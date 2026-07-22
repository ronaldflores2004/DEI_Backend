from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.notifications.repositories.notification_repository import (
    NotificationRepository
)



class NotificationService:
    
    @staticmethod
    def get_notifications(
        current_user_id: int,
        db: Session
    ):

        return (
            NotificationRepository.get_by_user(
                db=db,
                user_id=current_user_id
            )
        )


    @staticmethod
    def mark_as_read(
        notification_id: int,
        current_user_id: int,
        db: Session
    ):

        notification = (
            NotificationRepository.get_by_id(
                db=db,
                notification_id=notification_id
            )
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

        return (
            NotificationRepository.update(
                db=db,
                notification=notification
            )
        )

    @staticmethod
    def get_notification_summary(
        current_user_id: int,
        db: Session
    ):

        total = (
            NotificationRepository.count_by_user(
                db=db,
                user_id=current_user_id
            )
        )

        unread = (
            NotificationRepository.count_unread(
                db=db,
                user_id=current_user_id
            )
        )

        return {

            "total":
                total,

            "unread":
                unread
        }