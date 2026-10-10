def initialize_player_equipment(cursor, connection):

    cursor.execute("""
        SELECT COUNT(*)
        FROM player_recipes
    """)

    discovery_count = cursor.fetchone()[0]

    cursor.execute("""
        INSERT OR IGNORE INTO player_equipment (
            equipment_id,
            crafted
        )
        SELECT id, 0
        FROM equipment
        WHERE unlock_discoveries <= ?
    """, (discovery_count,))

    connection.commit()