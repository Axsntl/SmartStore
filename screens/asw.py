from reportlab.pdfgen import canvas

c = canvas.Canvas("test_ticket.pdf")
c.drawString(100, 750, "Hola mundo desde ReportLab!")
c.save()
print("PDF generado")
