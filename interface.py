import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
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
        self.geometry("520x450")

        self.excel_path = None
        self.output_dir = None

        # TÍTULO
        titulo = ctk.CTkLabel(
            self,
            text="Gerador de Comprovantes CSRF",
            font=("Arial", 22, "bold")
        )
        titulo.pack(pady=(20, 10))

        # =========================
        # LOGO COM PROPORÇÃO CORRETA
        # =========================

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(BASE_DIR, "assets", "logo.png")

        logo_img = Image.open(logo_path)

        max_width = 260

        ratio = max_width / logo_img.width
        new_height = int(logo_img.height * ratio)

        logo_img = logo_img.resize((max_width, new_height))

        self.logo = ctk.CTkImage(
            light_image=logo_img,
            dark_image=logo_img,
            size=(max_width, new_height)
        )

        logo_label = ctk.CTkLabel(self, image=self.logo, text="")
        logo_label.pack(pady=10)

        # BOTÃO SELECIONAR EXCEL
        self.btn_excel = ctk.CTkButton(
            self,
            text="Selecionar Planilha Excel",
            command=self.selecionar_excel
        )
        self.btn_excel.pack(pady=10)

        # BOTÃO SELECIONAR PASTA
        self.btn_pasta = ctk.CTkButton(
            self,
            text="Escolher Pasta de Saída",
            command=self.selecionar_pasta
        )
        self.btn_pasta.pack(pady=10)

        # BOTÃO GERAR (VERMELHO)
        self.btn_gerar = ctk.CTkButton(
            self,
            text="Gerar Comprovantes",
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            command=self.gerar
        )
        self.btn_gerar.pack(pady=20)

        # STATUS
        self.status = ctk.CTkLabel(
            self,
            text="Selecione a planilha e a pasta de saída"
        )
        self.status.pack(pady=20)

    # =========================
    # SELECIONAR EXCEL
    # =========================

    def selecionar_excel(self):

        caminho = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.csv")]
        )

        if caminho:
            self.excel_path = caminho
            self.status.configure(text="Planilha selecionada com sucesso")

    # =========================
    # SELECIONAR PASTA
    # =========================

    def selecionar_pasta(self):

        pasta = filedialog.askdirectory()

        if pasta:
            self.output_dir = pasta
            self.status.configure(text="Pasta de saída selecionada")

    # =========================
    # GERAR PDFs
    # =========================

    def gerar(self):

        if not self.excel_path:
            self.status.configure(text="Selecione a planilha primeiro")
            return

        if not self.output_dir:
            self.status.configure(text="Escolha a pasta de saída")
            return

        self.status.configure(text="Processando comprovantes...")

        beneficiarios = processar_excel(self.excel_path)

        pasta_pdfs = os.path.join(self.output_dir, "pdfs")
        pasta_zip = os.path.join(self.output_dir, "zip")

        os.makedirs(pasta_pdfs, exist_ok=True)
        os.makedirs(pasta_zip, exist_ok=True)

        arquivos = []

        for b in beneficiarios:

            cnpj_limpo = (
                b["cnpj"]
                .replace(".", "")
                .replace("/", "")
                .replace("-", "")
            )

            nome_pdf = f"2025_{b['codigo']}_{cnpj_limpo}.pdf"

            caminho_pdf = os.path.join(pasta_pdfs, nome_pdf)

            gerar_pdf(b, caminho_pdf)

            arquivos.append(caminho_pdf)

        zip_path = os.path.join(pasta_zip, "comprovantes.zip")

        with zipfile.ZipFile(zip_path, "w") as z:
            for a in arquivos:
                z.write(a, os.path.basename(a))

        self.status.configure(text="ZIP criado com sucesso!")


if __name__ == "__main__":
    app = App()
    app.mainloop()