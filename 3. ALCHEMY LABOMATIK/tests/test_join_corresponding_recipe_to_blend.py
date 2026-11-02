import pytest

from player_game.blending import join_corresponding_recipe_to_blend

from unittest.mock import MagicMock, patch


def test_join_corresponding_recipe_to_blend_cancellation():

    cursor = MagicMock()

    with (
        patch("player_game.blending.blending") as mock_blending,
        patch("player_game.blending.get_blend_affinity_signature") as mock_signature
    ):
        mock_blending.return_value = None

        result = join_corresponding_recipe_to_blend(cursor)
        
        assert result is None
        mock_signature.assert_not_called()


def test_join_corresponding_recipe_to_blend_clues():

    cursor = MagicMock()

    discoveries = {
        5: (
            "Potion de pouvoir exécutif",
            "Potion",
            "red",
            4,
            3,
            4,
            [("🔥", 0.5), ("🌱", 0.25), ("💧", 0.2), ("⚪", 0.05)]
        )
    }

    with (
        patch("player_game.blending.blending") as mock_blending,
        patch("player_game.blending.get_blend_affinity_signature") as mock_signature,
        patch("player_game.blending.get_discovery_affinity_signature") as mock_discoveries,
        patch("player_game.blending.get_unknown_recipes") as mock_unknown_recipes,
        patch("player_game.blending.save_clues_to_player_recipe_research") as mock_clues,
        patch("player_game.blending.compare_recipe_to_blend") as mock_compare,
        patch("player_game.blending.random.random", return_value=0.8)
    ):
        mock_blending.return_value = ({1: (0.5, "🔥"), 2: (0.25, "💧"), 3: (0.2, "🌱"), 4: (0.05, "⚪")}, 4, [15, 22]) # blending_affinities, capacity, blending_ingredients
        mock_signature.return_value = [("🔥", 0.5), ("💧", 0.25), ("🌱", 0.2)] # signature du mélange
        mock_discoveries.return_value = {}
        mock_unknown_recipes.return_value = list(discoveries.items())
        mock_compare.return_value = None
        mock_clues.return_value = [("🔥", 0.5), ("💧", 0.25)]
        
        result = join_corresponding_recipe_to_blend(cursor)
        
        assert result is None

        mock_clues.assert_called_once_with(5, 4, [("🔥", 0.5), ("🌱", 0.25), ("💧", 0.2), ("⚪", 0.05)], [("🔥", 0.5), ("💧", 0.25), ("🌱", 0.2)], cursor)


def test_join_corresponding_recipe_to_blend():

    cursor = MagicMock()

    discoveries = {
        3: (
            "Potion de puissance",
            "Potion",
            "red",
            2,
            2,
            2,
            [("🔥", 0.6), ("🌱", 0.4)]
        )
    }

# La règle à retenir : patch() remplace une fonction là où elle est recherchée, pas nécessairement là où elle a été définie.
# C'est particulièrement important ici : sinon, ton test risque d'appeler les véritables fonctions SQL alors que tu pensais les avoir simulées.

    with (
        patch("player_game.blending.blending") as mock_blending,
        patch("player_game.blending.get_blend_affinity_signature") as mock_signature,
        patch("player_game.blending.get_discovery_affinity_signature") as mock_discoveries,
        patch("player_game.blending.get_unknown_recipes") as mock_unknown_recipes,
        patch("player_game.blending.compare_recipe_to_blend") as mock_compare
    ):
        mock_blending.return_value = ({1: (0.7, "🔥"), 2: (0.3, "🌱")}, 2, [10, 20]) # blending_affinities, capacity, blending_ingredients
        mock_signature.return_value = [("🔥", 0.7), ("🌱", 0.3)] # signature du mélange
        mock_discoveries.return_value = discoveries # découvertes
        mock_unknown_recipes.return_value = [] # indices

        mock_compare.return_value = (3, "Potion de puissance", 2)
        

        result = join_corresponding_recipe_to_blend(cursor)
        
        assert result == (3, "Potion de puissance", 2)
        mock_compare.assert_called_once_with(3, "Potion de puissance", 2, 2, [("🔥", 0.6), ("🌱", 0.4)], [("🔥", 0.7), ("🌱", 0.3)])



@pytest.mark.parametrize(
    "random_value, accident_expected",
    [
        (0.49, True),
        (0.50, False),
        (0.51, False),
    ]
)

def test_join_corresponding_recipe_to_blend_number_of_ingredients_not_capacity(random_value, accident_expected):

    cursor = MagicMock()

    discoveries = {
        3: (
            "Potion de puissance",
            "Potion",
            "red",
            3,
            2,
            2,
            [("🔥", 0.6), ("🌱", 0.4)]
        )
    }

    with (
        patch("player_game.blending.blending") as mock_blending,
        patch("player_game.blending.get_blend_affinity_signature") as mock_signature,
        patch("player_game.blending.get_discovery_affinity_signature") as mock_discoveries,
        patch("player_game.blending.get_unknown_recipes") as mock_unknown_recipes,
        patch("player_game.blending.compare_recipe_to_blend") as mock_compare,
        patch("player_game.blending.trigger_blending_accident") as mock_accident,
        patch("player_game.blending.random.random") as mock_random
    ):
        mock_blending.return_value = ({1: (0.7, "🔥"), 2: (0.3, "🌱")}, 2, [10, 20]) # blending_affinities, capacity, blending_ingredients
        mock_signature.return_value = [("🔥", 0.7), ("🌱", 0.3)] # signature du mélange
        mock_discoveries.return_value = discoveries # découvertes
        mock_unknown_recipes.return_value = [] # indices
        mock_random.return_value = random_value

        result = join_corresponding_recipe_to_blend(cursor)

        assert result is None

        mock_compare.assert_not_called()

        if accident_expected:
            mock_accident.assert_called_once_with(cursor, [10, 20])
        else:
            mock_accident.assert_not_called()