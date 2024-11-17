import pdfplumber
from input import InstitutionType


class PDFHelper():
    def __init__(self, input_data):
        self.institution_enum = input_data.institution_enum
        self.account_enum = input_data.account_enum

        self.pdf_path = input_data.pdf_path
        self.pdf_title = input_data.pdf_title

        self.table_settings = {}
        self.column_count = -1


    def is_pdf_scanned(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            found_text = any(page.extract_text() for page in pdf.pages)
            if found_text:
                return False
        return True
    

    def get_extraction_config(self):
        if self.institution_enum == InstitutionType.TD:
            self.table_settings = {"vertical_strategy": "text"}
            self.column_count = 7
        elif self.institution_enum == InstitutionType.SIMPLII:
            self.table_settings = {"horizontal_strategy": "text"}
            self.column_count = 4
        else:
            print(f"Error: No config exists for {self.institution_enum.value}. Please select a supported institution.")


    def extract_pdf_table(self, page):
        if self.institution_enum == InstitutionType.TD:
            b_box = (0, 0, 347, 616)
            table = page.within_bbox(b_box).extract_table(self.table_settings)
            return table
        elif self.institution_enum == InstitutionType.SIMPLII:
            table = page.extract_tables(self.table_settings)
            return table
        else:
            print(f"Error: Extraction for PDF files from {self.institution_enum.value} are not supported. Please select a supported institution.")


    def search_pdf(self):
            self.get_extraction_config()
        # try:
            with pdfplumber.open(self.pdf_path) as pdf:
                with open("output/extracted_tables.txt", "w", encoding="utf-8") as output_file:
                    tables = []

                    for page in pdf.pages:
                        tables.append(self.extract_pdf_table(page))

                    if tables:
                        for table in tables:
                            if table:
                                for row in table:
                                    print(row)
                                    row_string = "\t".join(str(cell) if cell not in [None, ""] else "" for cell in row)
                                    output_file.write(row_string + "\n")

                        print("Table extraction complete. Check the extracted_table.txt file.")
                    else:
                        print(f"No tables were found in {self.pdf_title}\n\n")
                        output_file.write(f"No tables were found in {self.pdf_title}\n\n")
            
            return tables
        # except Exception as e:
        #     print(f"Error extracting table from PDF: {e}")
