from display.display_utils import LIGHT_PINK, RESET

def display_all_achievements(cursor):

    cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.category,
            p.name AS parent_name,
            a.description
        FROM achievements AS a
        LEFT JOIN achievements AS p
            ON a.parent_id = p.id
        ORDER BY a.id
    """)

    result = cursor.fetchall()
    display_achievement(result)
    return result

def display_achievement(achievements):

    for achievement_id, name, category, parent_name, description in achievements:
        print(f'{achievement_id:<2} - {LIGHT_PINK}{name}{RESET} - Type : {category} - Relié à : {parent_name} - {description}')

