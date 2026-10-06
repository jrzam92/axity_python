from pathlib import Path
from typing import List, Dict
from libreria_estandar.data_processing.csv_handler import CSVHandler
from libreria_estandar.logging_config.logger import get_logger

logger = get_logger(__name__)

class CSVIngestor:
    """Ingesta de archivos CSV"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data: List[Dict] = []
    
    def read(self) -> List[Dict]:
        """Lee el CSV y retorna los datos"""
        try:
            self.data = CSVHandler.read(self.file_path)
            logger.info(f"✅ CSV leído: {len(self.data)} registros desde {self.file_path.name}")
            logger.debug(f"Columnas encontradas: {list(self.data[0].keys()) if self.data else []}")
            return self.data
        except FileNotFoundError:
            logger.error(f"❌ Archivo no encontrado: {self.file_path}")
            raise
        except Exception as e:
            logger.error(f"❌ Error leyendo CSV: {e}")
            raise