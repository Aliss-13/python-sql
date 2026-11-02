import pytest

from unittest.mock import MagicMock, patch

from player_game.blending import discover_recipe

def test_discover_recipe_none():

    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    with patch(
        "player_game.blending.join_corresponding_recipe_to_blend",
        return_value=None
    ):
        discover_recipe(mock_cursor, mock_connection)

    mock_connection.commit.assert_called_once_with()
    mock_connection.rollback.assert_not_called()
    mock_cursor.execute.assert_not_called()

    
def test_discover_recipe_already_discovered():

    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    with patch(
        "player_game.blending.join_corresponding_recipe_to_blend",
        return_value=(5, "Potion de mana", 2)
        
    ):
        mock_cursor.fetchone.return_value = (5,)
        discover_recipe(mock_cursor, mock_connection)
        
    mock_connection.commit.assert_called_once_with()
    mock_connection.rollback.assert_not_called()

    # évite que le test prenne en compte les espaces et la mise en forme de la requête SQL
    sql, params = mock_cursor.execute.call_args.args

    assert " ".join(sql.split()) == (
        "SELECT recipe_id FROM player_recipes WHERE recipe_id = ?"
    )
    assert params == (5,)


def test_discover_recipe_not_already_discovered(capsys):

    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    with (
        patch("player_game.blending.join_corresponding_recipe_to_blend",
            return_value=(5, "Potion de mana", 2)),
        patch("player_game.blending.check_discovery_achievements") as mock_achievements,
        patch("player_game.blending.initialize_player_equipment") as mock_equipment
    ): # Les mocks empêchent l'exécution réelle des fonctions annexes.
        
        mock_cursor.fetchone.side_effect = [None, ("Potion de mana", "blue")]

        discover_recipe(mock_cursor, mock_connection)

        mock_achievements.assert_called_once_with(mock_cursor) # check_discovery_achievements
        mock_equipment.assert_called_once_with(mock_cursor) # initialize_player_equipment

        assert mock_cursor.execute.call_count == 3 # combien de fois est appelé cursor.execute
        mock_connection.commit.assert_called_once() # combien de commit
        mock_connection.rollback.assert_not_called() # combien de rollback


        sql, params = mock_cursor.execute.call_args.args # vérification dernière requête sql

        assert " ".join(sql.split()) == (
            "INSERT INTO player_recipes (recipe_id) VALUES (?)"
        )
        assert params == (5,)

        captured = capsys.readouterr() # affichage du print
        assert "Vous découvrez" in captured.out
        assert "Potion de mana" in captured.out


def test_discover_recipe_runtime_error():

    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    with (
        patch("player_game.blending.join_corresponding_recipe_to_blend", 
              return_value=(5, "Potion de mana", 2))
    ):
        mock_cursor.fetchone.side_effect = [None, None]

        with pytest.raises(RuntimeError):
            discover_recipe(mock_cursor, mock_connection)

# Lorsque Python sort du premier bloc with, le patch() est désactivé. Donc, au moment où tu appelles discover_recipe(), 
# la véritable fonction join_corresponding_recipe_to_blend() est de nouveau utilisée.
# 🧪 La correction : il faut que les deux contextes soient actifs pendant l'appel

    assert mock_cursor.execute.call_count == 2 # combien de fois est appelé cursor.execute
    mock_connection.commit.assert_not_called() # combien de commit
    mock_connection.rollback.assert_called_once() # combien de rollback


    