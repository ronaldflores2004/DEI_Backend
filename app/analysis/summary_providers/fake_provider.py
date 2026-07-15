from app.analysis.summary_providers.base_provider import (
    BaseSummaryProvider
)


class FakeSummaryProvider(
    BaseSummaryProvider
):

    def generate(
        self,
        dominant_emotion: str,
        latest_emotion: str,
        risk_level: str,
        topics: list,
        triggers: list,
    ) -> str:

        return (
            f"Durante esta semana predominó "
            f"{dominant_emotion}. "
            f"Tu emoción más reciente fue "
            f"{latest_emotion}."
        )