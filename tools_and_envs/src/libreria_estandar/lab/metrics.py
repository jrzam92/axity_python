from typing import List, Dict, Any
from libreria_estandar.logging_config.logger import get_logger

logger = get_logger(__name__)

class MetricsCalculator:
    """Calcula métricas de datasets"""
    
    @staticmethod
    def calculate(data: List[Dict]) -> Dict[str, Any]:
        """Calcula métricas básicas"""
        logger.debug("Calculando métricas del dataset...")
        
        if not data:
            logger.warning("⚠️ Dataset vacío")
            return {"total_records": 0, "columns": [], "sample": []}
        
        metrics = {
            "total_records": len(data),
            "columns": list(data[0].keys()),
            "column_count": len(data[0].keys()),
            "sample": data[:3]
        }
        
        logger.info(f"📊 Métricas calculadas: {metrics['total_records']} registros, {metrics['column_count']} columnas")
        return metrics