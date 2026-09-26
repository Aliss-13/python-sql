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
from discoveries import discover_recipe


def blending_ingredients(cursor):

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

    return blending_affinities, capacity


def join_corresponding_recipe_to_blend(cursor):

    blending_affinities, capacity = blending_ingredients(cursor)

    cursor.execute("""
        SELECT 
            recipe_discovery.recipe_id, 
            recipe_discovery.number_of_ingredients,
            recipe_discovery.affinity_id,
            recipe_discovery.value
        FROM recipe_discovery
        WHERE number_of_ingredients = ?
        ORDER BY recipe_discovery.recipe_id
        """, (capacity,))
    
    result = cursor.fetchall()

    current_recipe_id = None
    disc_affinities_ids = []
    affinities = 0
    corresponding_affinities = 0

    for disc_recipe_id, disc_number_of_ingredients, disc_affinity_id, disc_value in result:

        # Nouvelle recette
        if current_recipe_id != disc_recipe_id:

            # On vérifie la recette précédente
            if current_recipe_id is not None:

                # Le mélange ne doit pas avoir d'affinité supplémentaire
                extra_affinity = False

                for blending_affinity in blending_affinities:
                    if blending_affinity not in disc_affinities_ids:
                        extra_affinity = True

                if not extra_affinity and corresponding_affinities == affinities:
                    print("Correspondance trouvée !")
                    return current_recipe_id

            # On commence une nouvelle recette
            current_recipe_id = disc_recipe_id
            disc_affinities_ids = []
            affinities = 0
            corresponding_affinities = 0

        # On mémorise l'affinité demandée par la recette
        disc_affinities_ids.append(disc_affinity_id)
        affinities += 1

        # L'affinité existe-t-elle dans le mélange ?
        if disc_affinity_id not in blending_affinities:
            print("Pas de correspondance.")
            continue

        # Si elle existe, on compare sa valeur
        blending_value, icon = blending_affinities[disc_affinity_id]

        if blending_value == disc_value:
            corresponding_affinities += 1
        else:
            print("Pas de correspondance.")

    # Vérification de la dernière recette
    if current_recipe_id is not None:

        extra_affinity = False

        for blending_affinity in blending_affinities:
            if blending_affinity not in disc_affinities_ids:
                extra_affinity = True

        if not extra_affinity and corresponding_affinities == affinities:
            print("Correspondance trouvée !")
            return current_recipe_id

    return None
        
            
        


    
        

                

           

                

                
