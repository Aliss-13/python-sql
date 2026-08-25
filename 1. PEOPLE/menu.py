from display import display_people, display_age, display_color, display_group, display_color_with_ages

def menu(cursor, connection):
    
    while True:
        print()
        print("----------MENU----------")
        print()
        print("[1] Ajouter une personne")
        print("[2] Afficher toutes les personnes")
        print("[3] Rechercher par âge")
        print("[4] Rechercher par ville")
        print("[5] Modifier une personne")
        print("[6] Supprimer une personne")
        print("------------------------")
        print("[7] Ordonner ville -> âge -> nom")
        print("[8] Nombre de personnes par ville")
        print("[9] Age moyen par ville")
        print("[10] Filtrer les villes d'âge moyen > 30")
        print("[11] Filtrer les villes de population d'au moins 3 personnes")
        print("------------------------")
        print("[12] Modifier couleur préférée")
        print("[13] Nombre de personnes par couleur")
        print("[14] Filtrer les couleurs d'au moins 3 personnes majeures")
        print("[15] Statistiques d'âge par couleur")
        print("------------------------")
        print("[16] Quitter")

        choix = input("> ")

        if choix == "1":
            add_person(cursor, connection)

        elif choix == "2":
            display_all_people(cursor)

        elif choix == "3":
            filter_people_by_age(cursor)

        elif choix == "4":
            filter_people_by_city(cursor)

        elif choix == "5":
            display_all_people(cursor)
            update_person(cursor, connection)

        elif choix == "6":
            display_all_people(cursor)
            delete_person(cursor, connection)

        elif choix == "7":
            order_people_by_city(cursor)

        elif choix == "8":
            group_people_by_city(cursor)

        elif choix == "9":
            average_people_age_by_city(cursor)

        elif choix == "10":
            filter_cities_by_age(cursor)

        elif choix == "11":
            filter_cities_by_people_number(cursor)

        elif choix == "12":
            display_all_people(cursor)
            update_people_by_color(cursor, connection)

        elif choix == "13":
            group_people_by_color(cursor)

        elif choix == "14":
            filter_colors_by_people_number(cursor)

        elif choix == "15":
            group_people_by_color_with_ages(cursor)

        elif choix == "16":
            return

        else:
            print("Choix invalide")



def group_people_by_color_with_ages(cursor):

    cursor.execute("""
    SELECT
        colors.name,
        COUNT(*),
        MIN(people.age),
        AVG(people.age),
        MAX(people.age)
    FROM people
    LEFT JOIN colors
    ON people.color_id = colors.id
    GROUP BY people.color_id
    """)

    result = cursor.fetchall()
    display_color_with_ages(result)


def filter_colors_by_people_number(cursor):

    cursor.execute("""SELECT colors.name, COUNT(*)
    FROM people
    LEFT JOIN colors 
    ON people.color_id = colors.id
    WHERE age >= 18
    GROUP BY people.color_id
    HAVING COUNT(*) >= 3
    ORDER BY COUNT(*) DESC
    """)

    adults = cursor.fetchall()
    print(adults)


def group_people_by_color(cursor):

    cursor.execute("""SELECT colors.name, COUNT(*)
    FROM people
    LEFT JOIN colors 
    ON people.color_id = colors.id
    GROUP BY colors.id
    """)

    color_group = cursor.fetchall()
    display_color(color_group)


def update_people_by_color(cursor, connection):

    person_id = int(input("ID de la personne à modifier : "))
    couleur = input("Couleur : ")

    cursor.execute("""
        SELECT id
        FROM colors
        WHERE name = ?
        """, (couleur,))

    result = cursor.fetchone()
    color_id = result[0]

    cursor.execute("""
        UPDATE people
        SET color_id = ?
        WHERE id = ?
        """, (color_id, person_id))

    connection.commit()


# JOINT colors on joint une table !

    cursor.execute("""SELECT 
        people.id,
        people.name,
        people.age,
        people.city,
        colors.name 
        FROM people
        JOIN colors 
        ON people.color_id = colors.id
        """)

    print(cursor.fetchall())

def group_people_by_city(cursor):

    cursor.execute("""
        SELECT city, COUNT(*)
        FROM people
        GROUP BY city
        """)

    people_number = cursor.fetchall()
    display_group(people_number)


def average_people_age_by_city(cursor):

    cursor.execute("""
        SELECT city, AVG(age)
        FROM people
        GROUP BY city
        """)

    people_age = cursor.fetchall()
    display_age(people_age)


def filter_cities_by_age(cursor):

    cursor.execute("""SELECT city, AVG(age)
    FROM people
    GROUP BY city
    HAVING AVG(age) > 30
    """)

    cities_age = cursor.fetchall()
    print(cities_age)


def filter_cities_by_people_number(cursor):

    cursor.execute("""SELECT city, COUNT(*)
    FROM people
    GROUP BY city
    HAVING COUNT(*) >= 3
    ORDER BY COUNT(*) DESC
    """)

    population = cursor.fetchall()
    print(population)


def order_people_by_city(cursor):

    cursor.execute("""
    SELECT 
        people.id,
        people.name,
        people.age,
        people.city,
        colors.name 
    FROM people
    JOIN colors 
    ON people.color_id = colors.id
    ORDER BY people.city, people.age, people.name
    """)

    people = cursor.fetchall()
    display_people(people)


def add_person(cursor, connection):

    name = input("Nom : ")
    age = int(input("Âge : "))
    city = input("Ville : ")

    cursor.execute("""
        INSERT INTO people (name, age, city)
        VALUES (?, ?, ?)""", (name, age, city))

    connection.commit()



def display_all_people(cursor):

    cursor.execute("""
        SELECT
            people.id,
            people.name,
            people.age,
            people.city,
            colors.name
        FROM people
        LEFT JOIN colors
        ON people.color_id = colors.id
    """)

    people = cursor.fetchall()
    display_people(people)


def filter_people_by_name(cursor):

    name = input("Personne recherchée : ")

    cursor.execute("""
        SELECT
            people.id,
            people.name,
            people.age,
            people.city,
            colors.name
        FROM people
        LEFT JOIN colors
        ON people.color_id = colors.id
        WHERE LOWER(name) LIKE LOWER(?)
    """, (f"{name}%",))

    people = cursor.fetchall()
    display_people(people)


def filter_people_by_city(cursor):

    city = input("Ville recherchée : ")

    cursor.execute("""
        SELECT
            people.id,
            people.name,
            people.age,
            people.city,
            colors.name
        FROM people
        LEFT JOIN colors
        ON people.color_id = colors.id
        WHERE LOWER(city) LIKE LOWER(?)
    """, (f"{city}%",))

    people = cursor.fetchall()
    display_people(people)


def filter_people_by_age(cursor):

    age = int(input("Age : "))

    cursor.execute("""
        SELECT
            people.id,
            people.name,
            people.age,
            people.city,
            colors.name
        FROM people
        LEFT JOIN colors
        ON people.color_id = colors.id
        WHERE age = ?
    """, (age,))

    people = cursor.fetchall()
    display_people(people)


def update_person(cursor, connection):

    person_id = int(input("ID de la personne à modifier : "))
    name = input("Nouveau nom : ")
    age = int(input("Nouvel âge : "))
    city = input("Nouvelle ville : ")

    cursor.execute("""
        UPDATE people
        SET name = ?, age = ?, city = ?
        WHERE id = ?
    """, (name, age, city, person_id))

    connection.commit()


def delete_person(cursor, connection):

    person_id = int(input("ID de la personne à supprimer : "))

    cursor.execute("""
    DELETE FROM people
    WHERE id = ?
    """, (person_id,))

    connection.commit()