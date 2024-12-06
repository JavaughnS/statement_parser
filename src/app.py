import tkinter as tk
import customtkinter as ctk
from .input import Institutions, Accounts, AppInputs
from .run import begin_parse, clear_inputs

# Initialize customtkinter theme
ctk.set_appearance_mode("System")  # Light or Dark
ctk.set_default_color_theme("blue")  # Blue color theme

class StatementParserApp(ctk.CTk):
    def __init__(self):
        # trying to hide scrollbar and preserve scroll functionality
        # def on_scroll(event):
        #     self.path_entry.xview_scroll(int(-1 * (event.delta / 120)), "units")


        super().__init__()

        self.title("Statement Parser")
        self.geometry("720x540")

        self.institutions = [institution.value for institution in Institutions]
        self.accounts = [account.value[1] for account in Accounts]

        self.app_inputs = AppInputs()

        self.app_inputs.institution = ctk.StringVar(value="Make selection")
        self.app_inputs.account = ctk.StringVar(value="Make selection")
        self.app_inputs.pdf_path = ctk.StringVar()

        # Institutions dropdown
        self.institution_input_label = ctk.CTkLabel(self, text="Select an institution:")
        self.institution_input_label.pack(padx=100, pady=(50, 5), anchor="w")

        self.institution_dropdown = ctk.CTkComboBox(self, width=150, values=self.institutions, variable=self.app_inputs.institution)
        self.institution_dropdown.pack(padx=100, pady=(5, 20), anchor="w")

        # Accounts dropdown
        self.accounts_input_label = ctk.CTkLabel(self, text="Select an account:")
        self.accounts_input_label.pack(padx=100, pady=(20, 5), anchor="w")

        self.accounts_dropdown = ctk.CTkComboBox(self, width=150, values=self.accounts, variable=self.app_inputs.account)
        self.accounts_dropdown.pack(padx=100, pady=(5, 20), anchor="w")

        # Horizontally scrollable pdf path field
        self.string_input_label = ctk.CTkLabel(self, text="Enter the statement PDF path:")
        self.string_input_label.pack(padx=100, pady=(20, 5), anchor="w")

        self.path_entry_frame = ctk.CTkFrame(self)
        self.path_entry_frame.pack(padx=100, pady=5, anchor="w")
        self.path_entry = tk.Entry(self.path_entry_frame, textvariable=self.app_inputs.pdf_path, width=55)
        self.scrollbar = tk.Scrollbar(self.path_entry_frame, orient='horizontal', command=self.path_entry.xview)
        self.path_entry.config(xscrollcommand=self.scrollbar.set)
        self.path_entry.pack(side="top", fill="x")
        self.scrollbar.pack(side="bottom", fill="x")
        # self.scrollbar.pack_forget()
        # self.path_entry.bind("<Enter>", lambda e: self.path_entry.bind_all("<MouseWheel>", on_scroll))
        # self.path_entry.bind("<Leave>", lambda e: self.path_entry.unbind_all("<MouseWheel>"))

        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=30)

        self.parse_button = ctk.CTkButton(button_frame, text="Parse", command=lambda: begin_parse(self.app_inputs))
        self.clear_button = ctk.CTkButton(button_frame, text="Clear", command=lambda: clear_inputs(self.app_inputs))

        self.parse_button.grid(row=0, column=0, padx=(0, 70), sticky="w")
        self.clear_button.grid(row=0, column=1, padx=(70, 0), sticky="w")
