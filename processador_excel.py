import pandas as pd

def processar_excel(caminho_excel):

    # Ler o Excel
    df = pd.read_excel(caminho_excel)

    # Limpar espaços nos nomes das colunas
    df.columns = df.columns.str.strip()

    # Mapear nomes da planilha para nomes internos
    mapa_colunas = {
        "Competencia": "competencia",
        "CNPJ/CPF": "cnpj",
        "Razão Social": "razao",
        "Código Retenção INSS": "codigo",
        "Valor Total": "valor_total",
        "Valor INSS": "valor_inss"
    }

    df = df.rename(columns=mapa_colunas)

    colunas_obrigatorias = [
        "competencia",
        "cnpj",
        "razao",
        "codigo",
        "valor_total",
        "valor_inss"
    ]

    # Verificar colunas obrigatórias
    for c in colunas_obrigatorias:
        if c not in df.columns:
            print("Colunas encontradas:", df.columns.tolist())
            raise Exception(f"Coluna ausente: {c}")

    beneficiarios = {}

    for _, row in df.iterrows():

        try:
            cnpj = str(row["cnpj"]).strip()
            razao = str(row["razao"]).strip()
            codigo = str(row["codigo"]).strip()

            competencia = str(row["competencia"])
            mes = int(competencia.split("/")[0])

            valor_total = float(row["valor_total"])
            valor_retido = abs(float(row["valor_inss"]))

        except Exception as e:
            print("Erro ao processar linha:", row)
            raise e

        chave = f"{cnpj}_{razao}"

        if chave not in beneficiarios:

            beneficiarios[chave] = {
                "cnpj": cnpj,
                "razao": razao,
                "codigo": codigo,
                "meses": {i: {"pago": 0.0, "retido": 0.0} for i in range(1, 13)},
                "total_pago": 0.0,
                "retido": 0.0
            }

        beneficiarios[chave]["meses"][mes]["pago"] += valor_total
        beneficiarios[chave]["meses"][mes]["retido"] += valor_retido

        beneficiarios[chave]["total_pago"] += valor_total
        beneficiarios[chave]["retido"] += valor_retido

    return list(beneficiarios.values())