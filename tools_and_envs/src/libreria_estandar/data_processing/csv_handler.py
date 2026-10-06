import csv
from pathlib import Path
from typing import List, Dict

class CSVHandler:
    """Manejo de archivos CSV"""
    
    @staticmethod
    def read(file_path: Path) -> List[Dict]:
        """Lee CSV y retorna lista de diccionarios"""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    @staticmethod
    def write(file_path: Path, data: List[Dict], fieldnames: List[str]) -> None:
        """Escribe CSV desde lista de diccionarios"""
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)