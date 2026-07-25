from pydantic import BaseModel, Field

from app.shared.enums.entry_type_enum import EntryTypeEnum


class EmotionalEntryCreate(BaseModel):

    entry_type: EntryTypeEnum

    text_content: str | None = Field(default=None, min_length=1, max_length=10000)