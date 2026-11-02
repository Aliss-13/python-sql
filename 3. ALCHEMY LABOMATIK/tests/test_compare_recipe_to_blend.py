import pytest
from player_game.blending import compare_recipe_to_blend

@pytest.mark.parametrize(
    "blend_affinity_signature, attendu",
    [
        ([("🔥", 0.6), ("🌱", 0.4)],
        (3, "Potion de puissance", 2)),

        ([("🔥", 0.7), ("🌱", 0.3)],
        (3, "Potion de puissance", 2)),

        ([("💧", 0.6), ("🌱", 0.4)],
        None),

        ([("🔥", 0.5), ("🌱", 0.5)],
        None),

        ([("🔥", 0.4), ("🌱", 0.6)],
        None),
    ]
)

def test_compare_recipe_to_blend(blend_affinity_signature, attendu):
    result = compare_recipe_to_blend(3, "Potion de puissance", 2, 2, [("🔥", 0.6), ("🌱", 0.4)], blend_affinity_signature)
    assert result == attendu