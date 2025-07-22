from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_receipt(tenant_name, house_number, amount, receipt_id):
    filename = f"receipt_{receipt_id}.pdf"
    c = canvas.Canvas(filename)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "RENT PAYMENT RECEIPT")

    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Receipt ID: {receipt_id}")
    c.drawString(50, 730, f"Tenant Name: {tenant_name}")
    c.drawString(50, 710, f"House Number: {house_number}")
    c.drawString(50, 690, f"Amount Paid: KES {amount}")
    c.drawString(50, 670, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 640, "Thank you for your payment!")

    c.save()
    print(f"📄 Receipt generated: {filename}")
