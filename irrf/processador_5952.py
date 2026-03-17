# irrf/processador_5952.py

import pandas as pd
import os

def ler_planilha_5952(caminho):
    """
    Lê a planilha do código 5952 (CSLL / COFINS / PIS/PASEP)
    De acordo com o layout REAL enviado pelo Rafael.
    """

    try:
        df = pd.read_excel(caminho, engine="openpyxl")
    except Exception as e:
        raise ValueError(f"Erro ao carregar planilha 5952: {e}")

    # COLUNAS REAIS (conforme imagem enviada pelo Rafael)
    required = [
        "Competencia",
        "CNPJ/CPF",
        "Razão Social",
        "Código Retenção CLL",
        "PF/PJ",
        "Valor Total",
        "CSRF"    # <- valor retido REAL
    ]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"Planilha 5952 está faltando a coluna: {col}")

    # Somente PJ
    df = df[df["PF/PJ"] == "PJ"]

    if df.empty:
        raise ValueError("Planilha 5952 não contém dados PJ.")

    return df


def agrupar_por_beneficiario(df, ano, responsavel):
    """
    Agrupa os dados por CNPJ (beneficiário), calcula totais
    e prepara estrutura para o gerador PDF.
    """

    # Extrair mês da competência ("01/2025" → 1)
    df["Mes"] = df["Competencia"].astype(str).str.extract(r"(\d{1,2})")[0].astype(int)

    resultados = []

    for cnpj, grupo in df.groupby("CNPJ/CPF"):

        razao = grupo["Razão Social"].iloc[0]

        meses = pd.DataFrame({
            "Mes": grupo["Mes"].astype(int),
            "valor_pago": grupo["Valor Total"].astype(float),
            "valor_retido": grupo["CSRF"].astype(float)   # <- USANDO VALOR REAL RETIDO
        })

        total_pago = meses["valor_pago"].sum()
        total_retido = meses["valor_retido"].sum()

        resultados.append({
            "codigo": "5952",
            "ano": ano,
            "responsavel": responsavel,
            "cnpj": cnpj,
            "razao": razao,
            "meses": meses,
            "total_pago": total_pago,
            "total_retido": total_retido
        })

    return resultados


def processar_5952(caminho, ano, responsavel, pasta_saida):
    """
    Processa a planilha 5952 e devolve pasta + dados estruturados.
    """

    df = ler_planilha_5952(caminho)
    dados = agrupar_por_beneficiario(df, ano, responsavel)

    pasta_codigo = os.path.join(pasta_saida, f"5952_{ano}")
    os.makedirs(pasta_codigo, exist_ok=True)

    return pasta_codigo, dados