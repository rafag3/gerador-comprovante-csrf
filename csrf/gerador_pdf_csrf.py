# csrf/gerador_pdf_csrf.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime

def gerar_pdf_csrf(dados, destino):
    c = canvas.Canvas(destino, pagesize=A4)
    w, h = A4

    x0 = 40
    y = h - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x0, y, f"COMPROVANTE ANUAL DE RETENÇÃO – CSRF ({dados['ano']})")
    y -= 25

    data = datetime.datetime.now().strftime("%d/%m/%Y")
    c.setFont("Helvetica", 10)
    c.drawString(x0, y, f"Responsável: {dados['responsavel']}     Emitido em: {data}")
    y -= 30

    c.setFont("Helvetica-Bold", 11)
    c.drawString(x0, y, "1. Dados do Fornecedor")
    y -= 18

    c.setFont("Helvetica", 10)
    c.drawString(x0, y, f"Razão Social: {dados['nome']}")
    y -= 14
    c.drawString(x0, y, f"CNPJ: {dados['cnpj']}")
    y -= 25

    c.setFont("Helvetica-Bold", 11)
    c.drawString(x0, y, "2. Movimentação Mensal")
    y -= 18

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x0, y, "Competência")
    c.drawString(x0 + 160, y, "Valor Total (R$)")
    c.drawString(x0 + 330, y, "INSS Retido (R$)")
    y -= 12
    c.line(x0, y, w - 40, y)
    y -= 15

    c.setFont("Helvetica", 10)

    total_r = 0
    total_inss = 0

    for mes in dados["meses"]:
        c.drawString(x0, y, str(mes["competencia"]))
        c.drawRightString(x0 + 280, y, f"{mes['valor_total']:,.2f}")
        c.drawRightString(x0 + 450, y, f"{mes['valor_inss']:,.2f}")
        y -= 14

        total_r += mes["valor_total"]
        total_inss += mes["valor_inss"]

        if y < 80:
            c.showPage()
            y = h - 50
            c.setFont("Helvetica", 10)

    y -= 10
    c.line(x0, y, w - 40, y)
    y -= 20

    c.setFont("Helvetica-Bold", 11)
    c.drawString(x0, y, "3. Totais")
    y -= 18

    c.setFont("Helvetica", 10)
    c.drawString(x0, y, f"Total do Rendimento: R$ {total_r:,.2f}")
    y -= 14
    c.drawString(x0, y, f"Total de INSS Retido: R$ {total_inss:,.2f}")

    c.save()
