# irrf/interface_irrf.py

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

from utils_paths import data_path
from .processador_irrf import processar_irrf
from .processador_5952 import processar_5952
from .gerador_pdf_irrf import gerar_irrf_pdf
from .gerador_pdf_5952 import gerar_pdf_5952


class AppIRRF(ctk.CTk):
    def __init__(self, responsavel, ano):
        super().__init__()
        
        self.state("zoomed")          # ← TELA CHEIA
        self.update_idletasks()       # ← GARANTE APLICAR IMEDIATO
        
        self.title("Gerador de Comprovantes IRRF")
        self.geometry("1024x768")

        self.responsavel = responsavel
        self.ano = ano
        self.pasta_saida = None

        self.codigos_irrf = ["1708", "8045", "3208", "0588", "2100", "2631"]
        self.codigo_5952 = "5952"

        self.arquivos = {c: None for c in self.codigos_irrf + [self.codigo_5952]}
        self.chk_vars = {c: ctk.BooleanVar() for c in self.arquivos}

        # =============================================================
        # LOGO
        # =============================================================
        self._carregar_logo()

        # =============================================================
        # ÁREA SCROLL
        # =============================================================
        scroll = ctk.CTkScrollableFrame(self, width=820, height=650)
        scroll.pack(pady=10, padx=10, fill="both", expand=True)

        # =============================================================
        # TÍTULO
        # =============================================================
        titulo = ctk.CTkLabel(
            scroll,
            text=f"Gerador de Informes – Ano-calendário {self.ano}",
            font=("Arial Black", 28, "bold")
        )
        titulo.pack(pady=(5, 20))

        # =============================================================
        # BLOCO IRRF
        # =============================================================
        ctk.CTkLabel(
            scroll,
            text="RETENÇÃO DE IRRF – IN/SRF nº 119/2000",
            font=("Arial Black", 22)
        ).pack(pady=(10, 10))

        for codigo, desc in [
            ("1708", "Serviços Profissionais"),
            ("8045", "Comissões e Corretagens / Propaganda"),
            ("3208", "Aluguéis / Royalties (PJ)"),
            ("0588", "Serviços de Natureza Especializada"),
            ("2100", "Serviços de Propaganda"),
            ("2631", "Cooperativas / Obras"),
        ]:
            self._criar_check(scroll, codigo, desc)

        # SEPARADOR
        ctk.CTkLabel(scroll, text="─" * 100).pack(pady=20)

        # =============================================================
        # BLOCO 5952
        # =============================================================
        ctk.CTkLabel(
            scroll,
            text="RETENÇÃO CSLL / COFINS / PIS – Lei 10.833/2003",
            font=("Arial Black", 22)
        ).pack(pady=(10, 10))

        self._criar_check(scroll, "5952", "CSLL / COFINS / PIS – Código 5952")

        # =============================================================
        # BOTÃO DE PASTA
        # =============================================================
        self.btn_pasta = ctk.CTkButton(
            scroll,
            text="Selecionar Pasta de Saída",
            width=350,
            height=50,
            command=self._selecionar_pasta
        )
        self.btn_pasta.pack(pady=25)

        # =============================================================
        # GERAR
        # =============================================================
        btn_gerar = ctk.CTkButton(
            scroll,
            text="GERAR COMPROVANTES",
            fg_color="#006600",
            hover_color="#004d00",
            width=400,
            height=60,
            command=self._gerar
        )
        btn_gerar.pack(pady=20)

        # =============================================================
        # VOLTAR
        # =============================================================
        btn_voltar = ctk.CTkButton(
            scroll,
            text="← Voltar",
            fg_color="#666666",
            hover_color="#444444",
            width=160,
            height=45,
            command=self._voltar
        )
        btn_voltar.pack(pady=(10, 20))

        # STATUS
        self.status = ctk.CTkLabel(scroll, text="", wraplength=760)
        self.status.pack(pady=10)



    # =============================================================
    # Carregar logomarca
    # =============================================================
    def _carregar_logo(self):
        try:
            caminho = data_path("assets", "sompo_logo.png")
            img = Image.open(caminho)

            MAX_W, MAX_H = 260, 110
            w, h = img.size
            scale = min(MAX_W / w, MAX_H / h)

            self.logo_img = ctk.CTkImage(img, size=(int(w*scale), int(h*scale)))
            ctk.CTkLabel(self, image=self.logo_img, text="").pack(pady=15)

        except:
            ctk.CTkLabel(self, text="(Logo não encontrado)").pack(pady=15)



    # =============================================================
    # Criar checkbox + botão
    # =============================================================
    def _criar_check(self, parent, codigo, descricao):

        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=8)

        chk = ctk.CTkCheckBox(
            frame,
            text=f"{codigo} – {descricao}",
            variable=self.chk_vars[codigo],
            command=lambda c=codigo: self._toggle_btn(c)
        )
        chk.pack(anchor="center")

        btn = ctk.CTkButton(
            frame,
            text=f"Selecionar arquivo {codigo}",
            width=260,
            command=lambda c=codigo: self._selecionar_arquivo(c)
        )
        btn.pack(pady=5)
        btn.pack_forget()

        self.chk_vars[codigo].btn = btn



    def _toggle_btn(self, codigo):
        if self.chk_vars[codigo].get():
            self.chk_vars[codigo].btn.pack(pady=5)
        else:
            self.chk_vars[codigo].btn.pack_forget()
            self.arquivos[codigo] = None



    def _selecionar_arquivo(self, codigo):

        caminho = filedialog.askopenfilename(
            title=f"Selecionar arquivo {codigo}",
            filetypes=[("Excel", "*.xlsx")]
        )
        if caminho:
            self.arquivos[codigo] = caminho
            self.status.configure(text=f"Arquivo selecionado para {codigo}:\n{caminho}")


    def _selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta de saída")
        if pasta:
            self.pasta_saida = pasta
            self.status.configure(text=f"Pasta de saída:\n{pasta}")



    # =============================================================
    # MAPA DE DESCRIÇÃO DOS CÓDIGOS IRRF
    # =============================================================
    def _descricao_codigo(self, codigo):

        descricoes = {
            "1708": "Remuneração de serviços profissionais prestados por Pessoa Jurídica",
            "8045": "Comissões e corretagens pagos a PJ e serviços de propaganda prestados por PJ",
            "3208": "Royalties, aluguéis e rendimentos do capital pagos a PJ",
            "0588": "Serviços de natureza especializada prestados por PJ",
            "2100": "Pagamentos por serviços de propaganda e publicidade",
            "2631": "Serviços prestados por cooperativas"
        }
        return descricoes.get(codigo, "Descrição não encontrada")



    # =============================================================
    # GERAR PDFs (SEM TRY/EXCEPT)
    # =============================================================
    def _gerar(self):

        selecionados = [c for c,v in self.chk_vars.items() if v.get()]

        if not selecionados:
            self.status.configure(text="Selecione ao menos um código.")
            return

        if not self.pasta_saida:
            self.status.configure(text="Selecione a pasta de saída.")
            return

        self.status.configure(text="Processando... Aguarde.")
        self.update_idletasks()


        # -------------------------
        # IRRF – Layout 8045
        # -------------------------
        for codigo in self.codigos_irrf:

            if codigo in selecionados and self.arquivos[codigo]:

                pasta_codigo, registros = processar_irrf(
                    caminho=self.arquivos[codigo],
                    codigo=codigo,
                    ano=self.ano,
                    responsavel=self.responsavel,
                    pasta_saida=self.pasta_saida
                )

                for item in registros:

                    item["descricao"] = self._descricao_codigo(codigo)

                    cnpj = item["cnpj"].replace(".", "").replace("/", "").replace("-", "")

                    nome_pdf = f"1 - Informes de Rendimentos_{codigo}_{cnpj}.pdf"
                    caminho_pdf = os.path.join(pasta_codigo, nome_pdf)

                    print("Gerando PDF IRRF:", caminho_pdf)
                    gerar_irrf_pdf(item, caminho_pdf)
                    print("PDF IRRF gerado com sucesso:", caminho_pdf)


        # -------------------------
        # 5952 – Layout exclusivo
        # -------------------------
        if "5952" in selecionados and self.arquivos["5952"]:

            pasta_codigo, registros5952 = processar_5952(
                caminho=self.arquivos["5952"],
                ano=self.ano,
                responsavel=self.responsavel,
                pasta_saida=self.pasta_saida
            )

            for item in registros5952:

                cnpj = item["cnpj"].replace(".", "").replace("/", "").replace("-", "")
                razao = item["razao"].replace(" ", "_").replace("/", "_")

                nome_pdf = f"{item['ano']}_5952_{cnpj}_{razao}.pdf"
                caminho_pdf = os.path.join(pasta_codigo, nome_pdf)

                print("Gerando PDF 5952:", caminho_pdf)
                gerar_pdf_5952(item, caminho_pdf)
                print("PDF 5952 gerado:", caminho_pdf)


        self.status.configure(text="Gerado com sucesso!")



    def _voltar(self):
        self.destroy()
        from app import TelaInicial
        TelaInicial().mainloop()