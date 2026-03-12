from processador_excel import processar_excel
from gerador_pdf import gerar_pdf
import os
import zipfile
import re

EXCEL = "input/dados.xlsx"

# Processar Excel
beneficiarios = processar_excel(EXCEL)

# Criar pastas de saída
os.makedirs("output/pdfs", exist_ok=True)
os.makedirs("output/zip", exist_ok=True)

arquivos = []

for b in beneficiarios:

    # limpar CNPJ para usar no nome do arquivo
    cnpj_limpo = re.sub(r"\D", "", b["cnpj"])

    nome_pdf = f"2025_{b['codigo']}_{cnpj_limpo}.pdf"

    caminho_pdf = f"output/pdfs/{nome_pdf}"

    print(f"Gerando PDF: {nome_pdf}")

    gerar_pdf(b, caminho_pdf)

    arquivos.append(caminho_pdf)

# Criar ZIP final
zip_path = "output/zip/comprovantes.zip"

with zipfile.ZipFile(zip_path, "w") as z:

    for a in arquivos:
        z.write(a, os.path.basename(a))

print("\nPDFs gerados com sucesso")
print("ZIP criado:", zip_path)