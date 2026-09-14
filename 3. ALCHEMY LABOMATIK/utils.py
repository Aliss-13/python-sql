def id_exists(cursor, table, object_id):
    cursor.execute(f"""
        SELECT id
        FROM {table}
        WHERE id = ?
    """, (object_id,))

    return cursor.fetchone() is not None


def ask_int(prompt):

    while True:

        try:
            value = int(input(prompt))
            return value

        except ValueError:
            print("Saisie invalide.")


def ask_positive_int(prompt):

    while True:

        try:
            value = int(input(prompt))

            if value > 0 :
                return value
            else:
                print("La valeur doit être positive.")

        except ValueError:
            print("Saisie invalide.")


def ask_positive_float_0_1(prompt):

    while True:

        try:
            value = float(input(prompt))

            if 0 < value <= 1 :
                return value
            else:
                print("La valeur doit être positive et comprise entre 0 et 1.")

        except ValueError:
            print("Saisie invalide.")