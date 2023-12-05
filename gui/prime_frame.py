import customtkinter
from tools.gui_tools import configure_int_only_entry, handle_exceptions
from rpc.client import Client

class PrimeFrame(customtkinter.CTkFrame):
    def __init__(self, container: customtkinter.CTk, client: Client):
        super().__init__(container, width=960, corner_radius=0, fg_color="transparent")

        self.grid(row=0, column=1, rowspan=5, sticky="nsew")
        self.client = client

        customtkinter.CTkLabel(self, text="Números Primos entre 0 e N", font=customtkinter.CTkFont(size=25, weight="bold")).grid(row=0, column=0, columnspan=6, pady=(20, 30), sticky="n")

        # Entrada
        customtkinter.CTkLabel(self, text="Forneça um número inteiro N:", font=customtkinter.CTkFont(size=20, weight="normal")).grid(row=1, column=1, padx=60, pady=30, sticky = 'e')
        configure_int_only_entry(customtkinter.CTkEntry(self)).grid(row=1, column=3, padx=60)
        customtkinter.CTkButton(self, text="Verificar", font=customtkinter.CTkFont(size=20, weight="normal"), command=self.get_primes).grid(row=1, column=5, padx=60)

        # Text box
        # create scrollable textbox
        tk_textbox = customtkinter.CTkTextbox(self, activate_scrollbars=False)
        tk_textbox.grid(row=2, column=0, columnspan=6, sticky="nsew")

        # create CTk scrollbar
        ctk_textbox_scrollbar = customtkinter.CTkScrollbar(self, command=tk_textbox.yview)
        ctk_textbox_scrollbar.grid(row=2, column=6, sticky="ns")

        # connect textbox scroll event to CTk scrollbar
        tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

    @handle_exceptions 
    def get_primes(self):
        n = self.grid_slaves(row=1, column=3)[0].get()

        if n:
            values = [i for i in range(0, int(n))]
            m_res = self.client.is_prime_multiprocess(*values)

            result = "".join([f"{num},  " for num, is_prime in m_res if is_prime])

            text_box = self.grid_slaves(row=2, column=0)[0]  
            text_box.delete(1.0, customtkinter.END)
            text_box.insert(customtkinter.END, result)