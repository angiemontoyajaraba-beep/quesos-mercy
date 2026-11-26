# ==========================================================
# Calculadora de Descuento - Lógica separada de la página web
# ==========================================================

# --------------------------
# Función que realiza el cálculo
# --------------------------
def calcular_descuento(precio, porcentaje):
    """
    Recibe: precio original y % de descuento
    Devuelve: monto del descuento y precio final
    """
    # Calculamos cuánto dinero es el descuento
    monto_descuento = precio * porcentaje / 100
    
    # Restamos para saber cuánto se paga al final
    precio_final = precio - monto_descuento
    
    return monto_descuento, precio_final


# --------------------------
# Interacción con el usuario
# --------------------------
if __name__ == "__main__":
    print("=== CALCULADORA DE DESCUENTO ===\n")
    
    # Pedimos los datos al usuario
    precio = float(input("Ingresa el precio del producto: $"))
    descuento = float(input("Ingresa el porcentaje de descuento: "))
    
    # Llamamos a la función para hacer el cálculo
    monto, total_a_pagar = calcular_descuento(precio, descuento)
    
    # Mostramos los resultados
    print("\n--- RESULTADOS ---")
    print(f"Precio original:    ${precio:,.2f}")
    print(f"Descuento ({descuento}%):  -${monto:,.2f}")
    print(f"Precio final:       ${total_a_pagar:,.2f}")