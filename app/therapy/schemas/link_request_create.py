from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.shared.enums.sharing_mode_enum import (
    SharingModeEnum
)


class LinkRequestCreate(BaseModel):

    professional_id: int = Field(gt=0)

    # Por defecto el profesional solo ve las
    # entradas creadas desde que se acepta el vínculo.
    sharing_mode: SharingModeEnum = SharingModeEnum.NEW_ONLY

    # Obligatorio con FROM_DATE.
    share_from: datetime | None = None

    @model_validator(mode="after")
    def validate_share_from(self):

        if self.sharing_mode == SharingModeEnum.FROM_DATE:

            if not self.share_from:
                raise ValueError(
                    "share_from es obligatorio con FROM_DATE"
                )

            if self.share_from > datetime.utcnow():
                raise ValueError(
                    "share_from no puede ser una fecha futura"
                )

        elif self.share_from:
            raise ValueError(
                "share_from solo se usa con FROM_DATE"
            )

        return self
