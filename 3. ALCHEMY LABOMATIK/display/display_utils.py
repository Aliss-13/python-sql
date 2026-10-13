import textwrap


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
    print(f"Accès menu gestion base de données : {YELLOW}b{RESET}")
    print()


def display_recipe_description(description):
    
    if description is None:
        return

    lines = textwrap.wrap(description, width=100)

    for line in lines:
        print(f'     {DIM}{line}{RESET}')


def format_difficulty_stars(difficulty_id):
    return "★" * difficulty_id + DIM + "☆" * (5 - difficulty_id) + RESET # concaténation => "texte" + variable


def info_format_difficulty_stars():
    print(f"Difficulté découverte {LIGHT_PINK}(rang d'affinité){RESET} : ★ très facile {LIGHT_PINK}(2){RESET} - "
          f'★★ facile {LIGHT_PINK}(3){RESET} - ★★★ moyen {LIGHT_PINK}(4){RESET} - ★★★★ difficile {LIGHT_PINK}(5){RESET} - '
          f'★★★★★ très difficile {LIGHT_PINK}(6){RESET}')
    print()


def flamel_xpress():
    print(f"🌐 {CYAN}FlamelXpress© = N°1 mondial de l'alchimie = {RESET}")
    print("   « Le prix et la qualité en instantané ! »*")
    print(f"{DIM}   *Voir conditions générales de transmutation.{RESET}")
    print()

def youtique():
    print(f"🐍 {LIGHT_GREEN}La Youtique© - Parce qu'il faut bien que je vende mes merdes 🤸 {RESET}")
    print(f"{DIM}   Récupère le flouze, le pèze, la moula, le pognon et à toi les gourgandines et l'opium !{RESET}")
    print()


def display_reset_game():

    print(f"      ⚠️  {YELLOW}RÉINITIALISATION DE LA PARTIE{RESET}")
    print()
    print("Cette action supprimera toute votre progression :")
    print("- ingrédients")
    print("- recettes découvertes")
    print("- équipements fabriqués")
    print("- produits")
    print("- ventes")
    print("- recherches du grimoire")
    print("- etc.")
    print()
    print("Votre argent sera réinitialisé à 100 pièces.")
    print()
    print(f"Pour confirmer, tapez {YELLOW}reset_game{RESET}")
    print()

