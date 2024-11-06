import tkinter as tk
import customtkinter as ctk

# Initialize customtkinter theme
ctk.set_appearance_mode("System")  # Light or Dark
ctk.set_default_color_theme("blue")  # Blue color theme

class StatementParserApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        institutions = ["TD Bank", "Simplii Financial"]
        accounts = ["TD VISA", "Simplii Chequing", "Simplii Savings"]

        self.title("Statement Parser")
        self.geometry("720x540")

        # Institution dropdown
        self.institution_input_label = ctk.CTkLabel(self, text="Select an institution:")
        self.institution_input_label.pack(padx=100, pady=(50, 5), anchor="w")

        self.institution = ctk.StringVar(value="Make selection")
        self.institution_dropdown = ctk.CTkComboBox(self, width=150, values=institutions, variable=self.institution)
        self.institution_dropdown.pack(padx=100, pady=(5, 20), anchor="w")

        # Accounts dropdown
        self.accounts_input_label = ctk.CTkLabel(self, text="Select an account:")
        self.accounts_input_label.pack(padx=100, pady=(20, 5), anchor="w")

        self.account = ctk.StringVar(value="Make selection")
        self.accounts_dropdown = ctk.CTkComboBox(self, width=150, values=accounts, variable=self.account)
        self.accounts_dropdown.pack(padx=100, pady=(5, 20), anchor="w")

        # Statement text
        self.string_input_label = ctk.CTkLabel(self, text="Paste the statement text to be parsed:")
        self.string_input_label.pack(padx=100, pady=(20, 5), anchor="w")

        self.text_entry = ctk.CTkTextbox(self, width=500, height=150)
        self.text_entry.pack(padx=100, pady=5, anchor="w")

        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=30)

        self.parse_button = ctk.CTkButton(button_frame, text="Parse", command=self.begin_parse)
        self.clear_button = ctk.CTkButton(button_frame, text="Clear", command=self.clear_inputs)

        self.parse_button.grid(row=0, column=0, padx=(0, 70), sticky="w")
        self.clear_button.grid(row=0, column=1, padx=(70, 0), sticky="w")

    def begin_parse(self):
        input_text = self.text_entry.get("1.0", tk.END)
        print(f"Parsed")

    def clear_inputs(self):
        self.institution.set("Make selection")
        self.account.set("Make selection")
        self.text_entry.delete("1.0", tk.END)

    def parse_td_bank_statement(input_text):
        # Initialize an empty 2D array to store transactions
        transactions = []

        # Split the input text by new lines to get each transaction line
        lines = input_text.strip().split("\n")

        # Process each line
        for line in lines:
            # Split line by spaces to separate the components
            parts = line.split()

            # Ensure the line has enough parts to parse a transaction
            if len(parts) >= 5:
                # The first two items are the transaction date (month and day)
                transaction_date = f"{parts[0]} {parts[1]}"
                # The next two items are the posted date (month and day)
                posted_date = f"{parts[2]} {parts[3]}"
                # The description is everything up to the last element (the amount)
                description = " ".join(parts[4:-1])
                # The amount is the last element
                amount = parts[-1]

                # Append the transaction data as a list to the 2D array
                transactions.append([transaction_date, posted_date, description, amount])

        print(transactions)
        # return transactions

    def parse_simplii_statement(input_text):
        # Initialize an empty 2D array to store transactions
        transactions = []

        # Split the input text by new lines to get each line of the statement
        lines = input_text.strip().split("\n")

        # Process each transaction in chunks of 5 lines
        for i in range(0, len(lines), 5):
            # Ensure there are enough lines left for a complete transaction
            if i + 4 < len(lines):
                transaction_date = lines[i].strip()
                posted_date = lines[i + 1].strip()
                description = lines[i + 2].strip()
                balance = lines[i + 3].strip()
                amount = lines[i + 4].strip()

                # Append the transaction data as a list to the 2D array
                transactions.append([transaction_date, posted_date, description, balance, amount])

        return transactions


# Run the app
if __name__ == "__main__":
    app = StatementParserApp()
    app.mainloop()
