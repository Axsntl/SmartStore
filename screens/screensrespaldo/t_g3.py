from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import os
import appdirs


def generar_ticket_pdf(usuario: dict, carrito: list, output_dir: str = None) -> str:
    """
    Genera un ticket de compra en PDF con un diseño elegante y nombre único.

    Args:
        usuario (dict): Datos del usuario con llaves 'id' y 'nombre'.
        carrito (list): Lista de productos, cada uno con 'nombre','precio','cantidad'.
        output_dir (str, optional): Carpeta donde guardar los tickets. Si no se indica,
            se usará el directorio de datos del usuario.

    Returns:
        str: Ruta completa al archivo PDF generado, o None si hay error.
    """
    # 1. Determinar carpeta de salida usando appdirs si no se proporciona
    if not output_dir:
        user_data = appdirs.user_data_dir("SmartStore", "SmartStoreOrg")
        output_dir = os.path.join(user_data, "tickets")
    os.makedirs(output_dir, exist_ok=True)

    # 2. Crear nombre de archivo único: usuario + timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_name = usuario.get('nombre', 'user').replace(' ', '_')
    filename = f"{safe_name}_{timestamp}.pdf"
    output_path = os.path.join(output_dir, filename)
    print(f"DEBUG: Guardando ticket en {output_path}")

    try:
        # 3. Configurar canvas en horizontal (landscape)
        c = canvas.Canvas(output_path, pagesize=landscape(LETTER))
        width, height = landscape(LETTER)

        # 4. Encabezado: Título a la izquierda, logo opcional a la derecha
        header_h = inch
        c.setFont("Helvetica-Bold", 28)
        c.setFillColor(colors.HexColor("#0057B7"))
        c.drawString(inch * 0.5, height - header_h + 0.3 * inch, "SmartStore - Ticket")
        logo = "core/assets/icons/SSICON.png"
        logo_size = 0.8 * inch
        if os.path.exists(logo):
            c.drawImage(logo, width - inch * 0.5 - logo_size, height - header_h + 0.2 * inch,
                        width=logo_size, height=logo_size, preserveAspectRatio=True, mask='auto')
        # Línea decorativa
        c.setStrokeColor(colors.HexColor("#0057B7"))
        c.setLineWidth(2)
        c.line(inch * 0.5, height - header_h, width - inch * 0.5, height - header_h)

        # 5. Detalles de usuario y fecha
        info_y = height - header_h - 0.2 * inch
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.grey)
        fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
        c.drawString(inch * 0.5, info_y, f"Fecha: {fecha}")
        c.drawRightString(width - inch * 0.5, info_y,
                          f"Cliente: {usuario.get('nombre')} (ID: {usuario.get('id')})")

        # 6. Preparar datos de la tabla de productos
        datos = [["Producto", "Precio", "Cant.", "Subtotal"]]
        total = 0.0
        for prod in carrito:
            nombre = prod.get("nombre", "")
            precio = float(prod.get("precio", 0))
            cantidad = int(prod.get("cantidad", 0))
            subtotal = round(precio * cantidad, 2)
            total += subtotal
            datos.append([nombre, f"${precio:.2f}", cantidad, f"${subtotal:.2f}"])
        datos.append(["", "", "TOTAL", f"${total:.2f}"])

        # 7. Crear y estilizar la tabla
        col_w = [3.5 * inch, 1.2 * inch, 1 * inch, 1.2 * inch]
        tabla = Table(datos, colWidths=col_w)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0057B7")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor("#F7F7F7")),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#E0E0E0")),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        # 8. Posicionar y dibujar la tabla
        start_y = info_y - inch
        tabla.wrapOn(c, width, height)
        tabla.drawOn(c, inch * 0.5, start_y - len(datos) * 0.25 * inch)

        # 9. Pie de página agradecimiento
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.darkgrey)
        c.drawCentredString(width / 2, 0.5 * inch,
                              "Gracias por tu compra! Vuelve pronto a SmartStore.")

        # 10. Guardar y abrir automáticamente
        c.save()
        print(f"DEBUG: Ticket guardado en {output_path}")
        try:
            os.startfile(output_path)
        except Exception:
            pass
        return output_path
    except Exception as ex:
        print(f"DEBUG: Error generando ticket: {ex}")
        return None
