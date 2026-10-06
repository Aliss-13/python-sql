YELLOW = "\033[93m"
CYAN = "\033[38;2;112;198;250m"
BLUE = "\033[94m"
DIM = "\033[2m"
LIGHT_YELLOW = "\033[38;2;255;250;205m"
LIGHT_PINK = "\033[38;5;218m"
LIGHT_GREEN = "\033[38;5;120m"
PURPLE = "\033[95m"
ORANGE = "\033[38;5;208m"
RED = "\033[38;5;196m"
RESET = "\033[0m"


COLORS = {
    "white": "\033[37m",
    "green": "\033[32m",
    "blue": "\033[34m",
    "purple": "\033[35m",
    "reset": "\033[0m",
}


def dans_ton_q():
    print()
    print("À chaque étape : q pour quitter.")


def display_main_menu():
    print()
    print("   ┌──────────────────────┐   ")
    print("   | Alchemy Lab-o-Matik  |   ")
    print("   └──────────────────────┘   ")
    print("Votre magie, notre logistique®.")
    print()
    print()
    print(f"Accès menu gestion base de données : {YELLOW}bdd_forever{RESET}")
    print()