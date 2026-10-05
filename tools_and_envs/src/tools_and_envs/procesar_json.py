import json


def procesar_datos_usuarios(ruta_archivo: str):
    # 1. Colecciones que usaremos (Listas y Diccionarios)
    usuarios_activos = []
    conteo_roles = {"admin": 0, "usuario": 0, "invitado": 0, "desconocido": 0}

    # 2. Manejo de Errores Robusto (try-except)
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        # 3. Control de flujo (for, if)
        for usuario in datos:
            # Filtramos solo los activos
            if usuario.get("activo"):
                usuarios_activos.append(usuario["nombre"])

            # 4. Pattern Matching (Novedad de Python 3.10+)
            # Evaluamos el rol del usuario para agregarlo a nuestras estadísticas
            match usuario.get("rol"):
                case "admin":
                    conteo_roles["admin"] += 1
                case "usuario":
                    conteo_roles["usuario"] += 1
                case "invitado":
                    conteo_roles["invitado"] += 1
                case _:
                    # El '_' actúa como un 'default' (si no coincide con nada de arriba)
                    conteo_roles["desconocido"] += 1

        # Mostramos los resultados
        print("📊 Resumen de datos:")
        print(f"Usuarios activos ({len(usuarios_activos)}): {usuarios_activos}")
        print(f"Distribución de roles: {conteo_roles}")

    # Captura si el archivo no existe
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{ruta_archivo}'. Verifica la ruta.")

    # Captura si el archivo existe pero el JSON está mal escrito
    except json.JSONDecodeError as e:
        print(f"❌ Error de formato: El archivo no es un JSON válido. Detalle: {e}")

    # Captura cualquier otro error inesperado (Control de excepciones general)
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")


# Ejecutamos la función
if __name__ == "__main__":
    procesar_datos_usuarios("datos.json")
