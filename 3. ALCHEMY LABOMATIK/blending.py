#blend_ingredients()
#│
#├── afficher inventaire
#├── choisir ingrédient 1
#├── choisir ingrédient 2
#└── retourner le mélange
#[4, 14]
   #↓
#récupérer les affinités de 4
#récupérer les affinités de 14
   #↓
#calculer l'affinité finale du mélange
   #↓
#???


from display import display_inventory_join_id_to_list_numbering, display_mixing_tools_join_id_to_list_numbering, COLORS, RESET


def blending_list(cursor):

    # affichage des mélangeurs
    mixing_tools_numbering = display_mixing_tools_join_id_to_list_numbering(cursor)
    print()

    # choix du joueur
    while True:
        
        choix = input("Instrument de mélange choisi : ")

        # récupération de l'equipment_id
        if choix.isdigit() and int(choix) in mixing_tools_numbering:
            mixing_tool_id = mixing_tools_numbering[int(choix)]
            break

        print("choix invalide")

    # récupération capacity
    cursor.execute("""
        SELECT capacity
        FROM mixing_tools
        WHERE equipment_id = ?
        """, (mixing_tool_id,))
            
    result = cursor.fetchone()
    capacity = result[0]
            
    numbering = display_inventory_join_id_to_list_numbering(cursor)
    print()

    blending_ingredients = []

    ingredients_name = []

    for _ in range(capacity):

        while True:
        
            choix = input("Ingrédient choisi : ")
        
            if choix.isdigit() and int(choix) in numbering:
                ingredient_id = numbering[int(choix)]
                blending_ingredients.append(ingredient_id)

                cursor.execute("""
                    SELECT 
                        ingredients.name,
                        rarities.color
                    FROM ingredients
                    JOIN rarities
                        ON rarities.id = ingredients.rarity_id
                    WHERE ingredients.id = ?
                    """, (ingredient_id,))
                
                result = cursor.fetchone()
                name = result[0]
                color = result[1]
                ingredients_name.append(name)
                print(f"{COLORS[color]}{name}{RESET}")
                print()

                break

            print("choix invalide")

    print(f"ID ingrédients du mélange : {blending_ingredients}")
    print()
    

    blending_affinities = {}

    for ingredient_id in blending_ingredients:

        cursor.execute("""
            SELECT 
                ingredient_affinities.affinity_id, 
                ingredient_affinities.value,
                affinities.icon
            FROM ingredient_affinities
            JOIN affinities
                ON affinities.id = ingredient_affinities.affinity_id
            WHERE ingredient_id = ?
            """, (ingredient_id,))

        result = cursor.fetchall()

        for affinity_id, value, icon in result:
            if affinity_id in blending_affinities:
                total_value = value + blending_affinities[affinity_id][0]
                blending_affinities[affinity_id] = (total_value, icon)

            else:
                blending_affinities[affinity_id] = (value, icon)

    for affinity_id, (value, icon) in blending_affinities.items():
        blending_affinities[affinity_id] = (round(value / capacity, 2), icon)

    print("Affinités finales du mélange :")

    for affinity_id, (value, icon) in blending_affinities.items():
        print(f"{icon} : {value}")
            
    
       
        