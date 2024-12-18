from ..constants import MONTHS
from datetime import datetime
import re
import pandas

class DataHelper:
    def __init__(self, input_data: dict, raw_data: list):
        self.input_data = input_data
        self.raw_data = raw_data
        self.headers = ["Date", "Type", "Account", "Purpose", "Amount ($)", "Details"]

    def format_td_amount(self, row):
        amount = re.sub(r"[$,]", "", row[3])
        amount = float(f"-{amount.split('\n')[0]}") if amount[0] != "-" else float(amount[1:].split('\n')[0])
        return amount
    
    def format_simplii_amount(self, row):
        if row[3] not in [None, ""] and row[5] in [None, ""]:
            amount = float(f"-{row[3].replace(",", "")}")
        elif row[3] in [None, ""] and row[5] not in [None, ""]:
            amount = float(row[5].replace(",", ""))
        else:
            amount = 0

        return amount
    
    def format_table(self, data):
        table = []
        for row in data:
            month = row[0][:3].upper()
            day = f"0{row[0][3:].strip()}" if len(row[0][3:].strip()) == 1 else f"{row[0][3:].strip().split('\n')[0]}"

            date = datetime(int(self.input_data["statement-year"]), int(MONTHS.get(month)), int(day)).date()
            type = self.input_data["account-type"]
            account = self.input_data["method"]
            amount = self.format_td_amount(row) if self.input_data["column-count"] == 4 else self.format_simplii_amount(row)
            details = row[2].replace("\n", " ")

            record = [date, type, account, "", amount, details]
            table.append(record)

        return table
    
    def prepare_records(self):
         # Clean the data
        data = [
            row
            for row in self.raw_data
            if not any(isinstance(i, list) for i in row)
            and len(row) == self.input_data["column-count"]
            and row[0][:3].upper() in MONTHS
        ]

        table = self.format_table(data)

        records = pandas.DataFrame(table, columns=self.headers)

        return records

