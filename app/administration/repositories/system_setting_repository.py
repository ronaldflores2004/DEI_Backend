from sqlalchemy.orm import Session

from app.administration.models.system_setting import (
    SystemSetting
)


class SystemSettingRepository:
    """
    Repositorio para el acceso a datos de
    SystemSetting.
    """

    @staticmethod
    def get(
        db: Session,
        key: str,
    ) -> SystemSetting | None:

        return db.get(SystemSetting, key)

    @staticmethod
    def set(
        db: Session,
        key: str,
        value: str,
        user_id: int | None,
    ) -> SystemSetting:

        setting = db.get(SystemSetting, key)

        if setting:
            setting.value = value
            setting.updated_by_user_id = user_id

        else:
            setting = SystemSetting(
                key=key,
                value=value,
                updated_by_user_id=user_id
            )
            db.add(setting)

        db.commit()
        db.refresh(setting)

        return setting

    @staticmethod
    def delete(
        db: Session,
        key: str,
    ) -> None:

        setting = db.get(SystemSetting, key)

        if setting:
            db.delete(setting)
            db.commit()
