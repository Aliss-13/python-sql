from player_game.blending import get_blend_affinity_signature

def test_get_blend_affinity_signature(capsys):

    blending_affinities = {
        1: (0.3, "🔥"),
        2: (0.8, "🌱"),
        3: (0.5, "💧")
    }

    result = get_blend_affinity_signature(blending_affinities)

    assert result == [("🌱", 0.8), ("💧", 0.5), ("🔥", 0.3)]

    captured = capsys.readouterr()
    assert "Signature du mélange :\n🌱 : 0.8\n💧 : 0.5\n🔥 : 0.3" in captured.out