from enum import StrEnum

class CustomerOrigin(StrEnum):
    WHATSAPP = "whatsapp"
    INSTAGRAM = "instagram"
    IMPORT = "import"
    MANUAL = "manual"
