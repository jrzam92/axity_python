import yaml
from pathlib import Path
from typing import Any, Dict

class YAMLHandler:
    """Manejo de archivos YAML"""
    
    @staticmethod
    def read(file_path: Path) -> Dict:
        """Lee archivo YAML"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def write(file_path: Path, data: Any) -> None:
        """Escribe archivo YAML"""
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)