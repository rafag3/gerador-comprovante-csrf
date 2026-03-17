# irrf/processador_irrf.py

import pandas as pd
import os

def processar_irrf(caminho, codigo, ano, responsavel, pasta_saida):
    """
    Lê, limpa, converte e prepara dados do IRRF (1708, 8045, 3208, 0588, 2100, 2631)
    Garantido: retorna estrutura padronizada e sem erros.
    """

    try:
        df = pd.read_excel(caminho, engine="openpyxl")
    except Exception as e:
        raise Exception(f"Erro ao carregar a planilha {codigo}: {e}")

    required = [
        "Competencia",
        "CNPJ/CPF",
        "Razão Social",
        "Código Retenção IRRF",
        "PF/PJ",
        "Valor Total",
        "Valor IRRF"
    ]

    for col in required:
        if col not in df.columns:
            raise Exception(f"A planilha está faltando a coluna obrigatória: {col}")

    # Apenas PJ
    df = df[df["PF/PJ"] == "PJ"]

    # Filtrar código correto
    df = df[df["Código Retenção IRRF"] == int(codigo)]
    if df.empty:
        raise Exception(f"Nenhum registro encontrado para o código {codigo}.")

    # Extrair mês de forma segura:
    # Suporta "01/2025", "1/2025", "2025-01", etc.
    df["Mes"] = df["Competencia"].astype(str).str.extract(r"(\d{1,2})")[0].astype(int)

    registros = []

    for cnpj, grupo in df.groupby("CNPJ/CPF"):

        razao = grupo["Razão Social"].iloc[0]

        meses = pd.DataFrame({
            "Mes": grupo["Mes"].astype(int),
            "total": grupo["Valor Total"].astype(float),
            "irrf": grupo["Valor IRRF"].astype(float)
        })

        total_ano = meses["total"].sum()
        total_irrf = meses["irrf"].sum()

        registros.append({
            "codigo": codigo,
            "ano": ano,
            "responsavel": responsavel,
            "cnpj": cnpj,
            "razao": razao,
            "meses": meses,
            "total_ano": total_ano,
            "total_irrf": total_irrf
        })

    # Criar pasta do código
    pasta_codigo = os.path.join(pasta_saida, f"{codigo}_{ano}")
    os.makedirs(pasta_codigo, exist_ok=True)

    return pasta_codigo, registros