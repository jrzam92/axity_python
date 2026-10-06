import logging
from pathlib import Path

def get_logger(name: str, log_level: int = logging.DEBUG) -> logging.Logger:
    """Configura y retorna un logger estructurado"""
    
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(log_level)
        
        # Crear directorio de logs
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Handler para archivo (DEBUG y superior)
        file_handler = logging.FileHandler(log_dir / "app.log", encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Handler para consola (INFO y superior)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formato estructurado
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger