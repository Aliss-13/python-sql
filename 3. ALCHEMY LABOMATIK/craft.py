#5. Vérifier le feu / creuset

#6. Si tout est OK → demander la destination
               #↓
       #┌──────────────┐
       #↓              ↓
#product_inventory  shop_inventory
   
#8. Marquer la recette comme fabriquée
#9. COMMIT

from display import display_player_recipes_join_id_to_list_numbering

def craft_recipe(cursor, connection):

    # affichage des recettes connues  

    player_recipes = display_player_recipes_join_id_to_list_numbering(cursor)

    # choix du joueur

    while True:
            
        choix = input("Recette choisie : ")

        # récupération de l'identifiant de la recette

        if choix.isdigit() and 1 <= int(choix) <= len(player_recipes):
            recipe_id = player_recipes[int(choix)]
            break
            
        print("Choix invalide.")


    # récupération ingrédients + quantité

    cursor.execute("""
        SELECT 
            ingredient_id, 
            quantity
        FROM recipe_ingredients
        WHERE recipe_id = ?
    """, (recipe_id,))
                    
    result_recipe_ingredients = cursor.fetchall()

    cursor.execute("""
        SELECT 
            ingredient_id, 
            quantity
        FROM inventory
    """)
                        
    result_inventory = cursor.fetchall()

    
    inventory_has_required_ingredients = True

    for ingredient_id, required_quantity in result_recipe_ingredients: 
    # | for a, b in liste_de_tuples: | signifie : « Pour chaque tuple de deux éléments, mets le premier dans a et le second dans b. »
        
        ingredient_found = False

        for inventory_ingredient_id, inventory_quantity in result_inventory: 
            
            if ingredient_id == inventory_ingredient_id: 
                if required_quantity <= inventory_quantity:
                    ingredient_found = True
                 
        if not ingredient_found:
            inventory_has_required_ingredients = False

    if inventory_has_required_ingredients:

        for ingredient_id, required_quantity in result_recipe_ingredients:

            cursor.execute("""
                UPDATE inventory
                SET quantity = quantity - ?
                WHERE ingredient_id = ?
            """, (required_quantity, ingredient_id))
                    
        connection.commit()
        
        print("Recette fabriquée !")


    # récupération contenants + quantité
    
        cursor.execute("""
            SELECT 
                container_equipment_id
            FROM recipes
            WHERE id = ?
        """, (recipe_id,))
                        
        result = cursor.fetchone()
        container_equipment_id = result[0]
    
        cursor.execute("""
            SELECT
                equipment_id, 
                quantity
            FROM container_inventory
        """)
                            
        result_container_inventory = cursor.fetchall()
    
        
        container_inventory_has_required_containers = True
    
        container_found = False
    
        for equipment_id, quantity in result_container_inventory: 
                
            if container_equipment_id == equipment_id: 
                if quantity >= 1:
                    container_found = True
                     
        if not container_found:
            container_inventory_has_required_containers = False
    
        if container_inventory_has_required_containers:
    
            cursor.execute("""
                UPDATE container_inventory
                SET quantity = quantity - ?
                WHERE equipment_id = ?
            """, (1, container_equipment_id))
                        
        connection.commit()
            
          

                  

                    

                

