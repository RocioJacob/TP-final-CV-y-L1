from typing import List
from datetime import datetime
# Importación de modelos
from cliente import Cliente
from cuenta import Cuenta 

try:
# ... (el resto de la implementación es el mismo) ...
    from fpdf import FPDF
except Exception:
    FPDF = None

# -------------------- GENERADOR DE PDF (FPDF) --------------------

class PDFGenerator:
    def __init__(self, filename: str = "reporte.pdf"):
        if FPDF is None:
            raise ImportError("FPDF no está instalado. Ejecutar: pip install fpdf2")
        self.filename = filename

    def generar_pdf_cliente(self, cliente: Cliente, cuentas: List[Cuenta]):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Reporte Cliente: {cliente.nombre} {cliente.apellido}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, f"DNI: {cliente.dni}", ln=True)
        pdf.ln(6)
        for cuenta in cuentas:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, f"Cuenta: {cuenta.numero_cuenta} ({cuenta.__class__.__name__})", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.cell(0, 8, f"Saldo: {cuenta.saldo:.2f}", ln=True)
            pdf.cell(0, 6, "Transacciones (Últimas 10):", ln=True)
            for tx in cuenta.obtener_transacciones()[-10:]:
                pdf.cell(0, 6, f" - {tx.fecha.strftime('%Y-%m-%d %H:%M:%S')} {tx.tipo} {tx.monto:.2f}", ln=True)
            pdf.ln(4)
        pdf.cell(0, 6, f"Generado: {datetime.now().isoformat()}")
        import os
        directory = 'reportes'
        if not os.path.exists(directory):
            os.makedirs(directory)
        pdf.output(os.path.join(directory, self.filename))
        return self.filename