from sqlalchemy.orm import Session

from app.administration.models.crisis_line import (
    CrisisLine
)


class CrisisLineRepository:
    """
    Repositorio para el acceso a datos de
    CrisisLine.
    """

    @staticmethod
    def get_by_id(
        db: Session,
        line_id: int,
    ) -> CrisisLine | None:

        return (
            db.query(CrisisLine)
            .filter(CrisisLine.id == line_id)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        country_code: str | None = None,
        only_active: bool = False,
    ) -> list[CrisisLine]:

        query = db.query(CrisisLine)

        if country_code:
            query = query.filter(
                CrisisLine.country_code == country_code.upper()
            )

        if only_active:
            query = query.filter(
                CrisisLine.is_active.is_(True)
            )

        return (
            query
            .order_by(
                CrisisLine.country_code,
                CrisisLine.sort_order,
                CrisisLine.id
            )
            .all()
        )

    @staticmethod
    def save(
        db: Session,
        line: CrisisLine,
    ) -> CrisisLine:

        db.add(line)
        db.commit()
        db.refresh(line)

        return line
