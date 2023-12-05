import customtkinter

class CPFValidatorFrame(customtkinter.CTkFrame):
    def __init__(self, container: customtkinter.CTk):
        super().__init__(container, corner_radius=0, fg_color="transparent")

        self.grid(row=0, column=1, rowspan=5, sticky="nsew")

        customtkinter.CTkLabel(self, text="Validar CPF", font=customtkinter.CTkFont(size=25, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
      
        self.grid_columnconfigure(0, weight=1)