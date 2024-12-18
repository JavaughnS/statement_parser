import customtkinter as ctk
from .input import AppInputs
from .constants import ACCOUNT, MONTHS, NETWORK, OUTPUT_TYPES, TARGETS
from .run import begin_parse, clear_inputs

# Initialize customtkinter theme
ctk.set_appearance_mode("System")  # Light or Dark
ctk.set_default_color_theme("blue")  # Blue color theme

class StatementParserApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Statement Parser")
        self.geometry("960x540")
        self.grid_columnconfigure(0, weight=1)  # Allow resizing for main column
        self.grid_rowconfigure(0, weight=1)  # Allow resizing for main row

        self.targets = [target for target in TARGETS]
        self.statement_months = [month for month in MONTHS]
        self.output_types = [file_type for file_type in OUTPUT_TYPES]
        self.account_types = [account for account in ACCOUNT]
        self.card_types = [card for card in NETWORK]

        self.app_inputs = AppInputs()

        # Scrollable Frame to hold all content
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)  # Allow content to stretch

        # Create sections inside the scrollable frame
        self.create_statement_info_section()
        self.create_output_info_section()
        self.create_buttons()


    def toggle_field_states(self, caller: str):
        if caller == "TARGET":
            target = self.app_inputs.target.get()

            if target == "CUSTOM":
                statement_info_state = "normal"
                foreground = "white"
                txt_color = "black"
                self.table_settings_textbox.configure(state=statement_info_state, fg_color=foreground, text_color=txt_color)
            else:
                statement_info_state = "disabled"
                foreground = "gray"
                txt_color = "darkgray"
                self.table_settings_textbox.configure(state=statement_info_state, fg_color=foreground, text_color=txt_color)
            
            self.bank_name_entry.configure(state=statement_info_state, fg_color=foreground, text_color=txt_color)
            self.column_count_entry.configure(state=statement_info_state, fg_color=foreground, text_color=txt_color)
            self.scan_mode_radio_one.configure(state=statement_info_state, fg_color=foreground, text_color=txt_color)
            self.scan_mode_radio_two.configure(state=statement_info_state, fg_color=foreground, text_color=txt_color)

        elif caller == "OUTPUT_SETTINGS":
            settings = self.app_inputs.out_path_settings.get()

            if settings == "DEFAULT":
                self.statement_month_combobox.configure(state="readonly", fg_color="white", text_color="black")
                self.statement_year_entry.configure(state="normal", fg_color="white", text_color="black")
                self.account_type_combobox.configure(state="readonly", fg_color="white", text_color="black")
                self.card_type_combobox.configure(state="readonly", fg_color="white", text_color="black")
                self.out_file_type_combobox.configure(state="readonly", fg_color="white", text_color="black")
                self.out_path_entry.configure(state="disabled", fg_color="gray", text_color="darkgray")
            else:
                self.statement_month_combobox.configure(state="disabled", fg_color="gray", text_color="darkgray")
                self.statement_year_entry.configure(state="disabled", fg_color="gray", text_color="darkgray")
                self.account_type_combobox.configure(state="disabled", fg_color="gray", text_color="darkgray")
                self.card_type_combobox.configure(state="disabled", fg_color="gray", text_color="darkgray")
                self.out_file_type_combobox.configure(state="disabled", fg_color="gray", text_color="darkgray")
                self.out_path_entry.configure(state="normal", fg_color="white", text_color="black")


    def create_statement_info_section(self):
        statement_info_frame = ctk.CTkFrame(self.scrollable_frame)
        statement_info_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        statement_info_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(statement_info_frame, text="Bank Statement Info").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )

        # Target Selection
        ctk.CTkLabel(statement_info_frame, text="Select a target:").grid(
            row=1, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.target_combobox = ctk.CTkComboBox(
            statement_info_frame, values=self.targets, width=200,
            variable=self.app_inputs.target,
            state="readonly",
            command=lambda x: self.toggle_field_states("TARGET")
        )
        self.target_combobox.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Bank Name Entry
        ctk.CTkLabel(statement_info_frame, text="Enter your institution's name:").grid(
            row=3, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.bank_name_entry = ctk.CTkEntry(
            statement_info_frame, textvariable=self.app_inputs.institution, state="disabled"
        )
        self.bank_name_entry.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # Column Count Entry
        ctk.CTkLabel(statement_info_frame, text="Enter the number of columns your statement's records table has:").grid(
            row=5, column=0, padx=10, pady=(10, 5), sticky="w")
        self.column_count_entry = ctk.CTkEntry(
            statement_info_frame, textvariable=self.app_inputs.column_count, state="disabled"
        )
        self.column_count_entry.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

        # Table Settings Entry
        ctk.CTkLabel(statement_info_frame, text="Enter the JSON for your custom target:").grid(
            row=7, column=0, padx=10, pady=(10, 5), sticky="w")

        self.table_settings_frame = ctk.CTkFrame(statement_info_frame)
        self.table_settings_frame.grid(row=8, column=0, padx=10, pady=5, sticky="ew")
        self.table_settings_frame.grid_columnconfigure(0, weight=1)

        self.table_settings_textbox = ctk.CTkTextbox(self.table_settings_frame, height=100)
        self.table_settings_textbox.insert("1.0", "{\n    // Enter JSON here\n}")
        self.table_settings_textbox.configure(state="disabled")
        self.table_settings_textbox.grid(row=0, column=0, sticky="nsew")

        table_settings_textbox_scrollbar = ctk.CTkScrollbar(
            self.table_settings_frame, orientation="vertical", command=self.table_settings_textbox.yview
        )
        table_settings_textbox_scrollbar.grid(row=0, column=1, sticky="ns")
        self.table_settings_textbox.configure(yscrollcommand=table_settings_textbox_scrollbar.set)

        # Scan Mode Selection
        ctk.CTkLabel(statement_info_frame, text="Select a scan mode:").grid(
            row=9, column=0, padx=10, pady=(10, 5), sticky="w"
        )

        self.scan_mode_radio_one = ctk.CTkRadioButton(
            statement_info_frame,
            text="Scan Mode 1: Best results when records table is the largest on the page and/or moderately to well defined.",
            variable=self.app_inputs.scan_mode,
            value=0,
            state="disabled"
        )
        self.scan_mode_radio_one.grid(row=10, column=0, padx=10, pady=5, sticky="w")

        self.scan_mode_radio_two = ctk.CTkRadioButton(
            statement_info_frame,
            text="Scan Mode 2: Best results when records table is loosely defined.",
            variable=self.app_inputs.scan_mode,
            value=1,
            state="disabled"
        )
        self.scan_mode_radio_two.grid(row=11, column=0, padx=10, pady=5, sticky="w")

        # Statement File Path Entry
        ctk.CTkLabel(statement_info_frame, text="Enter the statement PDF path:").grid(
            row=12, column=0, padx=10, pady=(10, 5), sticky="w"
        )

        statement_path_frame = ctk.CTkFrame(statement_info_frame)
        statement_path_frame.grid(row=13, column=0, padx=10, pady=5, sticky="ew")
        statement_path_frame.grid_columnconfigure(0, weight=1)

        self.statement_path_entry = ctk.CTkEntry(
            statement_path_frame, textvariable=self.app_inputs.pdf_path
        ).grid(row=0, column=0, sticky="ew")
        ctk.CTkScrollbar(
            statement_path_frame, orientation="horizontal"
        ).grid(row=1, column=0, sticky="ew")


    def create_output_info_section(self):
        output_info_frame = ctk.CTkFrame(self.scrollable_frame)
        output_info_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        output_info_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(output_info_frame, text="Output File Info").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )

        # Output File Settings Selection
        ctk.CTkLabel(output_info_frame, text="Choose an output path resolution method:").grid(
            row=1, column=0, padx=10, pady=(10, 5), sticky="w")
        self.out_path_settings_combobox = ctk.CTkComboBox(
            output_info_frame,
            width=200,
            values=["DEFAULT", "CUSTOM"],
            variable=self.app_inputs.out_path_settings,
            state="readonly",
            command=lambda x: self.toggle_field_states("OUTPUT_SETTINGS")
        )
        self.out_path_settings_combobox.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Statement Month Selection
        ctk.CTkLabel(output_info_frame, text="Select the month of your statement:").grid(
            row=3, column=0, padx=10, pady=(10, 5), sticky="w")
        self.statement_month_combobox = ctk.CTkComboBox(
            output_info_frame,
            width=200,
            values=self.statement_months,
            variable=self.app_inputs.statement_month,
            state="readonly"
        )
        self.statement_month_combobox.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Statement Year Entry
        ctk.CTkLabel(output_info_frame, text="Enter the statement year:").grid(
            row=5, column=0, padx=10, pady=(10, 5), sticky="w")
        self.statement_year_entry = ctk.CTkEntry(output_info_frame, textvariable=self.app_inputs.statement_year)
        self.statement_year_entry.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

        # Account Type Selection
        ctk.CTkLabel(output_info_frame, text="Indicate the type of account:").grid(
            row=11, column=0, padx=10, pady=(10, 5), sticky="w")
        self.account_type_combobox = ctk.CTkComboBox(
            output_info_frame,
            width=200,
            values=self.account_types,
            variable=self.app_inputs.account_type,
            state="readonly"
        )
        self.account_type_combobox.grid(row=12, column=0, padx=10, pady=5, sticky="w")

        # Output File Type Selection
        ctk.CTkLabel(output_info_frame, text="Select a file type for the output:").grid(
            row=13, column=0, padx=10, pady=(10, 5), sticky="w")
        self.out_file_type_combobox = ctk.CTkComboBox(
            output_info_frame,
            width=200,
            values=self.output_types,
            variable=self.app_inputs.output_type,
            state="readonly"
        )
        self.out_file_type_combobox.grid(row=14, column=0, padx=10, pady=5, sticky="w")

        # Output Path Entry
        ctk.CTkLabel(
            output_info_frame,
            text="Enter the full output file path including the file name and extension:"
        ).grid(row=15, column=0, padx=10, pady=(10, 5), sticky="w")

        output_filepath_frame = ctk.CTkFrame(output_info_frame)
        output_filepath_frame.grid(row=16, column=0, padx=10, pady=5, sticky="ew")
        output_filepath_frame.grid_columnconfigure(0, weight=1)

        self.out_path_entry = ctk.CTkEntry(
            output_filepath_frame, textvariable=self.app_inputs.output_filepath, state="disabled"
        )
        self.out_path_entry.grid(row=0, column=0, sticky="ew")
        ctk.CTkScrollbar(
            output_filepath_frame, orientation="horizontal"
        ).grid(row=1, column=0, sticky="ew")


    def create_buttons(self):
        button_frame = ctk.CTkFrame(self.scrollable_frame)
        button_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            button_frame,
            text="Parse Statement",
            command=lambda: begin_parse(self.app_inputs)
        ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkButton(
            button_frame,
            text="Clear Inputs",
            command=lambda: clear_inputs(self.app_inputs)
        ).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
