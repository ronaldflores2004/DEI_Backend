from sqlalchemy.orm import Session

from app.notifications.models.notification import (
    Notification,
)


class NotificationRepository:
    """
    Repositorio para el acceso a datos de
    Notification.
    """

    @staticmethod
    def get_by_id(
        db: Session,
        notification_id: int,
    ) -> Notification | None:

        return (
            db.query(Notification)
            .filter(
                Notification.id == notification_id
            )
            .first()
        )

    @staticmethod
    def get_by_user(
        db: Session,
        user_id: int,
    ) -> list[Notification]:

        return (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id
            )
            .order_by(
                Notification.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def count_by_user(
        db: Session,
        user_id: int,
    ) -> int:

        return (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id
            )
            .count()
        )

    @staticmethod
    def count_unread(
        db: Session,
        user_id: int,
    ) -> int:

        return (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_read.is_(False),
            )
            .count()
        )

    @staticmethod
    def create(
        db: Session,
        notification: Notification,
    ) -> Notification:

        db.add(notification)

        db.commit()

        db.refresh(notification)

        return notification

    @staticmethod
    def update(
        db: Session,
        notification: Notification,
    ) -> Notification:

        db.commit()

        db.refresh(notification)

        return notification
    
    @staticmethod
    def count_all(
        db: Session,
    ) -> int:

        return (
            db.query(Notification)
            .count()
        )