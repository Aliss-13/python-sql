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


from display import display_inventory


def blending_list(cursor):

    display_inventory(cursor)
    print()

    blending_ingredients = []

    for _ in range(2):

        while True:
        
            choix = input("Ingrédient choisi : ")

            cursor.execute("""
                SELECT ingredient_id
                FROM inventory
                WHERE ingredient_id = ?
                """, (choix,))
                
            result = cursor.fetchone()
        
            if choix.isdigit() and result is not None:
                ingredient_id = int(choix)
                blending_ingredients.append(ingredient_id)
                break

            print("choix invalide")

    print(blending_ingredients)

    blending_affinities = {}

    for ingredient_id in blending_ingredients:

        cursor.execute("""
            SELECT 
                ingredient_affinities.affinity_id, 
                ingredient_affinities.value
            FROM ingredient_affinities
            WHERE ingredient_id = ?
            """, (ingredient_id,))

        result = cursor.fetchall()

        for affinity_id, value in result:
            if affinity_id in blending_affinities:
                total_value = value + blending_affinities[affinity_id]
                blending_affinities[affinity_id] = total_value

            else:
                blending_affinities[affinity_id] = value

    for affinity_id, value in blending_affinities.items():
        blending_affinities[affinity_id] = round(value / 2, 2)

    print(blending_affinities)
            
    
       
        