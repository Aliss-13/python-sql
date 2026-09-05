import sqlite3


def menu(cursor, connection):

    while True:

        print()
        print("========== ALCHEMY LABOMATIK ==========")
        print("[1] Ajouter affinité")
        print("[2] Voir affinités")
        print("[q] Quitter")

        choix = input("> ")

        if choix == "1":
            add_affinity(cursor, connection)

        elif choix == "2":
            display_all_affinities(cursor)

        elif choix == "q":
            return

        else:
            print("Choix invalide")

# -----------------------------------------------------------------------------------------------

def add_affinity(cursor, connection):

    name = input("Nom : ")

    try:
        cursor.execute("""
            INSERT INTO affinities (name)
            VALUES (?)
        """, (name,))
        connection.commit()
        print("Affinité ajoutée !")

    except sqlite3.IntegrityError:
        print("Cette affinité existe déjà.")

    connection.commit()


def display_all_affinities(cursor):

    cursor.execute("""
    SELECT
        id,
        name
    FROM affinities
    """)

    result = cursor.fetchall()
    display_affinity(result)


def display_affinity(affinities):
    for aff_id, name in affinities:
        print(f'{aff_id} - {name}')