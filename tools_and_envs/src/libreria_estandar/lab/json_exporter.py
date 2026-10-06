from pathlib import Path
from typing import Dict, Any
from libreria_estandar.data_processing.json_handler import JSONHandler
from libreria_estandar.time_utils.datetime_handler import DateTimeHandler
from libreria_estandar.logging_config.logger import get_logger

logger = get_logger(__name__)

class JSONExporter:
    """Exporta datos a JSON"""
    
    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def export(self, data: Dict[str, Any]) -> None:
        """Exporta datos con timestamp"""
        try:
            output = {
                "timestamp": DateTimeHandler.format_iso(DateTimeHandler.now_utc()),
                "metrics": data
            }
            
            JSONHandler.write(self.output_path, output)
            logger.info(f"💾 JSON exportado a: {self.output_path}")
        except Exception as e:
            logger.error(f"❌ Error exportando JSON: {e}")
            raise