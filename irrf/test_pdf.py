from irrf.gerador_pdf_irrf import gerar_irrf_pdf

dados = {
    "codigo": "1708",
    "ano": "2026",
    "responsavel": "Teste",
    "cnpj": "11.111.111/0001-11",
    "razao": "EMPRESA TESTE",
    "descricao": "Serviços profissionais",
    "meses": [
    ],
    "total_ano": 0,
    "total_irrf": 0
}

gerar_irrf_pdf(dados, "teste.pdf")
print("PDF gerado!")