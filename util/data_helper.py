from input import Institutions
import re
import pandas

# TODO: create object that can be used to clean and format
# data according to how many columns the data should have
# based on the statement that's being processed as well as whether
# the first element of the lists contains a month abbreviation as
# a proxy for whether this is an actual row of data

class DataHelper:
    def __init__(self, input_data, raw_data):
        self.institution_enum = input_data.institution_enum
        self.account_enum = input_data.account_enum
        self.raw_data = raw_data
        self.column_count = -1
        self.details_col_index = 3
        self.headers = ["Date", "Type", "Account", "Purpose", "Amount ($)", "Details"]
        self.year = re.search(r"(\d+)(?=\.[^\.]*$)", input_data.statement_title).group(1)
        self.months = {
            "JAN": "01",
            "FEB": "02",
            "MAR": "03",
            "APR": "04",
            "MAY": "05",
            "JUN": "06",
            "JUL": "07",
            "AUG": "08",
            "SEP": "09",
            "OCT": "10",
            "NOV": "11",
            "DEC": "12"
        }
        self.account_type = {
            1: "Credit",
            2: "Chequing",
            3: "Savings"
        }

    def get_formatting_config(self):
        if self.institution_enum == Institutions.TD:
            self.column_count = 4

        elif self.institution_enum == Institutions.SIMPLII:
            self.column_count = 7
        else:
            print(
                f"Error: There's some serious funny business afoot. "
                "No config exists for {self.institution_enum.value}. "
                "Please select a supported institution."
            )

    def format_td_amount(self, row):
        # TODO: flip the signs for TD VISA
        amount = re.sub(r"[$,]", "", row[3])
        return amount
    
    def format_simplii_amount(self, row):
        if row[3] not in [None, ""] and row[5] in [None, ""]:
            amount = f"-{row[3].replace(",", "")}"
        elif row[3] in [None, ""] and row[5] not in [None, ""]:
            amount = row[5].replace(",", "")
        else:
            amount = "0"

        return amount
    
    def format_table(self, data):
        table = []
        for row in data:
            month = row[0][:3].upper()
            day = f"0{row[0][3:].strip()}" if len(row[0][3:].strip()) == 1 else f"{row[0][3:].strip()}"

            date = f"{self.year}-{self.months.get(month)}-{day}"
            type = self.account_type.get(self.account_enum.value[0]) if self.account_enum.value[0] in self.account_type else "Cash"
            account = self.account_enum.value[2]
            amount = self.format_td_amount(row) if self.institution_enum == Institutions.TD else self.format_simplii_amount(row)
            details = row[2] if self.institution_enum == Institutions.TD else row[2]

            record = [date, type, account, "", amount, details]
            table.append(record)

        return table
    
    def prepare_records(self):
        self.get_formatting_config()

        # Clean the data
        data = [
            row
            for row in self.raw_data
            if not any(isinstance(i, list) for i in row)
            and len(row) == self.column_count
            and row[0][:3].upper() in self.months
        ]

        table = self.format_table(data)

        records = pandas.DataFrame(table, columns=self.headers)

        return records

