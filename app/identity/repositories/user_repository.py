from sqlalchemy.orm import Session

from app.identity.models.user import User


class UserRepository:
    """
    Repositorio encargado del acceso a datos
    de la entidad User.
    """

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def exists_email(
        db: Session,
        email: str
    ) -> bool:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
            is not None
        )

    @staticmethod
    def create(
        db: Session,
        user: User
    ) -> User:

        db.add(user)

        db.commit()

        db.refresh(user)

        return user

    @staticmethod
    def get_all(
        db: Session
    ) -> list[User]:

        return (
            db.query(User)
            .order_by(User.email)
            .all()
        )

    @staticmethod
    def count_all(
        db: Session
    ) -> int:

        return (
            db.query(User)
            .count()
        )

    @staticmethod
    def count_active(
        db: Session
    ) -> int:

        return (
            db.query(User)
            .filter(
                User.is_active == True
            )
            .count()
        )

    @staticmethod
    def count_inactive(
        db: Session
    ) -> int:

        return (
            db.query(User)
            .filter(
                User.is_active == False
            )
            .count()
        )

    @staticmethod
    def count_active_admins(
        db: Session
    ) -> int:

        return (
            db.query(User)
            .filter(
                User.role == "ADMIN",
                User.is_active == True
            )
            .count()
        )

    @staticmethod
    def update(
        db: Session,
        user: User
    ) -> User:

        db.commit()

        db.refresh(user)

        return user