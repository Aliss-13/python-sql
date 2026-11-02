from unittest.mock import MagicMock
import pytest
from player_game.blending import blend_affinities_result

@pytest.mark.parametrize(
    "ingredients_affinities, blending_affinities, capacity", # liste, dictionnaire, entier (2, 3, 4, 5 ou 6)
    [
        (
            # Scénario 1 : 2 ingrédients, 3 affinités différentes
            [[(1, 0.8, "🔥"), (2, 0.2, "🌱")], [(3, 0.6, "💧"), (2, 0.4, "🌱")]], 
            {1: (0.4, "🔥"), 2: (0.3, "🌱"), 3: (0.3, "💧")},
            2
        ),

        (   # Scénario 2 : 2 ingrédients, 2 affinités communes aux 2 ingrédients
            [[(1, 0.8, "🔥"), (2, 0.2, "🌱")], [(1, 0.6, "🔥"), (2, 0.4, "🌱")]], 
            {1: (0.7, "🔥"), 2: (0.3, "🌱")},
            2
        ),

        (   # Scénario 3 : 2 ingrédients, 1 affinité
            [[(1, 1, "🔥")], [(3, 1, "💧")]], 
            {1: (0.5, "🔥"), 3: (0.5, "💧")},
            2
        ),

        (   # Scénario 4 : 3 ingrédients, 3 affinités
            [[(1, 0.7, "🔥"), (2, 0.3, "🌱")], [(1, 0.5, "🔥"), (2, 0.5, "🌱")], [(1, 0.4, "🔥"), (3, 0.6, "💧")]], 
            {1: (0.53, "🔥"), 2: (0.27, "🌱"), 3: (0.20, "💧")},
            3
        ),

        (   # Scénario 5 : 6 ingrédients, 6 affinités
            [
                [(1, 0.7, "🔥"), (2, 0.3, "🌱")], 
                [(4, 0.5, "🟣"), (2, 0.5, "🌱")], 
                [(5, 0.4, "⚪"), (3, 0.6, "💧")], 
                [(6, 0.4, "🌪️"), (3, 0.6, "💧")], 
                [(4, 0.2, "🟣"), (1, 0.8, "🔥")], 
                [(5, 0.1, "⚪"), (6, 0.9, "🌪️")]
            ], 

            {1: (0.25, "🔥"), 2: (0.13, "🌱"), 3: (0.20, "💧"), 4: (0.12, "🟣"), 5: (0.08, "⚪"), 6: (0.22, "🌪️")},
            6
        )
    ]
)


def test_blend_affinities_result(ingredients_affinities, blending_affinities, capacity):

    cursor = MagicMock()

    #🧠 Pourquoi créer le mock à l'intérieur ?
    # Parce qu'on veut que chaque exécution du test dispose de son propre faux curseur, avec ses propres données et son propre historique d'appels.
    # Si plusieurs tests partageaient le même mock, ils risqueraient de se perturber mutuellement.

    # Petite précision de syntaxe :
    #- MagicMock : la classe.
    #- MagicMock() : on crée une instance de cette classe.
    #- cursor = MagicMock() : on stocke cette instance dans la variable cursor.
    
    ingredients = list(range(1, capacity + 1))

    cursor.fetchall.side_effect = ingredients_affinities
    
    # « Chaque fois que quelqu'un appelle cursor.fetchall(), renvoie cette liste. »
    # Chaque appel successif à fetchall() renvoie la liste suivante.
    # Pourquoi side_effect plutôt que return_value ?
    # Parce que notre fonction interroge SQLite une fois par ingrédient. Nous voulons donc simuler deux réponses différentes, dans l'ordre.

    result = blend_affinities_result(cursor, capacity, ingredients)

    assert result == blending_affinities

    # Méthode classique d'écriture des tests : Arrange, Act, Assert (AAA).
    
    # Arrange	Préparer les données	ingredients, MagicMock, side_effect
    # Act	Exécuter la fonction	result = blend_affinities_result(...)
    # Assert	Vérifier le résultat	assert result == {...}