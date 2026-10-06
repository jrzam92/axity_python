import httpx

def descargar_archivo_streaming(url: str, destino: str):
    """Descarga archivos grandes sin cargar todo en RAM"""
    print(f"📥 Iniciando descarga desde {url}...")
    
    with httpx.stream("GET", url, timeout=30.0) as response:
        response.raise_for_status()
        
        total_bytes = 0
        with open(destino, "wb") as f:
            for chunk in response.iter_bytes(chunk_size=8192):
                f.write(chunk)
                total_bytes += len(chunk)
        
        print(f"✅ Descargado: {destino} ({total_bytes} bytes)")