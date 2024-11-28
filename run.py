from input import Institutions, Accounts, InputData
from util.pdf_helper import PDFHelper
from util.data_helper import DataHelper

def begin_parse(app_inputs):
    pdf_path = app_inputs.pdf_path.get()

    if not pdf_path:
        print("Error: No PDF path provided.")
        return
    
    selected_institution = app_inputs.institution.get()
    selected_account = app_inputs.account.get()

    input_data = InputData()
    
    input_data.institution_enum = next(institution for institution in Institutions if institution.value == selected_institution)
    input_data.account_enum = next(account for account in Accounts if account.value[1] == selected_account)
    input_data.statement_path = pdf_path
    input_data.statement_title = pdf_path.rsplit("/", 1)[-1]
    
    pdf_helper = PDFHelper(input_data)

    if pdf_helper.is_pdf_scanned():
        print("This application does not support processing for image-based PDF files. Please try again with a text-based PDF file.")
        return
    
    print(f"Beginning table extraction from {input_data.statement_title}.")
    raw_data = pdf_helper.read_statement()
    # TODO: implement error handling
    print("Tables extraction complete. Cleaning and formatting data...")
    data_helper = DataHelper(input_data, raw_data)
    # This will only generate tables for the cashflows table for now
    records = data_helper.prepare_records()

    print(records)


def clear_inputs(app_inputs):
    app_inputs.institution.set("Make selection")
    app_inputs.account.set("Make selection")
    app_inputs.path_entry.set("")