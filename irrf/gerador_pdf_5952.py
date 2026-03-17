# irrf/gerador_pdf_5952.py

from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
import datetime


# Conversão de mês numérico para abreviação (igual ao PDF real)
def mes_abreviado(numero):
    nomes = {
        1:"Jan", 2:"Fev", 3:"Mar", 4:"Abr", 5:"Mai", 6:"Jun",
        7:"Jul", 8:"Ago", 9:"Set", 10:"Out", 11:"Nov", 12:"Dez"
    }
    return nomes.get(numero, "")


def gerar_pdf_5952(dados, destino_pdf):
    """
    Gera o PDF oficial do código 5952 (CSLL/COFINS/PIS),
    seguindo EXATAMENTE o layout do PDF enviado pelo usuário.
    """

    c = canvas.Canvas(destino_pdf, pagesize=A4)
    largura, altura = A4

    x0 = 50
    y = altura - 50

    # ============================================================
    # CABEÇALHO (igual ao PDF oficial)  [1](https://sompocorp-my.sharepoint.com/personal/j2l_rpnascimento_sompo_com_br/Documents/Arquivos%20de%20Microsoft%20Copilot%20Chat/1%20-%20Informes%20de%20Rendimentos_8045_94.704.202_0001-68.pdf)
    # ============================================================
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(largura/2, y, "Ministério da Fazenda")
    y -= 18

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(largura/2, y, "Secretaria Especial da Receita Federal do Brasil")
    y -= 22

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(largura/2, y,
        "COMPROVANTE ANUAL DE RETENÇÃO DE CSLL, COFINS E PIS/PASEP")
    y -= 16

    c.setFont("Helvetica", 10)
    c.drawCentredString(largura/2, y, "(Lei nº 10.833/2003, art. 30)")
    y -= 15

    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(largura/2, y, f"Ano-calendário de {dados['ano']}")
    y -= 30

    # ============================================================
    # BLOCO 1 – FONTE PAGADORA (fixo no PDF)
    # ============================================================
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x0, y, "1. FONTE PAGADORA")
    y -= 16

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "Nome")
    c.setFont("Helvetica", 9)
    c.drawString(x0 + 140, y, "Sompo Seguros S.A.")
    y -= 14

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "CNPJ")
    c.setFont("Helvetica", 9)
    c.drawString(x0 + 140, y, "61.383.493/0001-80")
    y -= 25

    # ============================================================
    # BLOCO 2 – PESSOA JURÍDICA FORNECEDORA DO SERVIÇO
    # ============================================================
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x0, y, "2. PESSOA JURÍDICA FORNECEDORA DO SERVIÇO")
    y -= 18

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "Nome completo")
    c.setFont("Helvetica", 9)
    c.drawString(x0 + 140, y, dados["razao"])
    y -= 14

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "CNPJ")
    c.setFont("Helvetica", 9)
    c.drawString(x0 + 140, y, dados["cnpj"])
    y -= 25

    # ============================================================
    # BLOCO 3 – TABELA (layout idêntico ao PDF)  [1](https://sompocorp-my.sharepoint.com/personal/j2l_rpnascimento_sompo_com_br/Documents/Arquivos%20de%20Microsoft%20Copilot%20Chat/1%20-%20Informes%20de%20Rendimentos_8045_94.704.202_0001-68.pdf)
    # ============================================================
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x0, y, "3. RELAÇÃO DE PAGAMENTOS E RETENÇÕES")
    y -= 20

    col_larguras = [
        120,   # Mês do pagamento
        130,   # Código
        120,   # Valor pago
        120    # Valor retido
    ]

    styles = getSampleStyleSheet()

    estilo_cab = styles['Heading5']
    estilo_cab.fontSize = 9
    estilo_cab.alignment = TA_CENTER

    estilo = styles['Normal']
    estilo.fontSize = 9
    estilo.leading = 12

    tabela_dados = [[
        Paragraph("MÊS DO PAGAMENTO", estilo_cab),
        Paragraph("CÓDIGO DA RETENÇÃO", estilo_cab),
        Paragraph("VALOR PAGO", estilo_cab),
        Paragraph("VALOR RETIDO", estilo_cab)
    ]]

    for _, linha in dados["meses"].iterrows():

        tabela_dados.append([
            Paragraph(mes_abreviado(int(linha["Mes"])), estilo),
            Paragraph("5952", estilo),
            Paragraph(f"R$ {linha['valor_pago']:,.2f}", estilo),
            Paragraph(f"R$ {linha['valor_retido']:,.2f}", estilo)
        ])

    # Linha de total
    tabela_dados.append([
        Paragraph("<b>Total</b>", estilo),
        Paragraph("5952", estilo),
        Paragraph(f"<b>R$ {dados['total_pago']:,.2f}</b>", estilo),
        Paragraph(f"<b>R$ {dados['total_retido']:,.2f}</b>", estilo)
    ])

    tabela = Table(tabela_dados, colWidths=col_larguras)

    tabela.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("BACKGROUND", (0,0), (-1,0), colors.white),
        ("LINEBELOW", (0,0), (-1,0), 1, colors.black),
        ("ALIGN", (2,1), (3,-1), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))

    w, h = tabela.wrapOn(c, largura, y)
    tabela.drawOn(c, x0, y - h)
    y -= (h + 35)

    # ============================================================
    # BLOCO 4 – INFORMAÇÕES COMPLEMENTARES
    # (em branco no PDF oficial)
    # ============================================================
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x0, y, "4. INFORMAÇÕES COMPLEMENTARES")
    y -= 30

    # ============================================================
    # BLOCO 5 – RESPONSÁVEL
    # ============================================================
    data_hoje = datetime.datetime.now().strftime("%d/%m/%Y")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x0, y, "5. RESPONSÁVEL PELAS INFORMAÇÕES")
    y -= 18

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "Nome")
    c.setFont("Helvetica", 9)
    c.drawString(x0 + 120, y, dados["responsavel"])
    y -= 14

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "Data")
    c.setFont("Helvetica", 9)
    c.drawString(x0 + 120, y, data_hoje)
    y -= 14

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x0, y, "Assinatura")
    c.setFont("Helvetica", 9)
    c.drawString(x0 + 120, y, "Dispensado assinatura por meio eletrônico")
    y -= 30

    # ============================================================
    # RODAPÉ (igual ao PDF oficial)  [1](https://sompocorp-my.sharepoint.com/personal/j2l_rpnascimento_sompo_com_br/Documents/Arquivos%20de%20Microsoft%20Copilot%20Chat/1%20-%20Informes%20de%20Rendimentos_8045_94.704.202_0001-68.pdf)
    # ============================================================
    c.setFont("Helvetica", 8)
    c.drawString(x0, 25, "Aprovado pela IN SRF nº 459/2004")

    c.save()