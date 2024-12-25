import pdfplumber
from src.constants import MONTHS


class PDFHelper():
    def __init__(self, input_data: dict):
        self.input_data = input_data


    def is_pdf_scanned(self):
        with pdfplumber.open(self.input_data['pdf-path']) as statement:
            found_text = any(page.extract_text() for page in statement.pages)
            if found_text:
                return False
        return True


    def extract_statement_data(self, page):
        if self.input_data['scan-mode'] is False:
            table = page.extract_table(self.input_data['table-settings'])
            return table
        elif self.input_data['scan-mode'] is True:
            table = page.extract_tables(self.input_data['table-settings'])
            return table
        else:
            print(
                f"Error: Extraction for PDF files from \
                    {self.input_data['institution'] if self.input_data['institution'] else 'Unknown Institution'} \
                        is not supported. Please select a supported institution."
            )


    def flatten_to_innermost(self, lst):
        if not any(isinstance(i, list) for i in lst):  # No further nested lists
            if lst[0] not in [None, ''] and lst[0][:3].upper() in MONTHS:
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
        # try:
            with pdfplumber.open(self.input_data['pdf-path']) as statement:
                # pg = statement.pages[0]
                # im = pg.to_image()
                # im.draw_vlines([60, 95, 129, 308, 349])
                # im.show()
                contents = []
                data = []

                for page_num, page in enumerate(statement.pages, start=1):
                    contents.append(self.extract_statement_data(page))

                if contents:
                    for table in contents:
                        if table:
                            for row in table:
                                # Flatten the row to the innermost list
                                flat_row = self.flatten_to_innermost(row) if any(isinstance(i, list) for i in row) else row
                                print(flat_row)

                                data.append(flat_row)

                    print("Table extraction complete. Check the extracted_table.txt file.")
                else:
                    print(f"No tables were found in {self.input_data['statement-title']}\n")
            
            return data
        # except Exception as e:
        #     print(f"Error extracting table from PDF: {e}")
