import customtkinter

class TopLevelPopUp(customtkinter.CTkToplevel):
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.geometry("600x150")
        self.title("ERRO")
        self.resizable(False, False)

        self.label = customtkinter.CTkLabel(self, text=message)
        self.label.pack(padx=20, pady=20)

        close_button = customtkinter.CTkButton(self, text="Fechar", command=self.destroy)
        close_button.pack(pady=10)

        self.grab_set()
        self.wait_window()