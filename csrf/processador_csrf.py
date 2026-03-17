# csrf/processador_csrf.py

import pandas as pd

def processar_csrf(caminho_excel, ano, responsavel):
    """
    Processa planilha CSRF no layout Sompo:
    - Competencia
    - CNPJ/CPF
    - Razão Social
    - PF/PJ
    - Valor Total
    - Valor INSS
    """

    try:
        df = pd.read_excel(caminho_excel, engine="openpyxl")
    except Exception as e:
        raise Exception(f"Erro ao ler planilha CSRF: {e}")

    required = [
        "Competencia",
        "CNPJ/CPF",
        "Razão Social",
        "PF/PJ",
        "Valor Total",
        "Valor INSS"
    ]

    for col in required:
        if col not in df.columns:
            raise Exception(f"Coluna ausente no CSRF: {col}")

    df = df[df["PF/PJ"] == "PJ"]

    registros = []

    for cnpj, grupo in df.groupby("CNPJ/CPF"):

        nome = grupo["Razão Social"].iloc[0]

        meses = []
        total_r = 0
        total_inss = 0

        for _, linha in grupo.iterrows():

            comp = linha["Competencia"]
            vtotal = float(linha["Valor Total"])
            vinss = float(linha["Valor INSS"])

            meses.append({
                "competencia": comp,
                "valor_total": vtotal,
                "valor_inss": vinss
            })

            total_r += vtotal
            total_inss += vinss

        registros.append({
            "ano": ano,
            "responsavel": responsavel,
            "nome": nome,
            "cnpj": cnpj,
            "meses": meses,
            "total_rendimento": total_r,
            "total_retencao": total_inss
        })

    return registros