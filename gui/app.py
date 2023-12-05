import customtkinter
from gui.calc_frame import CalcFrame
from gui.cpf_frame import CPFValidatorFrame
from gui.news_frame import LastNewsFrame
from gui.prime_frame import PrimeFrame
from rpc.client import Client

PATH_COLOR_THEME = "gui/color_theme.json"
APPEARANCE_MODE = "Light" # "Dark" | "Light" | "System"
WINDOW_RESOLUTION = f"{1100}x{580}"
WINDOW_TITLE = "RPC - Cliente"

APPEARANCE_MODE_OPTIONS_TRANSLATE = ["Claro", "Escuro", "Do Sistema"]

customtkinter.set_appearance_mode(APPEARANCE_MODE)
customtkinter.set_default_color_theme(PATH_COLOR_THEME)

class App(customtkinter.CTk):
    def __init__(self, client: Client):
        super().__init__()

        self.geometry(WINDOW_RESOLUTION)
        self.title(WINDOW_TITLE)

        # Cliente RPC
        self.client = client

        # Evita redimensionamento da janela
        self.resizable(False, False)

        # configure grid layout (4x4)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Barra lateral
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Cliente RPC", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_calc = customtkinter.CTkButton(self.sidebar_frame, text = "Calculadora", command = self.show_calc_content)
        self.sidebar_button_calc.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_prime = customtkinter.CTkButton(self.sidebar_frame, text = "Números Primos", command = self.show_prime_content)
        self.sidebar_button_prime.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_last_news = customtkinter.CTkButton(self.sidebar_frame, text = "Notícias IFET", command = self.show_news_content)
        self.sidebar_button_last_news.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_verify_cpf = customtkinter.CTkButton(self.sidebar_frame, text = "Validar CPF", command = self.show_cpf_validator_content)
        self.sidebar_button_verify_cpf.grid(row=4, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Alterar Tema:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=APPEARANCE_MODE_OPTIONS_TRANSLATE,
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=7, column=0, padx=20, pady=(10, 10))

        self.main_content_frame = customtkinter.CTkFrame(self)
        self.show_calc_content()

    def show_calc_content(self):
        self.clear_main_content()
        self.main_content_frame = CalcFrame(self, self.client)

    def show_prime_content(self):
        self.clear_main_content()
        self.main_content_frame = PrimeFrame(self, self.client)

    def show_news_content(self):
        self.clear_main_content()
        self.main_content_frame = LastNewsFrame(self, self.client)

    def show_cpf_validator_content(self):
        self.clear_main_content()
        self.main_content_frame = CPFValidatorFrame(self)

    def clear_main_content(self):
        # Limpa o conteúdo atual do main_content_frame
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        map = {"Claro": "Light", "Escuro": "Dark", "Do Sistema": "System"}
        customtkinter.set_appearance_mode(map.get(new_appearance_mode, new_appearance_mode))