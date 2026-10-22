import random
from player_game.dialogues import SALE_DIALOGUES

BASE_SELL_TICKS = 5
last_sales = {}

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
        return True

    except Exception:
        connection.rollback()
        raise


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



        