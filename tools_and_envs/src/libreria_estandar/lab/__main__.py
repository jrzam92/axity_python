from pathlib import Path
from libreria_estandar.lab.csv_ingestor import CSVIngestor
from libreria_estandar.lab.metrics import MetricsCalculator
from libreria_estandar.lab.json_exporter import JSONExporter
from libreria_estandar.logging_config.logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info("=" * 50)
    logger.info("🚀 INICIANDO LABORATORIO: Ingesta CSV → Métricas → JSON")
    logger.info("=" * 50)
    
    # Definir rutas
    base_path = Path(__file__).parent.parent.parent
    input_file = base_path / "data" / "input" / "sample.csv"
    output_file = base_path / "data" / "output" / "metrics.json"
    
    try:
        # 1. Ingesta de CSV
        logger.info("📂 Paso 1: Leyendo CSV...")
        ingestor = CSVIngestor(input_file)
        data = ingestor.read()
        
        # 2. Cálculo de métricas
        logger.info("🔢 Paso 2: Calculando métricas...")
        calculator = MetricsCalculator()
        metrics = calculator.calculate(data)
        
        # 3. Exportación a JSON
        logger.info("💾 Paso 3: Exportando a JSON...")
        exporter = JSONExporter(output_file)
        exporter.export(metrics)
        
        logger.info("=" * 50)
        logger.info("✅ LABORATORIO COMPLETADO EXITOSAMENTE")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"❌ ERROR FATAL: {e}")
        raise

if __name__ == "__main__":
    main()