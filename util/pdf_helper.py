import pdfplumber
from input import Institutions


class PDFHelper():
    def __init__(self, input_data):
        self.institution_enum = input_data.institution_enum
        self.pdf_path = input_data.statement_path
        self.pdf_title = input_data.statement_title

        self.table_settings = {}

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


    def is_pdf_scanned(self):
        with pdfplumber.open(self.pdf_path) as statement:
            found_text = any(page.extract_text() for page in statement.pages)
            if found_text:
                return False
        return True
    
    # TODO: setup actual config files for each statement type with all related
    # parameters so that processing details can be used across files without
    # repeated code
    def get_extraction_config(self):
        if self.institution_enum == Institutions.TD:
            self.table_settings = {"vertical_strategy": "text"}
        elif self.institution_enum == Institutions.SIMPLII:
            # TODO: try playing with intersection_y_tolerance to see if
            # you can properly capture cells with multiple lines
            self.table_settings = {"horizontal_strategy": "text"}
        else:
            print(
                f"Error: No config exists for {self.institution_enum.value}. "
                "Please select a supported institution."
            )


    def extract_statement_data(self, page):
        if self.institution_enum == Institutions.TD:
            b_box = (0, 0, 347, 616)
            table = page.within_bbox(b_box).extract_table(self.table_settings)
            return table
        elif self.institution_enum == Institutions.SIMPLII:
            table = page.extract_tables(self.table_settings)
            return table
        else:
            print(
                f"Error: Extraction for PDF files from {self.institution_enum.value} \
                are not supported. Please select a supported institution."
            )


    def flatten_to_innermost(self, lst):
        """Recursively drill into lists until reaching a list with no nested lists."""
        if not any(isinstance(i, list) for i in lst):  # No further nested lists
            if lst[0] not in [None, ''] and lst[0][:3].upper() in self.months:
                return lst
            else:
                return None
        for sublist in lst:
            if isinstance(sublist, list):
                flat_list = self.flatten_to_innermost(sublist)  # Recurse into the first nested list
                if flat_list:
                    return flat_list
        return lst

    
    def read_statement(self):
            self.get_extraction_config()
        # try:
            with pdfplumber.open(self.pdf_path) as statement:
                with open("output/extracted_tables.txt", "w", encoding="utf-8") as output_file:
                    contents = []
                    data = []

                    for page in statement.pages:
                        contents.append(self.extract_statement_data(page))

                    if contents:
                        for table in contents:
                            if table:
                                for row in table:
                                    # Flatten the row to the innermost list
                                    flat_row = self.flatten_to_innermost(row) if any(isinstance(i, list) for i in row) else row
                                    print(flat_row)

                                    row_string = "\t".join(str(cell) if cell not in [None, ""] else "" for cell in flat_row)
                                    output_file.write(row_string + "\n")
                                    data.append(flat_row)

                        print("Table extraction complete. Check the extracted_table.txt file.")
                    else:
                        print(f"No tables were found in {self.pdf_title}\n")
                        output_file.write(f"No tables were found in {self.pdf_title}\n\n")
            
            return data
        # except Exception as e:
        #     print(f"Error extracting table from PDF: {e}")
