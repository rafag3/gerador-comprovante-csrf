# app.py

import customtkinter as ctk
from PIL import Image
from utils_paths import data_path

from interface_csrf import AppCSRF
from irrf.interface_irrf import AppIRRF

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class TelaInicial(ctk.CTk):
    def __init__(self):
        super().__init__()
    
        self.title("Gerador de Comprovantes")
        self.geometry("1024x768")

        # Variáveis globais para ano e responsável (serão enviadas aos módulos)
        self.responsavel_var = ctk.StringVar()
        self.ano_var = ctk.StringVar()

        # =========================
        # LOGO
        # =========================
        self.carregar_logo()

        # =========================
        # TÍTULO
        # =========================
        titulo = ctk.CTkLabel(
            self,
            text="Gerador de Comprovantes",
            font=("Arial Black", 28, "bold")
        )
        titulo.pack(pady=(5, 25))

        # =========================
        # FRAME CENTRAL
        # =========================
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=(10, 20))

        # =========================
        # CAMPO RESPONSÁVEL
        # =========================
        lbl_resp = ctk.CTkLabel(
            frame,
            text="Responsável pelas Informações:",
            font=("Arial", 16)
        )
        lbl_resp.grid(row=0, column=0, sticky="w", pady=5)

        txt_resp = ctk.CTkEntry(
            frame,
            width=380,
            textvariable=self.responsavel_var,
            placeholder_text="Digite o nome do responsável"
        )
        txt_resp.grid(row=1, column=0, pady=5)

        # =========================
        # CAMPO ANO-CALENDÁRIO
        # =========================
        lbl_ano = ctk.CTkLabel(
            frame,
            text="Ano-calendário:",
            font=("Arial", 16)
        )
        lbl_ano.grid(row=2, column=0, sticky="w", pady=(20, 5))

        anos = [str(a) for a in range(2018, 2035)]
        ano_combo = ctk.CTkComboBox(
            frame,
            values=anos,
            variable=self.ano_var,
            width=150
        )
        ano_combo.grid(row=3, column=0, pady=5)
        self.ano_var.set("2025")  # valor padrão

        # =========================
        # BOTÃO CSRF
        # =========================
        btn_csrf = ctk.CTkButton(
            self,
            text="Gerar Comprovantes CSRF",
            width=300,
            height=50,
            command=self.abrir_csrf
        )
        btn_csrf.pack(pady=15)

        # =========================
        # BOTÃO IRRF / 5952
        # =========================
        btn_irrf = ctk.CTkButton(
            self,
            text="Gerar Comprovantes IRRF (inclui 5952)",
            fg_color="#003A8C",
            hover_color="#002B66",
            width=300,
            height=50,
            command=self.abrir_irrf
        )
        btn_irrf.pack(pady=15)

    # =============================================================
    # CARREGAR LOGO
    # =============================================================
    def carregar_logo(self):
        try:
            logo_path = data_path("assets", "sompo_logo.png")
            img = Image.open(logo_path)

            MAX_W, MAX_H = 250, 100
            w, h = img.size
            scale = min(MAX_W / w, MAX_H / h)

            self.logo_img = ctk.CTkImage(
                light_image=img,
                size=(int(w * scale), int(h * scale))
            )

            ctk.CTkLabel(self, image=self.logo_img, text="").pack(pady=15)

        except Exception as e:
            ctk.CTkLabel(self, text="(Logo não encontrado)").pack(pady=10)
            print("Erro ao carregar logo:", e)

    # =============================================================
    # ABRIR TELAS
    # =============================================================
    def abrir_csrf(self):
        if not self.validar_campos():
            return
        self.destroy()
        AppCSRF(
            responsavel=self.responsavel_var.get(),
            ano=self.ano_var.get()
        ).mainloop()

    def abrir_irrf(self):
        if not self.validar_campos():
            return
        self.destroy()
        AppIRRF(
            responsavel=self.responsavel_var.get(),
            ano=self.ano_var.get()
        ).mainloop()

    # =============================================================
    # VALIDAR CAMPOS
    # =============================================================
    def validar_campos(self):
        if not self.responsavel_var.get().strip():
            ctk.CTkMessagebox(title="Erro",
                              message="Digite o nome do responsável antes de prosseguir.",
                              icon="cancel")
            return False
        if not self.ano_var.get().isdigit():
            ctk.CTkMessagebox(title="Erro",
                              message="Selecione um ano válido.",
                              icon="cancel")
            return False
        return True


if __name__ == "__main__":
    TelaInicial().mainloop()