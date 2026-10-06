from datetime import datetime, timezone
from zoneinfo import ZoneInfo

class DateTimeHandler:
    """Manejo de fechas y zonas horarias"""
    
    @staticmethod
    def now_utc() -> datetime:
        """Retorna datetime actual en UTC"""
        return datetime.now(timezone.utc)
    
    @staticmethod
    def now_local(tz: str = "America/Mexico_City") -> datetime:
        """Retorna datetime en zona horaria específica"""
        return datetime.now(ZoneInfo(tz))
    
    @staticmethod
    def format_iso(dt: datetime) -> str:
        """Formatea datetime a ISO 8601"""
        return dt.isoformat()
    
    @staticmethod
    def parse_iso(date_string: str) -> datetime:
        """Parsea string ISO a datetime"""
        return datetime.fromisoformat(date_string)