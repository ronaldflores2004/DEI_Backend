from pydantic import BaseModel

from app.shared.enums.entry_type_enum import EntryTypeEnum


class EmotionalEntryCreate(BaseModel):

    entry_type: EntryTypeEnum

    text_content: str | None = None