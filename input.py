from enum import Enum

class Institutions(Enum):
    TD = "TD Bank"
    SIMPLII = "Simplii Financial"

class Accounts(Enum):
    TD_VISA = (1, "TD VISA", "TD VISA")
    SIMPLII_CHEQUING = (2, "Simplii Chequing", "Simplii Chequing (Interac)")
    SIMPLII_SAVINGS = (3, "Simplii Savings", "Simplii Savings")

class AppInputs:
    def __init__(self):
        self.institution = None
        self.account = None
        self.pdf_path = None

class InputData:
    def __init__(self):
        self.institution_enum = None
        self.account_enum = None
        self.statement_path = None
        self.statement_title = None
