from player_game.blending import pick_ingredients_to_blend
from display.display_utils import COLORS, RESET

from unittest.mock import MagicMock, patch

def test_pick_ingredients_empty_inventory(capsys):

    cursor = MagicMock()

    inventory = []

    with (
        patch("player_game.blending.display_inventory") as mock_inventory,
        patch("builtins.input") as mock_input
    ):
        mock_inventory.return_value = inventory

        result = pick_ingredients_to_blend(cursor, capacity=2)
        
        assert result is None

        mock_input.assert_not_called()
        captured = capsys.readouterr()
        assert "Votre inventaire est vide." in captured.out


def test_pick_ingredients_first_input_cancel():

    cursor = MagicMock()

    inventory = [
        (1, "Mandragore", 3, 1, "Une racine étrange", "green", "🔥", 0.7),
        (1, "Mandragore", 3, 1, "Une racine étrange", "green", "🌱", 0.3),
        (2, "Champignon", 2, 1, "Un champignon suspect", "blue", "💧", 1.0)
    ]

    with (
        patch("player_game.blending.display_inventory") as mock_inventory,
        patch("builtins.input") as mock_input
    ):
        mock_inventory.return_value = inventory
        mock_input.return_value = ""

        result = pick_ingredients_to_blend(cursor, capacity=2)
        
        assert result is None
        mock_input.assert_called_once()
        cursor.fetchone.assert_not_called()


def test_pick_ingredients(capsys):

    cursor = MagicMock()
    
    inventory = [
        (1, "Mandragore", 3, 1, "Une racine étrange", "green", "🔥", 0.7),
        (1, "Mandragore", 3, 1, "Une racine étrange", "green", "🌱", 0.3),
        (2, "Champignon", 2, 1, "Un champignon suspect", "blue", "💧", 1.0)
    ]

    with (
        patch("player_game.blending.display_inventory") as mock_inventory,
        patch("builtins.input") as mock_input
    ):

        mock_inventory.return_value = inventory
        mock_input.side_effect = ["1", "2"]
        cursor.fetchone.side_effect = [("Mandragore", "green"), ("Champignon", "blue")]
        
        result = pick_ingredients_to_blend(cursor, capacity=2)

        assert result == [1, 2]

        assert mock_input.call_count == 2
        captured = capsys.readouterr()
        assert f"{COLORS["green"]}Mandragore{RESET}" in captured.out
        assert f"{COLORS["blue"]}Champignon{RESET}" in captured.out


def test_pick_not_enough_quantity_ingredients(capsys):

    cursor = MagicMock()
    
    inventory = [
        (1, "Mandragore", 1, 1, "Une racine étrange", "green", "🔥", 0.7),
        (1, "Mandragore", 1, 1, "Une racine étrange", "green", "🌱", 0.3),
        (2, "Champignon", 2, 1, "Un champignon suspect", "blue", "💧", 1.0)
    ]

    with (
        patch("player_game.blending.display_inventory") as mock_inventory,
        patch("builtins.input") as mock_input
    ):

        mock_inventory.return_value = inventory
        mock_input.side_effect = ["1", "1", "2"]
        cursor.fetchone.side_effect = [("Mandragore", "green"), ("Champignon", "blue")]
        
        result = pick_ingredients_to_blend(cursor, capacity=2)
        assert cursor.fetchone.call_count == 2

        assert result == [1, 2]

        assert mock_input.call_count == 3
        captured = capsys.readouterr()
        assert f"{COLORS["green"]}Mandragore{RESET}" in captured.out
        assert "Vous n'avez plus assez de cet ingrédient !" in captured.out
        assert f"{COLORS["blue"]}Champignon{RESET}" in captured.out


def test_pick_not_available_ingredient(capsys):

    cursor = MagicMock()
    
    inventory = [
        (1, "Mandragore", 1, 1, "Une racine étrange", "green", "🔥", 0.7),
        (1, "Mandragore", 1, 1, "Une racine étrange", "green", "🌱", 0.3),
        (2, "Champignon", 2, 1, "Un champignon suspect", "blue", "💧", 1.0)
    ]

    with (
        patch("player_game.blending.display_inventory") as mock_inventory,
        patch("builtins.input") as mock_input
    ):

        mock_inventory.return_value = inventory
        mock_input.side_effect = ["9", "1", "2"]
        cursor.fetchone.side_effect = [("Mandragore", "green"), ("Champignon", "blue")]
        

        result = pick_ingredients_to_blend(cursor, capacity=2)

        assert cursor.fetchone.call_count == 2

        assert result == [1, 2]

        assert mock_input.call_count == 3
        captured = capsys.readouterr()
        assert "Choix invalide. Recommencer ou Entrée pour revenir." in captured.out
        assert f"{COLORS["green"]}Mandragore{RESET}" in captured.out
        assert f"{COLORS["blue"]}Champignon{RESET}" in captured.out