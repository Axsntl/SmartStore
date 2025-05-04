from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os


def generar_ticket_pdf(usuario, carrito, output_path="ticket.pdf"):
    """
    Genera un ticket de compra en PDF usando ReportLab.

    usuario: dict con claves 'id' y 'nombre'
    carrito: lista de productos, cada uno con 'nombre', 'precio', 'cantidad'
    output_path: ruta de salida del PDF
    """
    print(f"DEBUG: generar_ticket_pdf() iniciado con usuario={usuario}, carrito={carrito}, output_path={output_path}")
    try:
        # Asegurar carpeta de salida
        save_dir = os.path.dirname(output_path)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
            print(f"DEBUG: Creada carpeta de salida {save_dir}")

        # Preparar canvas
        c = canvas.Canvas(output_path, pagesize=LETTER)
        width, height = LETTER

        # Fondo de header negro
        c.setFillColor(colors.black)
        c.rect(0, height-80, width, 80, fill=1, stroke=0)

        # Logo y título
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(40, height-50, "SmartStore")

        # Franja azul
        c.setFillColor(colors.HexColor("#0057B7"))
        c.rect(0, height-85, width, 5, fill=1, stroke=0)

        # Detalles usuario y fecha
        y = height - 120
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
        c.drawString(40, y, f"Fecha: {fecha}")
        c.drawString(300, y, f"Cliente: {usuario.get('nombre')} (ID: {usuario.get('id')})")

        # Encabezados tabla
        y -= 20
        c.setFont("Helvetica-Bold", 11)
        for texto, x in [("Producto", 40), ("Precio", 280), ("Cant.", 350), ("Subtotal", 410)]:
            c.drawString(x, y, texto)

        # Lista de productos
        y -= 15
        c.setFont("Helvetica", 10)
        total = 0
        for prod in carrito:
            nombre = prod.get("nombre")
            precio = prod.get("precio", 0)
            cantidad = prod.get("cantidad", 0)
            subtotal = precio * cantidad
            total += subtotal

            if y < 50:
                c.showPage()
                y = height - 50
            c.drawString(40, y, nombre)
            c.drawString(280, y, f"${precio:.2f}")
            c.drawString(350, y, str(cantidad))
            c.drawString(410, y, f"${subtotal:.2f}")
            y -= 15

        # Total final
        if y < 80:
            c.showPage()
            y = height - 80
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, f"TOTAL A PAGAR: ${total:.2f}")

        # Pie de página
        y -= 30
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(40, y, "Gracias por tu compra en SmartStore!")

        # Guardar PDF
        c.save()
        print(f"DEBUG: PDF guardado correctamente en {output_path}")

        # Intentar abrir automáticamente
        try:
            os.startfile(output_path)
            print(f"DEBUG: Abriendo PDF en {output_path}")
        except Exception as e:
            print(f"DEBUG: No se pudo abrir automáticamente el PDF: {e}")

    except Exception as err:
        print(f"DEBUG: Error generando PDF: {err}")
