from datetime import datetime
from zoneinfo import ZoneInfo

from display import display_customer, display_product, display_sale, display_product_revenue, display_revenue_from_customer
from display import display_stock_purchase


RED = "\033[91m"
GREEN = "\033[32m"
BLUE = "\033[94m"
LIGHT_GREEN = "\033[38;5;120m"
RESET = "\033[0m"
# --------------------------------------------------------- MENU --------------------------------------------------------------

def menu(cursor, connection):

    while True:

        print()
        print("========== MAGIQUE BOUTIQUE ==========")
        print("[1] 🧺 PRODUITS")
        print("[2] 📦 STOCK")
        print("[3] 👥 CLIENTS")
        print("[4] 🛒 VENTES")
        print("[5] 📊 STATS")
        print("[q] 🔚 Quitter")

        choix = input("> ")

        if choix == "1":
            menu_products(cursor, connection)

        elif choix == "2":
            menu_stock(cursor, connection)

        elif choix == "3":
            menu_customers(cursor, connection)

        elif choix == "4":
            menu_sales(cursor, connection)

        elif choix == "5":
            menu_statistics(cursor)

        elif choix == "q":
            return

        else:
            print("Choix invalide")


def menu_products(cursor, connection):    

    while True:

        print()
        print("🧺 PRODUITS ")
        print("[1] Ajouter produit")
        print("[2] Afficher produits")
        print("[3] Modifier prix produit")
        print("[r] Retour")

        choix = input("> ")
        
        if choix == "1":
            add_product(cursor, connection)

        elif choix == "2":
            all_products(cursor)

        elif choix == "3":
            update_price(cursor, connection)

        elif choix == "r":
            return
            
        else:
            print("Choix invalide")


def menu_stock(cursor, connection):    

    while True:

        print()
        print("📦 STOCK ")
        print("[1] Ajouter stock")
        print("[2] Modifier prix fournisseur")
        print("[3] Afficher achats stock")
        print("[r] Retour")

        choix = input("> ")

        if choix == "1":
            add_stock(cursor, connection)

        elif choix == "2":
            update_purchase_price(cursor, connection)

        elif choix == "3":
            all_restocks(cursor)
            print()
            total_stock_cost(cursor)

        elif choix == "r":
            return
            
        else:
            print("Choix invalide")


def menu_customers(cursor, connection): 

    while True:

        print()
        print("👥 CLIENTS ")
        print("[1] Ajouter client")
        print("[2] Afficher clients")
        print("[r] Retour")

        choix = input("> ")

        if choix == "1":
            add_customer(cursor, connection)

        elif choix == "2":
            all_customers(cursor)

        elif choix == "r":
            return
            
        else:
            print("Choix invalide")


def menu_sales(cursor, connection):    

    while True:

        print()
        print("🛒 VENTES ")
        print("[1] Ajouter vente")
        print("[2] Supprimer vente")
        print("[3] Afficher ventes")
        print("[r] Retour")

        choix = input("> ")

        if choix == "1":
            add_sale(cursor, connection)

        elif choix == "2":
            delete_sale(cursor, connection)

        elif choix == "3":
            all_sales(cursor)
            print()
            total_revenue(cursor)
            print()
            total_margin(cursor)

        elif choix == "r":
            return
                    
        else:
            print("Choix invalide")


def menu_statistics(cursor):

    while True:

        print()
        print("📊 STATS ")
        print("[1] Chiffre d'affaires - Marge - Revenu net")
        print("[2] Classement meilleurs produits")
        print("[3] Classement meilleurs clients")
        print("[r] Retour")

        choix = input("> ")

              
        if choix == "1":
            total_revenue(cursor)
            print()
            total_margin(cursor)
            print()
            net_revenue(cursor)

        elif choix == "2":
            products_revenues(cursor)

        elif choix == "3":
            revenues_from_customers(cursor)

        elif choix == "r":
            return
            
        else:
            print("Choix invalide")

#--------------------------------------------------------- STOCKS -----------------------------------------

def add_stock(cursor, connection):

    all_products(cursor)

    product_id = int(input("Produit : "))
    added_stock = int(input("Stock à ajouter : "))

    cursor.execute("""
        SELECT purchase_price
        FROM products
        WHERE id = ?
    """, (product_id,))

    purchase_price = cursor.fetchone()[0]

    cursor.execute("""
        UPDATE products
        SET stock = stock + ?
        WHERE id = ?
    """, (added_stock, product_id))

    date = input("Date (jj-mm-aaaa, vide = aujourd'hui) : ")

    if not date:
        date = datetime.now(ZoneInfo("Europe/Paris")).strftime("%d-%m-%Y")

    cursor.execute("""
        INSERT INTO stock_purchases
            (product_id, quantity, unit_purchase_price, date)
        VALUES (?, ?, ?, ?)
    """, (product_id, added_stock, purchase_price, date))

    connection.commit()


def all_restocks(cursor):

    cursor.execute("""
        SELECT
            stock_purchases.id,
            products.id,
            products.name,
            products.category,
            stock_purchases.quantity,
            stock_purchases.unit_purchase_price,
            stock_purchases.unit_purchase_price * stock_purchases.quantity AS total,
            stock_purchases.date
        FROM stock_purchases
        JOIN products
            ON products.id = stock_purchases.product_id
    """)

    stock_purchases = cursor.fetchall()
    display_stock_purchase(stock_purchases)


def total_stock_cost(cursor):

    cursor.execute("""
        SELECT SUM(
            unit_purchase_price * quantity
        )
        FROM stock_purchases
    """)

    result = cursor.fetchone()
    total_cost = result[0]

    print(f"{RED}Coût total des réassorts : {total_cost}{RESET}")

#--------------------------------------------------------- PRODUCTS -----------------------------------------

def add_product(cursor, connection):

    name = input("Nom : ")
    category = input("Catégorie : ")
    price = float(input("Prix : "))
    stock = int(input("Stock disponible : "))
    purchase_price = float(input("Prix fournisseur : "))

    cursor.execute("""
        INSERT INTO products (name, category, price, stock, purchase_price)
        VALUES (?, ?, ?, ?, ?)""", (name, category, price, stock, purchase_price))

    connection.commit()


def all_products(cursor):

    cursor.execute("""
        SELECT
            products.id,
            products.name,
            products.category,
            products.price,
            products.stock, 
            products.purchase_price
        FROM products
    """)

    products = cursor.fetchall()
    display_product(products)


def update_price(cursor, connection):

    all_products(cursor)

    product_id = int(input("Produit : "))
    new_price = float(input("Nouveau prix : "))

    cursor.execute("""
        UPDATE products
        SET price = ?
        WHERE id = ?
        """, (new_price, product_id,))

    connection.commit()


def update_purchase_price(cursor, connection):

    all_products(cursor)

    product_id = int(input("Produit : "))
    new_price = float(input("Nouveau prix fournisseur : "))

    cursor.execute("""
        UPDATE products
        SET purchase_price = ?
        WHERE id = ?
        """, (new_price, product_id,))

    connection.commit()

#--------------------------------------------------------- CUSTOMERS -----------------------------------------

def add_customer(cursor, connection):

    name = input("Nom : ")
    city = input("Ville : ")

    cursor.execute("""
        INSERT INTO customers (name, city)
        VALUES (?, ?)""", (name, city)
        )

    connection.commit()


def all_customers(cursor):

    cursor.execute("""
        SELECT
            customers.id,
            customers.name,
            customers.city
        FROM customers
    """)

    customers = cursor.fetchall()
    display_customer(customers)

#--------------------------------------------------------- SALES -----------------------------------------
    
def delete_sale(cursor, connection):

    all_sales(cursor)
    sale_id = int(input("Vente à supprimer : "))

    cursor.execute("""
        SELECT 
            quantity,
            product_id
        FROM sales
        JOIN products
            ON sales.product_id = products.id
        WHERE sales.id = ?
    """,(sale_id,))

    sale = cursor.fetchone()
    quantity = sale[0]
    product_id = sale[1]

    cursor.execute("""
        UPDATE products
        SET stock = stock + ?
        WHERE id = ?
        """, (quantity, product_id,))
        
    cursor.execute("""
        DELETE FROM sales
        WHERE id = ?
    """, (sale_id,))

    connection.commit()


def add_sale(cursor, connection):

    all_customers(cursor)
    customer_id = int(input("Client : "))

    all_products(cursor)
    product_id = int(input("Produit : "))

    quantity = int(input("Quantité : "))

    cursor.execute("""
        SELECT stock, price, purchase_price
        FROM products
        WHERE id = ?
    """, (product_id,))

    sale = cursor.fetchone()
    stock = sale[0]
    unit_price = sale[1]
    unit_purchase_price = sale[2]

    if stock >= quantity:

        cursor.execute("""
            UPDATE products
            SET stock = stock - ?
            WHERE id = ?
            """, (quantity, product_id,))

        date = input("Date (jj-mm-aaaa, vide = aujourd'hui) : ")

        if not date:
            date = datetime.now(ZoneInfo("Europe/Paris")).strftime("%d-%m-%Y")

        cursor.execute("""
            INSERT INTO sales (customer_id, product_id, quantity, unit_price, unit_purchase_price, date)
            VALUES (?, ?, ?, ?, ?, ?)""", (customer_id, product_id, quantity, unit_price, unit_purchase_price, date)
            )

        connection.commit()


    else:
        print("Stock insuffisant")
        return


def all_sales(cursor):

    cursor.execute("""
    SELECT
        sales.id,
        customers.name,
        products.name,
        sales.quantity,
        products.price AS prix_actuel,
        sales.unit_price AS prix_vente,
        (sales.unit_price - sales.unit_purchase_price) * quantity AS margin,
        sales.unit_price * quantity AS revenue,
        sales.date
    FROM sales
    JOIN customers
        ON sales.customer_id = customers.id
    JOIN products
        ON sales.product_id = products.id
    """)

    result = cursor.fetchall()
    display_sale(result)

#--------------------------------------------------------- REVENUE, MARGIN -----------------------------------------

def net_revenue(cursor):

    cursor.execute("""
        SELECT SUM(
            (unit_price - unit_purchase_price) * quantity
        )
        FROM sales
    """)

    total_margin = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT SUM(
            unit_purchase_price * quantity
        )
        FROM stock_purchases
    """)

    total_stock_cost = cursor.fetchone()[0] or 0

    net_revenue = total_margin - total_stock_cost

    print(f"{LIGHT_GREEN}Revenu net : {net_revenue}{RESET}")


def total_revenue(cursor):

    cursor.execute("""
    SELECT
        SUM(products.price * sales.quantity) AS total
    FROM sales
    JOIN products
    ON sales.product_id = products.id
    """)

    result = cursor.fetchone()
    total_revenue = result[0]
    print(f"{BLUE}Chiffre d'affaires : {total_revenue}{RESET}")


def total_margin(cursor):

    cursor.execute("""
    SELECT
        SUM((sales.unit_price - sales.unit_purchase_price) * sales.quantity) AS total
    FROM sales
    """)

    result = cursor.fetchone()
    total_margin = result[0]
    print(f"{GREEN}Marge nette : {total_margin}{RESET}")


def products_revenues(cursor):

    cursor.execute("""
    SELECT
        products.name,
        SUM(sales.quantity) AS total_sold,
        products.price,
        SUM(products.price * sales.quantity) AS total_revenue
    FROM sales
    JOIN products
        ON sales.product_id = products.id
    GROUP BY products.id 
    ORDER BY total_revenue DESC
    """)

    result = cursor.fetchall()
    display_product_revenue(result)


def revenues_from_customers(cursor):

    cursor.execute("""
    SELECT
        customers.name,
        SUM(sales.quantity),
        SUM(products.price * sales.quantity) AS total_revenue
    FROM sales
    JOIN products
        ON sales.product_id = products.id
    JOIN customers
        ON sales.customer_id = customers.id
    GROUP BY customers.id 
    ORDER BY total_revenue DESC
    """)

    result = cursor.fetchall()
    display_revenue_from_customer(result)