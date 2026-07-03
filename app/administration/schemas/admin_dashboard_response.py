from pydantic import BaseModel


class AdminDashboardResponse(BaseModel):

    total_users: int

    total_patients: int

    total_professionals: int

    verified_professionals: int

    pending_professionals: int

    total_entries: int

    total_analyses: int

    total_sessions: int