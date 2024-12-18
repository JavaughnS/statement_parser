from pathlib import Path

class ExcelHelper:
    def __init__(self, input_data, records):
        self.input_data = input_data
        self.records = records

    
    def export(self):
        extension = self.input_data["output-type"]

        default_file_name = "statement-data"
        if self.input_data["institution"] and self.input_data["account-type"] and self.input_data["statement-month"] and self.input_data["statement-year"]:
            default_file_name = f"Cashflows-{self.input_data["institution"]}_{self.input_data["account-type"]}-{self.input_data["statement-month"]}_{self.input_data["statement-year"]}.{extension}"
        
        default_path = Path.home() / "Downloads"

        file_path = self.input_data["output-filepath"] if self.input_data["output-filepath"] else default_path / default_file_name # if output_filepath is not null or empty, do that instead
        
        if extension == "xlsx":
            self.records.to_excel(file_path, index=False)
        else:
            self.records.to_csv(file_path, index=False)
        
        return str(file_path)