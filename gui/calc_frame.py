import customtkinter
from tools.gui_tools import configure_float_only_entry, handle_exceptions
from rpc.client import Client

class CalcFrame(customtkinter.CTkFrame):
    def __init__(self, container: customtkinter.CTk, client: Client):
        super().__init__(container, width=960, corner_radius=0, fg_color="transparent")

        self.grid(row=0, column=1, rowspan=5, sticky="nsew")
        self.client = client

        customtkinter.CTkLabel(self, text="Calculadora", font=customtkinter.CTkFont(size=25, weight="bold")).grid(row=0, column=0, columnspan=6, padx=5, pady=(20, 30), sticky="n")

        # Soma
        customtkinter.CTkLabel(self, text="Somar:", font=customtkinter.CTkFont(size=20, weight="normal")).grid(row=1, column=0, padx=20, pady=30, sticky = 'e')
        configure_float_only_entry(customtkinter.CTkEntry(self, placeholder_text="Parcela")).grid(row=1, column=1, padx=20)
        customtkinter.CTkLabel(self, text="+", font=customtkinter.CTkFont(size=20, weight="normal")).grid(row=1, column=2, padx=20)
        configure_float_only_entry(customtkinter.CTkEntry(self, placeholder_text="Parcela")).grid(row=1, column=3, padx=20)
        customtkinter.CTkButton(self, text="=", font=customtkinter.CTkFont(size=20, weight="normal"), command=self.sum_and_update).grid(row=1, column=4, padx=20)
        customtkinter.CTkEntry(self, placeholder_text="Total").grid(row=1, column=5, padx=20)

        # Subtração
        customtkinter.CTkLabel(self, text="Subtrair:", font=customtkinter.CTkFont(size=20, weight="normal")).grid(row=2, column=0, padx=20, pady=30, sticky = 'e')
        configure_float_only_entry(customtkinter.CTkEntry(self, placeholder_text="Minuendo")).grid(row=2, column=1, padx=20)
        customtkinter.CTkLabel(self, text="-", font=customtkinter.CTkFont(size=20, weight="normal")).grid(row=2, column=2, padx=20)
        configure_float_only_entry(customtkinter.CTkEntry(self, placeholder_text="Subtraendo")).grid(row=2, column=3, padx=20)
        customtkinter.CTkButton(self, text="=", font=customtkinter.CTkFont(size=20, weight="normal"), command=self.sub_and_update).grid(row=2, column=4, padx=20)
        customtkinter.CTkEntry(self, placeholder_text="Diferença").grid(row=2, column=5, padx=20)

        # Multiplicação
        customtkinter.CTkLabel(self, text="Multiplicar:", font=customtkinter.CTkFont(size=20, weight="normal")).grid(row=3, column=0, padx=20, pady=30, sticky = 'e')
        configure_float_only_entry(customtkinter.CTkEntry(self, placeholder_text="Fator")).grid(row=3, column=1, padx=20)
        customtkinter.CTkLabel(self, text="x", font=customtkinter.CTkFont(size=20, weight="normal")).grid(row=3, column=2, padx=20)
        configure_float_only_entry(customtkinter.CTkEntry(self, placeholder_text="Fator")).grid(row=3, column=3, padx=20)
        customtkinter.CTkButton(self, text="=", font=customtkinter.CTkFont(size=20, weight="normal"), command=self.mul_and_update).grid(row=3, column=4, padx=20)
        customtkinter.CTkEntry(self, placeholder_text="Produto").grid(row=3, column=5, padx=20)

        # Divisão
        customtkinter.CTkLabel(self, text="Dividir:", font=customtkinter.CTkFont(size=20, weight="normal")).grid(row=4, column=0, padx=20, pady=30, sticky = 'e')
        configure_float_only_entry(customtkinter.CTkEntry(self, placeholder_text="Fator")).grid(row=4, column=1, padx=20)
        customtkinter.CTkLabel(self, text="/", font=customtkinter.CTkFont(size=20, weight="normal")).grid(row=4, column=2, padx=20)
        configure_float_only_entry(customtkinter.CTkEntry(self, placeholder_text="Fator")).grid(row=4, column=3, padx=20)
        customtkinter.CTkButton(self, text="=", font=customtkinter.CTkFont(size=20, weight="normal"), command=self.div_and_update).grid(row=4, column=4, padx=20)
        customtkinter.CTkEntry(self, placeholder_text="Quociente").grid(row=4, column=5, padx=20)

    @handle_exceptions 
    def sum_and_update(self):
        n1 = self.grid_slaves(row=1, column=1)[0].get()
        n2 = self.grid_slaves(row=1, column=3)[0].get()

        if n1 and n2:
            result_entry = self.grid_slaves(row=1, column=5)[0]  
            result_entry.delete(0, "end")
            result_entry.insert(0, str(self.client.sum(float(n1), float(n2))))

    @handle_exceptions
    def sub_and_update(self):
        n1 = self.grid_slaves(row=2, column=1)[0].get()
        n2 = self.grid_slaves(row=2, column=3)[0].get()

        if n1 and n2:
            result_entry = self.grid_slaves(row=2, column=5)[0]  
            result_entry.delete(0, "end")
            result_entry.insert(0, str(self.client.sub(float(n1), float(n2))))

    @handle_exceptions
    def mul_and_update(self):
        n1 = self.grid_slaves(row=3, column=1)[0].get()
        n2 = self.grid_slaves(row=3, column=3)[0].get()

        if n1 and n2:
            result_entry = self.grid_slaves(row=3, column=5)[0]  
            result_entry.delete(0, "end")
            result_entry.insert(0, str(self.client.mul(float(n1), float(n2))))

    @handle_exceptions
    def div_and_update(self):
        n1 = self.grid_slaves(row=4, column=1)[0].get()
        n2 = self.grid_slaves(row=4, column=3)[0].get()

        if n1 and n2:
            result_entry = self.grid_slaves(row=4, column=5)[0]  
            result_entry.delete(0, "end")
            result_entry.insert(0, str(self.client.div(float(n1), float(n2))))

    
    