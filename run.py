from input import InstitutionType, AccountType, InputData
from util.pdf_helper import PDFHelper

def begin_parse(app_inputs):
    pdf_path = app_inputs.path_entry.get()

    if not pdf_path:
        print("Error: No PDF path provided.")
        return
    
    selected_institution = app_inputs.institution.get()
    selected_account = app_inputs.account.get()

    input_data = InputData()
    
    input_data.institution_enum = next(institution for institution in InstitutionType if institution.value == selected_institution)
    input_data.account_enum = next(account for account in AccountType if account.value[1] == selected_account)
    input_data.pdf_path = pdf_path
    input_data.pdf_title = pdf_path.rsplit("/", 1)[-1]
    
    pdf_helper = PDFHelper(input_data)

    if pdf_helper.is_pdf_scanned():
        print("This application does not support processing for image-based PDF files. Please try again with a text-based PDF file.")
        return
    
    print(f"Beginning table extraction from {input_data.pdf_title}.")
    table = pdf_helper.search_pdf()

def clear_inputs(app_inputs):
    app_inputs.institution.set("Make selection")
    app_inputs.account.set("Make selection")
    app_inputs.path_entry.set("")