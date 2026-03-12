import customtkinter as ctk
from tkinter import filedialog
from processador_excel import processar_excel
from gerador_pdf import gerar_pdf
import os
import zipfile

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Gerador de Comprovantes CSRF")
        self.geometry("500x300")

        self.excel_path = None

        self.label = ctk.CTkLabel(
            self,
            text="Gerador de Comprovantes CSRF",
            font=("Arial", 20)
        )
        self.label.pack(pady=20)

        self.btn_excel = ctk.CTkButton(
            self,
            text="Selecionar Planilha Excel",
            command=self.selecionar_excel
        )
        self.btn_excel.pack(pady=10)

        self.btn_gerar = ctk.CTkButton(
            self,
            text="Gerar Comprovantes",
            command=self.gerar
        )
        self.btn_gerar.pack(pady=10)

        self.status = ctk.CTkLabel(self, text="")
        self.status.pack(pady=20)

    def selecionar_excel(self):

        caminho = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.csv")]
        )

        if caminho:
            self.excel_path = caminho
            self.status.configure(text=f"Planilha selecionada")

    def gerar(self):

        if not self.excel_path:
            self.status.configure(text="Selecione uma planilha primeiro")
            return

        self.status.configure(text="Processando...")

        beneficiarios = processar_excel(self.excel_path)

        os.makedirs("output/pdfs", exist_ok=True)
        os.makedirs("output/zip", exist_ok=True)

        arquivos = []

        for b in beneficiarios:

            cnpj_limpo = (
                b["cnpj"]
                .replace(".", "")
                .replace("/", "")
                .replace("-", "")
            )

            nome_pdf = f"2025_{b['codigo']}_{cnpj_limpo}.pdf"

            caminho_pdf = f"output/pdfs/{nome_pdf}"

            gerar_pdf(b, caminho_pdf)

            arquivos.append(caminho_pdf)

        zip_path = "output/zip/comprovantes.zip"

        with zipfile.ZipFile(zip_path, "w") as z:
            for a in arquivos:
                z.write(a, os.path.basename(a))

        self.status.configure(text="PDFs gerados com sucesso!")


if __name__ == "__main__":
    app = App()
    app.mainloop()