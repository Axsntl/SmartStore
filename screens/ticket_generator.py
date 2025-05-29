from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os


def generar_ticket_pdf(usuario: dict, carrito: list, output_dir: str = None) -> str:
    """
    Genera un ticket PDF en el directorio Documents/SmartStore/tickets con nombre único.

    Args:
        usuario (dict): {'id', 'nombre'} del cliente.
        carrito (list): Lista de productos con 'nombre', 'precio', 'cantidad'.
        output_dir (str, optional): Carpeta de destino. Si None, usa Documents/SmartStore/tickets.

    Returns:
        str: Ruta al PDF generado o None en caso de error.
    """
    # 1. Determinar carpeta de salida en Documents
    if not output_dir:
        home = os.path.expanduser("~")
        output_dir = os.path.join(home, "Documents", "SmartStore", "tickets")
    os.makedirs(output_dir, exist_ok=True)
    print(f"DEBUG: Usando directorio de tickets: {output_dir}")

    # 2. Nombre único usando usuario y timestamp
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    uname = usuario.get('nombre', 'user').replace(' ', '_')
    filename = f"{uname}_{ts}.pdf"
    output_path = os.path.join(output_dir, filename)
    print(f"DEBUG: Ruta de salida: {output_path}")

    try:
        # 3. Crear canvas
        c = canvas.Canvas(output_path, pagesize=LETTER)
        width, height = LETTER

        # 4. Header: fondo y título
        c.setFillColor(colors.HexColor("#0057B7"))
        c.rect(0, height-80, width, 80, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(40, height-50, "SmartStore")
        # línea debajo
        c.setFillColor(colors.white)
        c.setFont("Helvetica", 12)
        c.drawString(40, height-65, f"Ticket generado: {ts}")

        # 5. Detalles cliente y fecha
        y = height - 100
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
        c.drawString(40, y, f"Fecha: {fecha}")
        c.drawRightString(width-40, y, f"Cliente: {usuario.get('nombre')} (ID: {usuario.get('id')})")

        # 6. Encabezados tabla
        y -= 20
        c.setFont("Helvetica-Bold", 11)
        for text, x in [("Producto", 40), ("Precio", 280), ("Cant.", 360), ("Subtotal", 430)]:
            c.drawString(x, y, text)

        # 7. Listado productos
        y -= 15
        c.setFont("Helvetica", 10)
        total = 0
        for prod in carrito:
            nombre = prod.get('nombre', '')
            precio = float(prod.get('precio', 0))
            cantidad = int(prod.get('cantidad', 0))
            subtotal = precio * cantidad
            total += subtotal
            if y < 50:
                c.showPage()
                y = height - 50
            c.drawString(40, y, nombre)
            c.drawString(280, y, f"${precio:.2f}")
            c.drawString(360, y, str(cantidad))
            c.drawString(430, y, f"${subtotal:.2f}")
            y -= 15

        # 8. Total final
        if y < 80:
            c.showPage()
            y = height - 80
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, f"TOTAL A PAGAR: ${total:.2f}")

        # 9. Pie de página
        y -= 30
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.grey)
        c.drawString(40, y, "¡Gracias por su compra en SmartStore!")

        # 10. Guardar PDF
        c.save()
        print(f"DEBUG: PDF guardado en: {output_path}")
        # Intentar abrir (solo Windows)
        try:
            os.startfile(output_path)
        except Exception:
            pass
        return output_path

    except Exception as e:
        print(f"DEBUG: Error al generar PDF: {e}")
        return None
# El pdf se genera en el directorio especificado o en el predeterminado, util si se quiere lanzar como programa