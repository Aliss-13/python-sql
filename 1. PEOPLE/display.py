def display_people(people):
    for person_id, name, age, city, color in people:
        print(f'ID : {person_id} - Nom : {name} - Age : {age} - Ville : {city} - Couleur : {color}')


def display_color_with_ages(people):
    for color, number, age_min, age_avg, age_max in people:
        print (f'Couleur : {color} - Nombre : {number} - Age min : {age_min} - Avg : {age_avg:.2f} - Age max : {age_max}')

def display_group(people):
    for city, people_number in people:
        print (f'Ville : {city} - Personnes : {people_number}')


def display_age(people):
    for city, people_age in people:
        print (f'Ville : {city} - Age moyen : {people_age}')


def display_color(people):
    for color, people_number in people:
        print (f'Couleur : {color} - Personnes : {people_number}')