from enum import Enum

class InstitutionType(Enum):
    TD = "TD Bank"
    SIMPLII = "Simplii Financial"

class AccountType(Enum):
    TD_VISA = (1, "TD VISA")
    SIMPLII_CHEQUING = (2, "Simplii Chequing")
    SIMPLII_SAVINGS = (3, "Simplii Savings")

class AppInputs:
    def __init__(self):
        self.institution = None
        self.account = None
        self.path_entry = None

class InputData:
    def __init__(self):
        self.institution_enum = None
        self.account_enum = None
        self.pdf_path = None
        self.pdf_title = None
