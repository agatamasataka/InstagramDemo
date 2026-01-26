import customtkinter as ctk

# Locaop Brand Colors
# Primary Cyan (Logo/Accents): #33B9BB (Original Analysis: #33B9BB)
# CTA Orange (Action Buttons): Gradient from #FFAA00 to #FF6000
# Secondary/Text: #333333 (Dark Gray)
# Background: #FFFFFF (White) or #F5F7FA (Light Gray)
# Sidebar/Nav: #FFFFFF or very light branding

class BrandColors:
    PRIMARY = "#33B9BB"      # Cyan
    SECONDARY = "#F0F0F0"    # Light Gray
    TEXT_MAIN = "#333333"    # Dark Gray
    TEXT_WHITE = "#FFFFFF"
    CTA_ORANGE = "#FF9500"   # Approximate Orange for simplicity (CustomTkinter doesn't do complex gradients natively on buttons easily)
    CTA_HOVER = "#E08300"
    SUCCESS_GREEN = "#2B4A3B" # Keeping dark mode compatibility logic or shifting to Locaop style?
    # Locaop is light/clean. Let's switch to Light Mode default or support both.
    
    # Light Mode Palette
    BG_LIGHT_MAIN = "#F5F7FA" # Very light grey-blueish
    BG_WHITE = "#FFFFFF"
    BORDER_LIGHT = "#E1E4E8"

# Theme Manager
def apply_theme():
    ctk.set_appearance_mode("Light") # Locaop uses a clean white interface
    ctk.set_default_color_theme("green") # Closest built-in to Cyan or we set manual colors

# Component Styles
BUTTON_CONFIG = {
    "corner_radius": 20, # Pill shape
    "font": ("M PLUS Rounded 1c", 14, "bold"),
    "fg_color": BrandColors.CTA_ORANGE,
    "hover_color": BrandColors.CTA_HOVER,
    "text_color": BrandColors.TEXT_WHITE
}

HEADER_LABEL_CONFIG = {
    "font": ("M PLUS Rounded 1c", 24, "bold"),
    "text_color": BrandColors.PRIMARY
}

SUBHEADER_CONFIG = {
    "font": ("M PLUS Rounded 1c", 16, "bold"),
    "text_color": BrandColors.TEXT_MAIN
}
