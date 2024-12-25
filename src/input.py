import customtkinter as ctk

class AppInputs:
    def __init__(self):
        self.target = ctk.StringVar()
        self.institution = ctk.StringVar()
        self.table_settings = ctk.StringVar()
        self.scan_mode = ctk.IntVar(value=0)
        self.column_count = ctk.IntVar(value="")
        self.pdf_path = ctk.StringVar()

        self.out_path_settings = ctk.StringVar(value="DEFAULT")
        self.statement_month = ctk.StringVar()
        self.statement_year = ctk.StringVar()
        self.account_type = ctk.StringVar()
        self.output_type = ctk.StringVar()
        self.output_filepath = ctk.StringVar()
