from time import sleep
import customtkinter
from tools.gui_tools import configure_int_only_entry, handle_exceptions
from rpc.client import Client

class CPFValidatorFrame(customtkinter.CTkFrame):
    def __init__(self, container: customtkinter.CTk, client: Client):
        super().__init__(container, width=960, corner_radius=0, fg_color="transparent")

        self.grid(row=0, column=1, rowspan=5, sticky="nsew")
        self.client = client

        customtkinter.CTkLabel(self, text="    Validar CPF    ", font=customtkinter.CTkFont(size=25, weight="bold")).grid(row=0, column=0, columnspan=6, pady=(20, 30), sticky="n")

        # Entrada
        customtkinter.CTkLabel(self, text="    Insira um CPF:", font=customtkinter.CTkFont(size=20, weight="normal")).grid(row=1, column=1, padx=60, pady=30, sticky = 'e')
        configure_int_only_entry(customtkinter.CTkEntry(self, width=250)).grid(row=1, column=3, padx=60)
        customtkinter.CTkButton(self, text="  Verificar  ", font=customtkinter.CTkFont(size=20, weight="normal"), command=self.check_cpf).grid(row=1, column=5, padx=60)

        # Resultado
        customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont(size=110, weight="bold")).grid(row=2, column=0, columnspan=6, pady=(70, 30), sticky="n")

    @handle_exceptions 
    def check_cpf(self):
        cpf = self.grid_slaves(row=1, column=3)[0].get()

        if cpf:
            isValid = self.client.validate_cpf(cpf)
            result = f"{'     VÁLIDO     ' if isValid else '     INVÁLIDO     '}"
            self.grid_slaves(row=2, column=0)[0].configure(text = result, text_color= "green" if isValid else "red")  
