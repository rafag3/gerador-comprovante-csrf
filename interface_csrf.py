# interface_csrf.py

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

from utils_paths import data_path
from csrf.processador_csrf import processar_csrf
from csrf.gerador_pdf_csrf import gerar_pdf_csrf


class AppCSRF(ctk.CTk):
    def __init__(self, responsavel, ano):
        super().__init__()

        # TELA CHEIA
        self.state("zoomed")
        self.update_idletasks()

        self.title("Gerador de Comprovantes IRRF")
        self.geometry("1024x768")

        self.title("Gerador de Comprovantes CSRF")

        self.responsavel = responsavel
        self.ano = ano
        self.arquivo_excel = None
        self.pasta_saida = None

        # LOGO
        self._carregar_logo()

        titulo = ctk.CTkLabel(
            self,
            text=f"Gerador de Comprovantes CSRF – Ano {self.ano}",
            font=("Arial Black", 28, "bold")
        )
        titulo.pack(pady=(10, 20))

        btn_excel = ctk.CTkButton(
            self,
            text="Selecionar Planilha CSRF",
            width=280,
            command=self._selecionar_excel
        )
        btn_excel.pack(pady=10)

        btn_pasta = ctk.CTkButton(
            self,
            text="Selecionar Pasta de Saída",
            width=280,
            command=self._selecionar_pasta
        )
        btn_pasta.pack(pady=10)

        btn_gerar = ctk.CTkButton(
            self,
            text="GERAR COMPROVANTES",
            fg_color="#006600",
            hover_color="#004d00",
            width=350,
            height=50,
            command=self._gerar
        )
        btn_gerar.pack(pady=25)

        btn_voltar = ctk.CTkButton(
            self,
            text="← Voltar",
            width=160,
            fg_color="#666666",
            hover_color="#444444",
            command=self._voltar
        )
        btn_voltar.pack(pady=(5, 20))

        self.status = ctk.CTkLabel(self, text="", wraplength=700)
        self.status.pack(pady=10)

    # ------------------------------------------------------------------    
    # LOGO
    # ------------------------------------------------------------------
    def _carregar_logo(self):
        try:
            caminho = data_path("assets", "sompo_logo.png")
            img = Image.open(caminho)

            MAX_W, MAX_H = 260, 100
            w, h = img.size
            scale = min(MAX_W / w, MAX_H / h)

            self.logo_img = ctk.CTkImage(
                img, size=(int(w * scale), int(h * scale))
            )
            ctk.CTkLabel(self, image=self.logo_img, text="").pack(pady=10)

        except:
            ctk.CTkLabel(self, text="(Logo não encontrado)").pack(pady=10)

    # ------------------------------------------------------------------    
    def _selecionar_excel(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar arquivo CSRF",
            filetypes=[("Excel", "*.xlsx")]
        )
        if caminho:
            self.arquivo_excel = caminho
            self.status.configure(text=f"Planilha selecionada:\n{caminho}")

    # ------------------------------------------------------------------    
    def _selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecionar pasta de saída")
        if pasta:
            self.pasta_saida = pasta
            self.status.configure(text=f"Pasta de saída:\n{pasta}")

    # ------------------------------------------------------------------    
    def _gerar(self):
        if not self.arquivo_excel:
            self.status.configure(text="Selecione a planilha CSRF.")
            return

        if not self.pasta_saida:
            self.status.configure(text="Selecione a pasta de saída.")
            return

        self.status.configure(text="Processando...")

        registros = processar_csrf(
            self.arquivo_excel,
            self.ano,
            self.responsavel
        )

        pasta_pdf = os.path.join(self.pasta_saida, f"CSRF_{self.ano}")
        os.makedirs(pasta_pdf, exist_ok=True)

        for b in registros:
            cnpj_limpo = (
                b["cnpj"]
                .replace(".", "")
                .replace("/", "")
                .replace("-", "")
            )
            razao_limpa = b["nome"].replace(" ", "_")

            nome_pdf = f"{self.ano}_CSRF_{cnpj_limpo}_{razao_limpa}.pdf"
            gerar_pdf_csrf(b, os.path.join(pasta_pdf, nome_pdf))

        self.status.configure(text="Comprovantes CSRF gerados com sucesso!")

    # ------------------------------------------------------------------
    def _voltar(self):
        self.destroy()
        from app import TelaInicial
        TelaInicial().mainloop()