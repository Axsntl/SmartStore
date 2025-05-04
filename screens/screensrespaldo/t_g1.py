from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os


def generar_ticket_pdf(usuario: dict, carrito: list, output_path: str = "ticket.pdf") -> str:
    """
    Genera un ticket de compra en PDF usando ReportLab.

    Args:
        usuario (dict): Datos del usuario con claves 'id' y 'nombre'.
        carrito (list): Lista de productos en el carrito. Cada producto debe ser dict con 'nombre', 'precio', 'cantidad'.
        output_path (str): Ruta donde se guardará el PDF.

    Returns:
        str: La ruta del archivo PDF generado.
    """
    # DEBUG: inicio generación
    print(f"DEBUG: generar_ticket_pdf() iniciado con usuario={usuario}, carrito={carrito}, output_path={output_path}")
    try:
        # 1. Preparar carpeta de salida si es necesario
        save_dir = os.path.dirname(output_path)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
            print(f"DEBUG: Creada carpeta de salida: {save_dir}")

        # 2. Crear objeto Canvas
        c = canvas.Canvas(output_path, pagesize=LETTER)
        width, height = LETTER

        # 3. Dibujar header
        #   - fondo negro
        c.setFillColor(colors.black)
        c.rect(0, height - 80, width, 80, fill=1, stroke=0)
        #   - título SmartStore en blanco
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(40, height - 50, "SmartStore")
        #   - línea azul debajo
        c.setFillColor(colors.HexColor("#0057B7"))
        c.rect(0, height - 85, width, 5, fill=1, stroke=0)

        # 4. Detalles de usuario y fecha
        y = height - 120
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
        c.drawString(40, y, f"Fecha: {fecha}")
        c.drawString(300, y, f"Cliente: {usuario.get('nombre')} (ID: {usuario.get('id')})")

        # 5. Encabezados de tabla
        y -= 20
        c.setFont("Helvetica-Bold", 11)
        for texto, x in [("Producto", 40), ("Precio", 280), ("Cant.", 350), ("Subtotal", 410)]:
            c.drawString(x, y, texto)

        # 6. Listado de productos
        y -= 15
        c.setFont("Helvetica", 10)
        total = 0.0
        for prod in carrito:
            nombre = prod.get("nombre", "")
            precio = float(prod.get("precio", 0))
            cantidad = int(prod.get("cantidad", 0))
            subtotal = precio * cantidad
            total += subtotal

            # Salto de página si llega al margen inferior
            if y < 50:
                c.showPage()
                y = height - 50

            # Dibujar fila de producto
            c.drawString(40, y, nombre)
            c.drawString(280, y, f"${precio:.2f}")
            c.drawString(350, y, str(cantidad))
            c.drawString(410, y, f"${subtotal:.2f}")
            y -= 15

        # 7. Total final
        if y < 80:
            c.showPage()
            y = height - 80
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, f"TOTAL A PAGAR: ${total:.2f}")

        # 8. Pie de página con mensaje de agradecimiento
        y -= 30
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(40, y, "Gracias por tu compra en SmartStore!")

        # 9. Guardar el PDF en disco
        c.save()
        print(f"DEBUG: PDF guardado correctamente en: {output_path}")

        # 10. Intentar abrir automáticamente en Windows
        try:
            os.startfile(output_path)
            print(f"DEBUG: Abriendo PDF en: {output_path}")
        except Exception as e:
            print(f"DEBUG: No se pudo abrir automáticamente el PDF: {e}")

        return output_path

    except Exception as err:
        print(f"DEBUG: Error generando PDF: {err}")
        return None
