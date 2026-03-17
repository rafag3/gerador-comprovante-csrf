# irrf/gerador_pdf_irrf.py

from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import datetime


def mes_abreviado(numero):
    meses = {
        1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
        7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"
    }
    return meses.get(numero, "?")


def gerar_irrf_pdf(dados, destino_pdf):

    c = canvas.Canvas(destino_pdf, pagesize=A4)
    largura, altura = A4

    x0 = 40
    y = altura - 40

    # Cabeçalho
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(largura/2, y, "MINISTÉRIO DA FAZENDA")
    y -= 16
    c.drawCentredString(largura/2, y, "SECRETARIA DA RECEITA FEDERAL")
    y -= 16
    c.drawCentredString(largura/2, y,
        "COMPROVANTE ANUAL DE RENDIMENTOS PAGOS OU CREDITADOS")
    y -= 14
    c.drawCentredString(largura/2, y,
        "E DE RETENÇÃO DE IMPOSTO DE RENDA NA FONTE – PESSOA JURÍDICA")
    y -= 20
    c.drawCentredString(largura/2, y, f"Ano-calendário: {dados['ano']}")
    y -= 30

    # Fonte Pagadora
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x0, y, "1. FONTE PAGADORA")
    y -= 16

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "NOME EMPRESARIAL")
    c.setFont("Helvetica", 9)
    c.drawString(x0+140, y, "SOMPO SEGUROS S.A.")
    y -= 14

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "CNPJ")
    c.setFont("Helvetica", 9)
    c.drawString(x0+140, y, "61.383.493/0001-80")
    y -= 25

    # Beneficiário
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x0, y, "2. PESSOA JURÍDICA BENEFICIÁRIA DOS RENDIMENTOS")
    y -= 16

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "NOME EMPRESARIAL")
    c.setFont("Helvetica", 9)
    c.drawString(x0+140, y, dados["razao"])
    y -= 14

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "CNPJ")
    c.setFont("Helvetica", 9)
    c.drawString(x0+140, y, dados["cnpj"])
    y -= 25

    # Tabela IRRF
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x0, y, "3. RENDIMENTO E IMPOSTO RETIDO NA FONTE")
    y -= 18

    col_widths = [45, 55, 250, 70, 70]

    styles = getSampleStyleSheet()
    cell = styles["Normal"]
    cell.fontSize = 9
    head = styles["Heading5"]
    head.fontSize = 9
    head.alignment = TA_CENTER

    tabela = [[
        Paragraph("Mês", head),
        Paragraph("Código", head),
        Paragraph("Descrição do Rendimento", head),
        Paragraph("Rendimento (R$)", head),
        Paragraph("Imposto (R$)", head)
    ]]

    for _, linha in dados["meses"].iterrows():
        tabela.append([
            Paragraph(mes_abreviado(int(linha["Mes"])), cell),
            Paragraph(str(dados["codigo"]), cell),
            Paragraph(dados["descricao"], cell),
            Paragraph(f"{linha['total']:,.2f}", cell),
            Paragraph(f"{linha['irrf']:,.2f}", cell)
        ])

    tabela.append([
        Paragraph("<b>TOTAL NO ANO</b>", cell),
        Paragraph(str(dados["codigo"]), cell),
        Paragraph("", cell),
        Paragraph(f"<b>{dados['total_ano']:,.2f}</b>", cell),
        Paragraph(f"<b>{dados['total_irrf']:,.2f}</b>", cell)
    ])

    tbl = Table(tabela, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.25, colors.black),
        ("ALIGN", (3,1), (4,-1), "RIGHT")
    ]))

    w, h = tbl.wrap(largura, y)
    tbl.drawOn(c, x0, y-h)
    y -= h + 30

    # Responsável
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x0, y, "5. RESPONSÁVEL PELAS INFORMAÇÕES")
    y -= 16

    data = datetime.datetime.now().strftime("%d/%m/%Y")

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "NOME")
    c.setFont("Helvetica", 9)
    c.drawString(x0+140, y, dados["responsavel"])
    y -= 14

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "DATA")
    c.setFont("Helvetica", 9)
    c.drawString(x0+140, y, data)
    y -= 14

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "ASSINATURA")
    c.setFont("Helvetica", 9)
    c.drawString(x0+140, y, "Dispensado assinatura eletrônica")
    y -= 25

    c.save()