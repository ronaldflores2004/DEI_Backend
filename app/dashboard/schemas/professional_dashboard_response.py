from pydantic import BaseModel


class ProfessionalDashboardResponse(BaseModel):

    active_patients: int

    patients_with_risk: int

    pending_link_requests: int

    total_insights: int