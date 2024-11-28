import re
from pathlib import Path

class ExcelHelper:
    def __init__(self, input_data, records):
        self.institution = input_data.institution_enum.value.replace(" ", "_")
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
        self.records = records

    
    def export_to_excel(self):
        month_num = self.records["Date"].iloc[-1].month
        month_name = next((k for k, v in self.months.items() if int(v) == month_num), None)

        excel_file_path = Path.home() / "Downloads" / f"Cashflows-{self.institution}-{month_name}_{self.year}.xlsx"
        
        self.records.to_excel(excel_file_path, index=False)
        
        return str(excel_file_path)