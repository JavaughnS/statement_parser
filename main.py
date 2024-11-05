import tkinter as tk
import customtkinter as ctk

# Initialize customtkinter theme
ctk.set_appearance_mode("System")  # Light or Dark
ctk.set_default_color_theme("blue")  # Blue color theme

class StatementParserApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Statement Parser")
        self.geometry("400x400")

        # Configure a grid for vertical centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Input 1: Dropdown with options a to d
        self.label1 = ctk.CTkLabel(self, text="Input 1")
        self.label1.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))

        self.option_var1 = ctk.StringVar(value="a")
        self.dropdown1 = ctk.CTkComboBox(self, values=["a", "b", "c", "d"], variable=self.option_var1)
        self.dropdown1.grid(row=0, column=1, sticky="w", padx=20, pady=(5, 20))

        # Input 2: Dropdown with options 1 to 3
        self.label2 = ctk.CTkLabel(self, text="Input 2")
        self.label2.grid(row=1, column=0, sticky="w", padx=20, pady=(20, 5))

        self.option_var2 = ctk.StringVar(value="1")
        self.dropdown2 = ctk.CTkComboBox(self, values=["1", "2", "3"], variable=self.option_var2)
        self.dropdown2.grid(row=1, column=1, sticky="w", padx=20, pady=(5, 20))

        # Input 3: Text input field
        self.label3 = ctk.CTkLabel(self, text="Input 3")
        self.label3.grid(row=2, column=0, sticky="w", padx=20, pady=(20, 5))

        self.text_entry = ctk.CTkEntry(self)
        self.text_entry.grid(row=2, column=1, sticky="w", padx=20, pady=(5, 20))

# Run the app
if __name__ == "__main__":
    app = StatementParserApp()
    app.mainloop()
