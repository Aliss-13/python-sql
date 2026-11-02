import pytest
from player_game.blending import compare_clues_to_blend

@pytest.mark.parametrize(
    "recipe_id, difficulty_number_of_affinities, signature, blend_affinity_signature, attendu",

    [
        (5, 3, [("🔥", 0.5), ("🌱", 0.3), ("💧", 0.2)], [("🔥", 0.6), ("💧", 0.3), ("🌱", 0.1)], [(5, 1)]),
        (6, 2, [("🔥", 0.5), ("🌱", 0.3), ("💧", 0.15), ("⚪", 0.05)], [("🔥", 0.6), ("🌱", 0.25), ("💧", 0.1), ("⚪", 0.05)], [(6, 1), (6, 2)]),
        (7, 3, [("🔥", 0.5), ("🌱", 0.3), ("💧", 0.2)], [("💧", 0.5), ("🔥", 0.3), ("🌱", 0.2)], []),
        (8, 4, [("🔥", 0.5), ("🌱", 0.3), ("💧", 0.15), ("⚪", 0.05)], [("🔥", 0.7), ("🌱", 0.3)], [(8, 1), (8, 2)])
    ]

)

def test_compare_clues_to_blend_partial_match(recipe_id, difficulty_number_of_affinities, signature, blend_affinity_signature, attendu):
    
    result = compare_clues_to_blend(recipe_id, difficulty_number_of_affinities, signature, blend_affinity_signature)
   
    assert result == attendu
        