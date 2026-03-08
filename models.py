from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Announcement:
    id: int
    symbol: str
    name: str
    file_text: str
    path: str
    uploaded_date: str
    manual_date: int
    logo_url: str = ""

    @property
    def pdf_filename(self) -> str:
        return f"{self.symbol}_{self.id}.pdf"

    @property
    def is_annual_report(self) -> bool:
        return "annual report" in self.file_text.lower()

    @property
    def period_description(self) -> str:
        return self.file_text

    @classmethod
    def from_api(cls, data: dict) -> "Announcement":
        return cls(
            id=data["id"],
            symbol=data["symbol"],
            name=data["name"],
            file_text=data["fileText"],
            path=data["path"],
            uploaded_date=data.get("uploadedDate", ""),
            manual_date=data.get("manualDate", 0),
            logo_url=data.get("logoUrl", ""),
        )


@dataclass
class AnalysisResult:
    symbol: str
    company_name: str
    period: str
    analysis_text: str
    generated_at: datetime = field(default_factory=datetime.now)
