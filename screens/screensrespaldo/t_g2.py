from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, Image
from datetime import datetime
import os


def generar_ticket_pdf(usuario: dict, carrito: list, output_path: str = "ticket.pdf") -> str:
    """
    Genera un ticket de compra en PDF con un diseño elegante.

    Args:
        usuario (dict): {'id', 'nombre'}
        carrito (list): [{'nombre','precio','cantidad'}]
        output_path (str): Ruta de salida.

    Returns:
        str: Ruta generada o None.
    """
    print(f"DEBUG: generar_ticket_pdf elegante() iniciado con usuario={usuario}, carrito={carrito}, output_path={output_path}")
    try:
        # Crear carpeta de salida
        dirpath = os.path.dirname(output_path)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)

        # Canvas en horizontal para aspecto tipo factura
        c = canvas.Canvas(output_path, pagesize=landscape(LETTER))
        width, height = landscape(LETTER)

        # Logo (si existe) y título sofisticado
        logo_path = "core/assets/icons/SSICON.png"
        if os.path.exists(logo_path):
            c.drawImage(logo_path, inch*0.5, height - inch*1, width=inch, height=inch, mask='auto')
        c.setFont("Helvetica-Bold", 26)
        c.setFillColor(colors.HexColor("#0057B7"))
        c.drawString(inch*1.7, height - inch*0.8, "SmartStore - Ticket de Compra")

        # Línea decorativa
        c.setStrokeColor(colors.HexColor("#0057B7"))
        c.setLineWidth(2)
        c.line(inch*0.5, height - inch*1.1, width - inch*0.5, height - inch*1.1)

        # Info cliente y fecha en gris oscuro
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.grey)
        fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
        c.drawString(inch*0.5, height - inch*1.4, f"Fecha: {fecha}")
        c.drawString(width/2, height - inch*1.4, f"Cliente: {usuario.get('nombre')} (ID {usuario.get('id')})")

        # Preparar datos de tabla
        datos = [["Producto", "Precio Unit.", "Cantidad", "Subtotal"]]
        total = 0.0
        for prod in carrito:
            nombre = prod.get("nombre", "")
            precio = float(prod.get("precio", 0))
            cantidad = int(prod.get("cantidad", 0))
            subtotal = round(precio * cantidad, 2)
            total += subtotal
            datos.append([nombre, f"${precio:.2f}", cantidad, f"${subtotal:.2f}"])
        datos.append(["", "", "TOTAL:", f"${total:.2f}"])

        # Crear tabla y estilo
        tabla = Table(datos, colWidths=[3*inch, 1.2*inch, 1*inch, 1.2*inch])
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0057B7")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN',(1,1),(-1,-1),'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('BACKGROUND', (0,1), (-1,-2), colors.HexColor("#F2F2F2")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ])
        tabla.setStyle(style)

        # Ubicar tabla
        tabla.wrapOn(c, width, height)
        tabla.drawOn(c, inch*0.5, height - inch*3)

        # Pie de página estilizado
        footer_y = inch*0.5
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.darkgrey)
        c.drawCentredString(width/2, footer_y, "¡Gracias por tu confianza! Visítanos de nuevo en SmartStore.")

        # Guardar y abrir
        c.save()
        print(f"DEBUG: Ticket elegante guardado en {output_path}")
        try:
            os.startfile(output_path)
        except Exception as e:
            print(f"DEBUG: No se pudo abrir automáticamente: {e}")
        return output_path
    except Exception as e:
        print(f"DEBUG: Error en generar_ticket_pdf elegante: {e}")
        return None
