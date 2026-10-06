from pathlib import Path
from typing import List

class PathManager:
    """Manejo seguro de rutas con pathlib"""
    
    @staticmethod
    def ensure_directory(path: Path) -> Path:
        """Crea directorio si no existe"""
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def list_files(directory: Path, pattern: str = "*") -> List[Path]:
        """Lista archivos en un directorio"""
        return list(directory.glob(pattern))
    
    @staticmethod
    def safe_path(base: Path, *parts: str) -> Path:
        """Crea una ruta segura"""
        return base.joinpath(*parts).resolve()