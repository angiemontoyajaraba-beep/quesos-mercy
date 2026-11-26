import html
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs


PRODUCTOS = {
    "queso_blando": {
        "nombre": "Queso Blando",
        "precio": 14000
    },
    "queso_duro": {
        "nombre": "Queso Duro",
        "precio": 15000
    },
    "bollos": {
        "nombre": "Bollos",
        "precio": 3000
    },
    "suero": {
        "nombre": "Suero",
        "precio": 8000
    },
    "yuca": {
        "nombre": "Yuca",
        "precio": 5000
    },
    "angelito": {
        "nombre": "Angelito",
        "precio": 3000
    }
}


def formatear_pesos(valor):
    return "$" + f"{valor:,.0f}".replace(",", ".")


def calcular_descuento(precio, porcentaje):
    """
    Recibe el subtotal y el porcentaje de descuento.
    Devuelve el monto descontado y el precio final.
    """

    monto_descuento = precio * porcentaje / 100

    precio_final = precio - monto_descuento

    return monto_descuento, precio_final


def calcular_pedido(producto_id, cantidad, descuento):
    if producto_id not in PRODUCTOS:
        return {
            "ok": False,
            "mensaje": "Selecciona un producto válido."
        }

    try:
        cantidad = int(cantidad)
    except (TypeError, ValueError):
        return {
            "ok": False,
            "mensaje": "La cantidad debe ser un número entero válido."
        }

    if cantidad < 1:
        return {
            "ok": False,
            "mensaje": "La cantidad debe ser al menos 1."
        }

    try:
        porcentaje = float(descuento)
    except (TypeError, ValueError):
        return {
            "ok": False,
            "mensaje": "Ingresa un porcentaje de descuento válido."
        }

    if porcentaje != porcentaje or porcentaje < 0 or porcentaje > 100:
        return {
            "ok": False,
            "mensaje": "El descuento debe estar entre 0 y 100."
        }

    producto = PRODUCTOS[producto_id]

    precio_unitario = producto["precio"]

    subtotal = precio_unitario * cantidad

    monto_descuento, total = calcular_descuento(
        subtotal,
        porcentaje
    )

    return {
        "ok": True,
        "producto": producto["nombre"],
        "cantidad": cantidad,
        "precio_unitario": formatear_pesos(precio_unitario),
        "subtotal": formatear_pesos(subtotal),
        "porcentaje": porcentaje,
        "descuento": formatear_pesos(monto_descuento),
        "total": formatear_pesos(total)
    }


def crear_pagina(contenido):
    return f"""<!DOCTYPE html>
<html lang="es-CO">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultado | Quesos Mercy</title>

    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 25px 15px;
            font-family: Arial, sans-serif;
            background: #fff8ed;
            color: #40352b;
        }}

        .contenedor {{
            max-width: 520px;
            margin: 40px auto;
            padding: 30px;
            background: white;
            border-radius: 14px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        }}

        h1 {{
            text-align: center;
            color: #8a5a2b;
        }}

        .detalle {{
            padding: 13px 0;
            border-bottom: 1px solid #eee;
        }}

        .total {{
            margin-top: 25px;
            text-align: center;
            font-size: 27px;
            font-weight: bold;
            color: #397443;
        }}

        .mensaje {{
            margin-top: 20px;
            padding: 15px;
            background: #f7f1e7;
            border-radius: 8px;
            text-align: center;
        }}

        .boton {{
            display: block;
            margin-top: 25px;
            padding: 13px;
            background: #8a5a2b;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 8px;
        }}

        .boton:hover {{
            background: #70451f;
        }}
    </style>
</head>

<body>

    <main class="contenedor">

        {contenido}

        <a href="/" class="boton">
            Volver a Quesos Mercy
        </a>

    </main>

</body>
</html>"""


class handler(BaseHTTPRequestHandler):

    def enviar_pagina(self, contenido, estado=200):
        pagina = crear_pagina(contenido)

        self.send_response(estado)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        self.wfile.write(pagina.encode("utf-8"))

    def do_GET(self):
        contenido = """
        <h1>🧀 Quesos Mercy</h1>
        <p>Para calcular tu pedido, regresa a la página principal
        y completa el formulario.</p>
        """

        self.enviar_pagina(contenido)

    def do_POST(self):
        longitud = int(self.headers.get("Content-Length", 0))

        datos_recibidos = self.rfile.read(longitud).decode("utf-8")

        datos = parse_qs(datos_recibidos)

        producto = datos.get("producto", [""])[0]
        cantidad = datos.get("cantidad", [""])[0]
        descuento = datos.get("descuento", ["0"])[0]

        resultado = calcular_pedido(
            producto,
            cantidad,
            descuento
        )

        if not resultado["ok"]:
            mensaje = html.escape(resultado["mensaje"])

            contenido = f"""
            <h1>No se pudo calcular el pedido</h1>

            <div class="mensaje">
                {mensaje}
            </div>

            <p>Regresa al formulario e intenta nuevamente.</p>
            """

            self.enviar_pagina(contenido, 400)
            return

        nombre = html.escape(resultado["producto"])
        cantidad = resultado["cantidad"]
        precio = resultado["precio_unitario"]
        subtotal = resultado["subtotal"]
        porcentaje = resultado["porcentaje"]
        descuento = resultado["descuento"]
        total = resultado["total"]

        contenido = f"""
        <h1>🧀 ¡Resumen de tu pedido!</h1>

        <div class="detalle">
            <strong>Producto:</strong> {nombre}
        </div>

        <div class="detalle">
            <strong>Cantidad:</strong> {cantidad}
        </div>

        <div class="detalle">
            <strong>Precio por unidad:</strong> {precio}
        </div>

        <div class="detalle">
            <strong>Subtotal:</strong> {subtotal}
        </div>

        <div class="detalle">
            <strong>Descuento aplicado:</strong> {porcentaje:g}%
        </div>

        <div class="detalle">
            <strong>Valor descontado:</strong> {descuento}
        </div>

        <div class="total">
            Total a pagar: {total}
        </div>

        <div class="mensaje">
            ¡Gracias por elegir Quesos Mercy!
        </div>
        """

        self.enviar_pagina(contenido)