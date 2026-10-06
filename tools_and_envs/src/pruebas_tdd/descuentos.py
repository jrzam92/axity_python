def servicio_email_externo(email: str, mensaje: str) -> bool:
    # Esta función simularía conectarse a un servidor real como AWS SES.
    # Por eso la mockeamos en los tests.
    pass

def notificar_cliente(email: str, mensaje: str) -> bool:
    return servicio_email_externo(email, mensaje)

def calcular_total(carrito: list[dict], es_vip: bool = False) -> float:
    total_base = sum(item["precio"] for item in carrito)
    descuento = 0.0
    
    if len(carrito) > 3:
        descuento += 0.10  # 10% por volumen
        
    if es_vip:
        descuento += 0.05  # 5% extra por VIP
        
    total_final = total_base * (1 - descuento)
    return round(total_final, 2)