import json
from pathlib import Path
from typing import Any, Dict

class JSONHandler:
    """Manejo de archivos JSON"""
    
    @staticmethod
    def read(file_path: Path) -> Dict:
        """Lee archivo JSON"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def write(file_path: Path, data: Any, indent: int = 2) -> None:
        """Escribe archivo JSON"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)