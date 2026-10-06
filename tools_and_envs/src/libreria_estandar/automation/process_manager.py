import subprocess
from typing import Tuple

class ProcessManager:
    """Ejecuta comandos del sistema con subprocess"""
    
    @staticmethod
    def run_command(command: str) -> Tuple[str, str, int]:
        """
        Ejecuta comando y retorna (stdout, stderr, return_code)
        """
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        
        return result.stdout, result.stderr, result.returncode
    
    @staticmethod
    def run_python_script(script_path: str) -> Tuple[str, str, int]:
        """Ejecuta un script de Python"""
        return ProcessManager.run_command(f"python {script_path}")