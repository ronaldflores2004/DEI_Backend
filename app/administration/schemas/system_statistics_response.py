from pydantic import BaseModel


class SystemStatisticsResponse(BaseModel):

    active_users: int

    inactive_users: int

    archived_entries: int

    generated_recommendations: int

    notifications_sent: int