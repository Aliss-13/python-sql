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


def initialize_player_money(cursor, connection):

    cursor.execute("""
    INSERT OR IGNORE INTO player (id)
    VALUES (1)
    """)

    connection.commit()


def initialize_containers(cursor, connection):

    initial_containers = [
    # Seuil 0
    ("Fiole en verre", 8),
    ("Fiole piriforme", 12),
    ("Flasque souple", 10),
    ("Cuir tanné", 7),
    ("Serviette de table", 5),

    # Seuil 15
    ("Thermos de chantier", 32),
    ("Mini baril plombé", 25),
    ("Carré de soie", 30),
    ("Affiche électorale", 18),

    # Seuil 20
    ("Flacon en cristal ciselé", 48),
    ("Bocal à anchois", 28),
    ("Papyrus", 26),
    ("Notice de montage IKEA", 38),

    # Seuil 25
    ("Flasque Metal Gear Solid", 44),
    ("Parchemin maudit", 35),
    ("Feuille de Bananarama", 34),

    # Seuil 30
    ("Tonnelet en bois-sorcier", 60),

    # Seuil 35
    ("Poche à perfusion", 55),

    # Seuil 40
    ("Tireuse à bière", 85),
    ("Flacon Oeil-de-Dragon", 72),
    ("Cloison de logement social", 68),
    ("Contrat d'assurance", 80),
    ("Plan dimensionnel", 75),
]

    for name, price in initial_containers:
        cursor.execute("""
            INSERT OR IGNORE INTO containers (
                equipment_id,
                price
            )
            SELECT id, ?
            FROM equipment
            WHERE name = ?
        """, (price, name))

    connection.commit()