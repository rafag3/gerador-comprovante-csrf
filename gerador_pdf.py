from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def formatar_real(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def gerar_pdf(dados, caminho):

    largura, altura = A4
    c = canvas.Canvas(caminho, pagesize=A4)

    y = altura - 40

    # Cabeçalho
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(largura/2, y, "Ministério da Fazenda")
    y -= 15
    c.drawCentredString(largura/2, y, "Secretaria Especial da Receita Federal do Brasil")
    y -= 15
    c.drawCentredString(largura/2, y, "Receita Federal")

    y -= 25
    c.drawCentredString(
        largura/2,
        y,
        "COMPROVANTE ANUAL DE RETENÇÃO DE CSLL, COFINS E PIS/PASEP"
    )

    y -= 15
    c.setFont("Helvetica", 10)
    c.drawCentredString(largura/2, y, "(Lei nº 10.833/2003, art. 30)")
    y -= 15

    c.drawCentredString(largura/2, y, "Ano-calendário de 2025")

    y -= 30

    # BLOCO 1
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "1. FONTE PAGADORA")
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Nome: Sompo Seguros S.A.")
    y -= 20
    c.drawString(50, y, "CNPJ: 61.383.493/0001-80")

    y -= 30

    # BLOCO 2
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "2. PESSOA JURÍDICA FORNECEDORA DO SERVIÇO")
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Nome completo: {dados['razao']}")
    y -= 20
    c.drawString(50, y, f"CNPJ: {dados['cnpj']}")

    y -= 30

    # BLOCO 3
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "3. RELAÇÃO DE PAGAMENTOS E RETENÇÕES")

    y -= 20

    # Cabeçalho da tabela
    c.setFont("Helvetica-Bold", 9)

    c.drawString(50, y, "MÊS")
    c.drawString(140, y, "CÓDIGO")
    c.drawString(250, y, "VALOR PAGO")
    c.drawString(380, y, "VALOR RETIDO")

    y -= 15

    meses_nome = {
        1: "Jan/2025",
        2: "Fev/2025",
        3: "Mar/2025",
        4: "Abr/2025",
        5: "Mai/2025",
        6: "Jun/2025",
        7: "Jul/2025",
        8: "Ago/2025",
        9: "Set/2025",
        10: "Out/2025",
        11: "Nov/2025",
        12: "Dez/2025"
    }

    c.setFont("Helvetica", 9)

    total_pago = 0
    total_retido = 0

    for mes in range(1, 13):

        info = dados["meses"].get(mes, {"pago":0, "retido":0})

        pago = info["pago"]
        retido = info["retido"]

        total_pago += pago
        total_retido += retido

        c.drawString(50, y, meses_nome[mes])
        c.drawString(140, y, str(dados["codigo"]))
        c.drawString(250, y, formatar_real(pago))
        c.drawString(380, y, formatar_real(retido))

        y -= 15

    y -= 10

    # Totais
    c.setFont("Helvetica-Bold", 10)

    c.drawString(50, y, "Total")
    c.drawString(250, y, formatar_real(total_pago))
    c.drawString(380, y, formatar_real(total_retido))

    y -= 40

    # BLOCO 4
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "4. INFORMAÇÕES COMPLEMENTARES")
    y -= 20

    c.setFont("Helvetica", 9)
    c.drawString(
        50,
        y,
        "Comprovante gerado em meio eletrônico para fins de comprovação anual das retenções informadas."
    )

    y -= 30

    # BLOCO 5
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "5. RESPONSÁVEL PELAS INFORMAÇÕES")
    y -= 20

    c.setFont("Helvetica", 9)
    c.drawString(50, y, "Nome: MARCELO BATISTA DA SILVA")
    y -= 20

    c.drawString(50, y, "Assinatura: Dispensado assinatura por meio eletrônico")

    y -= 40

    # Rodapé
    c.drawString(50, 30, "Aprovado pela IN SRF nº 459/2004")
    c.drawRightString(largura-50, 30, "Pág. 1")

    c.save()