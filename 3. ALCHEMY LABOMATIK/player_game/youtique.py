import random

from player_game.dialogues import SALE_DIALOGUES
from player_game.get_achievements import check_commercial_achievements

from display.display_utils import LIGHT_GREEN, RESET, DIM, COLORS, YELLOW, ORANGE, CYAN
from display.display_inventories import display_product_inventory
from display.display_shop_inventory import display_shop_inventory


BASE_SELL_TICKS = 5
last_sales = {}


def youtique():
    print(f"🐍 {LIGHT_GREEN}La Youtique© - Parce qu'il faut bien que je vende mes merdes 🤸 {RESET}")
    print(f"{DIM}   Récupère le flouze, le pèze, la moula, le pognon et à toi les gourgandines et l'opium !{RESET}")
    print()


def random_sale_dialogue(item):
    text = random.choice(SALE_DIALOGUES)
    return text.format(item=item)


def sell_recipe(cursor, connection, recipe_id):

    try:
        cursor.execute("""
            SELECT selling_price
            FROM recipes
            WHERE id = ?
        """, (recipe_id,))

        result = cursor.fetchone()

        if result is None:
            return False

        selling_price = result[0] # Déballer le tuple

        cursor.execute("""
            UPDATE shop_inventory
            SET quantity = quantity - 1
            WHERE recipe_id = ?
              AND quantity > 0
        """, (recipe_id,))

        if cursor.rowcount == 0:
            connection.rollback()
            return False

        cursor.execute("""
            UPDATE player
            SET money = money + ?
            WHERE id = 1
        """, (selling_price,))

        if cursor.rowcount == 0:
            raise ValueError("Joueur introuvable.")

        cursor.execute("""
            INSERT INTO sales_history (recipe_id, quantity)
            VALUES (?, 1)
        """, (recipe_id,))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    check_commercial_achievements(cursor)
    return True

    
def auto_sell(cursor, connection, game_tick):

    cursor.execute("""
        SELECT
            shop_inventory.recipe_id,
            recipes.name,
            shop_inventory.quantity,
            recipes.selling_price, 
            recipes.demand
        FROM shop_inventory
        
        JOIN recipes
            ON recipes.id = shop_inventory.recipe_id
        """)

    products = cursor.fetchall()

    for recipe_id, recipe_name, quantity, selling_price, demand in products:

        interval = round(BASE_SELL_TICKS / demand)

        if recipe_id not in last_sales:
            last_sales[recipe_id] = game_tick
            continue

        if game_tick - last_sales[recipe_id] >= interval:

            if quantity == 0:
                last_sales[recipe_id] = game_tick
                continue

            if quantity >= 1:

                try:
             
                    cursor.execute("""
                        UPDATE shop_inventory
                        SET quantity = quantity - ?
                        WHERE recipe_id = ?
                    """, (1, recipe_id))

                    cursor.execute("""
                        UPDATE player
                        SET money = money + ?
                        WHERE id = ?
                    """, (selling_price, 1))


                    cursor.execute("""
                        SELECT recipe_id
                        FROM sales_history
                    """)
                    
                    sales_history_ids = cursor.fetchall()
                    sales_history_ids_unpacked = [sales_history_id[0] for sales_history_id in sales_history_ids]

                    if recipe_id not in sales_history_ids_unpacked:
                        
                        cursor.execute("""
                            INSERT INTO sales_history (recipe_id, quantity)
                            VALUES (?, ?)
                        """, (recipe_id, 1))
                        
                    else:
                        cursor.execute("""
                            UPDATE sales_history
                            SET quantity = quantity + ?
                            WHERE recipe_id = ?
                        """, (1, recipe_id))

                    
                except Exception:
                    connection.rollback()
                    raise

                connection.commit()

                last_sales[recipe_id] = game_tick

                print(f"\nVous avez vendu {recipe_name} !")
                print(random_sale_dialogue(recipe_name))
                print(f"💰 +{selling_price} pièces !")
                print()      

#-------------------------------------- Transferts Inventaire → Youtique© et vice-versa ----------------------------------------------

def menu_transfer_products(cursor, connection):

    while True:

        print("\n📦 TRANSFERT DE PRODUITS\n")
        print("[1] 📓 Inventaire → Youtique©")
        print("[2] 🐍 Youtique© → Inventaire")
        print("[r] Retour")

        choice = input("Choix : ")

        if choice == "1":
            source = "product_inventory"
            destination = "shop_inventory"
            products = display_product_inventory(cursor)

        elif choice == "2":
            source = "shop_inventory"
            destination = "product_inventory"
            products = display_shop_inventory(cursor)

        elif choice == "r":
            break

        else:
            print("Choix invalide.")
            continue

        check_transfert(cursor, connection, source, destination, products)


def check_transfert(cursor, connection, source, destination, products):

    if not products:
        print("Aucun produit disponible pour ce transfert.")
        return

    # Choix du produit à transférer

    try:
        product_choice = int(input("Numéro du produit à transférer : "))

        if not 1 <= product_choice <= len(products):
            print("Produit invalide.")
            return

        selected_product = products[product_choice - 1]

        recipe_id = selected_product[0]
        available_quantity = selected_product[4]

    except ValueError:
        print("Veuillez entrer un numéro valide.")
        return

    # Quantité

    try:
        quantity = int(input(f"Quantité à transférer (max {available_quantity}) : "))

        if not 1 <= quantity <= available_quantity:
            print("Quantité invalide.")
            return

    except ValueError:
        print("Veuillez entrer un nombre entier.")
        return

    # Appel de la fonction de transfert

    try:
        transfer_product(
            cursor, connection,
            recipe_id, quantity,
            source, destination
        )

        print(f"✅ {quantity} produit(s) transféré(s) !")

    except ValueError as error:
        print(error)


def transfer_product(cursor, connection, recipe_id, quantity, source, destination):

    allowed_tables = {"product_inventory", "shop_inventory"}

    if source not in allowed_tables or destination not in allowed_tables:
        raise ValueError("Table d'inventaire invalide.")

    if source == destination:
        raise ValueError("La source et la destination sont identiques.")

    if quantity <= 0:
        raise ValueError("La quantité doit être positive.")

    try:
        cursor.execute(f"""
            UPDATE {source}
            SET quantity = quantity - ?
            WHERE recipe_id = ?
            AND quantity >= ?
        """, (quantity, recipe_id, quantity))

        if cursor.rowcount == 0:
            raise ValueError("Stock insuffisant pour ce transfert.")

        cursor.execute(f"""
            INSERT INTO {destination} (recipe_id, quantity)
            VALUES (?, ?)
            ON CONFLICT(recipe_id)
            DO UPDATE SET quantity = quantity + excluded.quantity
        """, (recipe_id, quantity))

        connection.commit()

    except Exception:
        connection.rollback()
        raise


# UPDATE ... AND quantity >= ?
# On retire les produits uniquement si la quantité disponible est suffisante. Cela empêche de créer un stock négatif.

# cursor.rowcount == 0
# Si aucune ligne n'a été modifiée, c'est que la recette n'existe pas dans le stock source ou que la quantité est insuffisante.

# excluded.quantity
# Dans ON CONFLICT, excluded désigne les valeurs qu'on tentait d'insérer. Ici, c'est donc la quantité transférée.

#-------------------------------------------------- Statistiques de vente -------------------------------------------------------

def get_shop_sales_report(cursor):

    cursor.execute("""
        SELECT
            recipes.id,
            recipes.name,
            rarities.color,
            recipe_types.name,
            COALESCE(SUM(sales_history.quantity), 0) AS total_sold,
            COALESCE(SUM(sales_history.quantity), 0) * recipes.selling_price AS revenue,
            COALESCE(shop_inventory.quantity, 0) AS stock

        FROM recipes

        JOIN rarities
            ON rarities.id = recipes.rarity_id

        JOIN recipe_types
            ON recipe_types.id = recipes.type_id

        JOIN sales_history
            ON sales_history.recipe_id = recipes.id

        LEFT JOIN shop_inventory
            ON shop_inventory.recipe_id = recipes.id

        GROUP BY recipes.id
        ORDER BY revenue DESC
       
        
    """)
    result = cursor.fetchall()
    return result

# SUM(sales_history.quantity) additionne toutes les quantités vendues pour chaque recette.
# COALESCE(..., 0) remplace une valeur NULL par 0. C'est particulièrement utile pour les produits qui ne sont plus présents dans le stock de la Youtique©.
# GROUP BY recipes.id regroupe les ventes d'une même recette pour obtenir un bilan par produit.
# ORDER BY revenue DESC classe les produits du plus gros chiffre d'affaires au plus petit.
# Le JOIN sales_history signifie que le bilan affiche uniquement les produits ayant un historique de vente. C'est cohérent pour un bilan commercial.


def display_shop_sales_report(cursor):

    result = get_shop_sales_report(cursor)
    print(f"{LIGHT_GREEN}🐍 BILAN COMMERCIAL{RESET}")
    print()

    total_sold_global = 0
    revenue_global = 0

    for display_number, product in enumerate(result, start=1):

        recipe_id, name, color, type, total_sold, revenue, stock = product
        total_sold_global = total_sold_global + total_sold
        revenue_global = revenue_global + revenue
        print(f"{display_number:<2} - {CYAN}CA : {revenue:<3}{RESET} - {ORANGE}Ventes : {total_sold:<2}{RESET} - "
              f"{COLORS[color]}{name}{RESET} - {YELLOW}{type}{RESET}")
        
    print()
    print(f"{LIGHT_GREEN}🐍 TOTAL{RESET} - {CYAN}CA : {revenue_global}{RESET} - {ORANGE}Ventes : {total_sold_global}{RESET}")
        
        

