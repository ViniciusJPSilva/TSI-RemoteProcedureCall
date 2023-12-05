import tkinter as tk
import customtkinter


app = customtkinter.CTk()
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# create scrollable textbox
tk_textbox = customtkinter.CTkTextbox(app, activate_scrollbars=False)
tk_textbox.grid(row=0, column=0, sticky="nsew")

# create CTk scrollbar
ctk_textbox_scrollbar = customtkinter.CTkScrollbar(app, command=tk_textbox.yview)
ctk_textbox_scrollbar.grid(row=0, column=1, sticky="ns")

# connect textbox scroll event to CTk scrollbar
tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

app.mainloop()