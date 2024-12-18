from .input import AppInputs
import os
import json
from .constants import OUTPUT_TYPES
from jsonschema import validate, ValidationError, SchemaError
from .util.pdf_helper import PDFHelper
from .util.data_helper import DataHelper
from .util.output_helper import ExcelHelper

def load_inputs(app_inputs: AppInputs) -> dict:
    script_dir = os.path.dirname(__file__)
    input_data = {}

    input_data["target"] = app_inputs.target.get()
    input_data["pdf-path"] = app_inputs.pdf_path.get().strip()
    input_data["statement-month"] = app_inputs.statement_month.get()
    input_data["statement-year"] = app_inputs.statement_year.get().strip().replace(" ", "_")
    input_data["account-type"] = app_inputs.account_type.get()
    input_data["output-type"] = OUTPUT_TYPES[app_inputs.output_type.get()]
    input_data["output-filepath"] = app_inputs.output_filepath.get().strip()

    input_data["statement-title"] = input_data["pdf-path"].rsplit("/", 1)[-1]

    if input_data["target"] == "CUSTOM":
        input_data["institution"] = app_inputs.institution.get().strip().replace(" ", "_")
        input_data["table-settings"] = json.loads(app_inputs.table_settings.get("1.0", "end").strip())
        input_data["scan-mode"] = False if app_inputs.scan_mode.get() == 0 else True
        input_data["column-count"] = app_inputs.column_count.get()

        input_data["method"] = ""
    else:
        file_path = os.path.join(script_dir, "configs.json")
        with open(file_path, "r") as json_file:
            configs = json.load(json_file)
        config = configs[input_data["target"]]
        input_data["institution"] = input_data["target"]
        input_data["table-settings"] = config["table-settings"]
        input_data["scan-mode"] = False if config["scan-mode"] == 0 else True
        input_data["column-count"] = config["column-count"]

        input_data["method"] = config["method"]

    # try:
    # validate(instance=input_data, schema=os.path.join(script_dir, "input_schema.json"))   
    # except ValidationError as e:
    #     print("Validation error:", e.message)
    # except SchemaError as e:
    #     print("Schema error:", e.message)

    # TODO: also do a validation on whether the selected output type matches the file extension
    # if a custom output path is provided, and emit a warning if there's a mismatch

    return input_data

def begin_parse(app_inputs: AppInputs):

    if not app_inputs.pdf_path.get():
        print("Error: No PDF path provided.")
        return
    
    input_data = load_inputs(app_inputs)
    
    pdf_helper = PDFHelper(input_data)

    if pdf_helper.is_pdf_scanned():
        print("This application does not support processing for image-based PDF files. \
              Please try again with a text-based PDF file.")
        return
    
    print(f"Beginning table extraction from {input_data["statement-title"]}.")
    raw_data = pdf_helper.read_statement()
    # TODO: implement error handling
    print("Table extraction complete. Cleaning and formatting data...")
    data_helper = DataHelper(input_data, raw_data)
    # This will only generate tables for the cashflows table for now
    records = data_helper.prepare_records()
    print(records)

    print("Data formatted. Exporting to Excel...")
    file_output_path = ExcelHelper(input_data, records).export()
    print(f"Records from {input_data["statement-title"]} have been successfully extracted to {file_output_path}")


def clear_inputs(app_inputs: AppInputs):
    if app_inputs.target.get() == "CUSTOM":
        app_inputs.institution.set("")
        app_inputs.table_settings.set("{\n\t// Enter JSON here\n}")
        app_inputs.scan_mode.set(0)
    app_inputs.target.set("")
    app_inputs.pdf_path.set("")

    if app_inputs.out_path_settings == "DEFAULT":
        app_inputs.statement_month.set("")
        app_inputs.statement_year.set("")
        app_inputs.account_type.set("")
        app_inputs.output_type.set("")
    else:
        app_inputs.output_filepath.set("")
    app_inputs.out_path_settings == "DEFAULT"