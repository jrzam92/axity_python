from pathlib import Path

class FileOperations:
    """Operaciones básicas de archivos"""
    
    @staticmethod
    def read_text(file_path: Path) -> str:
        """Lee archivo de texto"""
        return file_path.read_text(encoding='utf-8')
    
    @staticmethod
    def write_text(file_path: Path, content: str) -> None:
        """Escribe archivo de texto"""
        file_path.write_text(content, encoding='utf-8')
    
    @staticmethod
    def file_exists(file_path: Path) -> bool:
        """Verifica si archivo existe"""
        return file_path.exists() and file_path.is_file()