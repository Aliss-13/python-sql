from display import display_customer, display_product, display_sale, display_product_revenue, display_revenue_from_customer

def menu(cursor, connection):
    
    while True:
        print()
        print("----------MENU----------")
        print("[1] Ajouter un produit")
        print("[2] Afficher les produits")
        print("[3] Ajouter un client")
        print("[4] Afficher les clients")
        print("[5] Ajouter une vente")
        print("[6] Afficher les ventes")
        print("[7] Chiffre d'affaires")
        print("[8] Best-sellers")
        print("[9] Meilleurs clients")
        print("[q] Quitter")

        choix = input("> ")

        if choix == "1":
            add_product(cursor, connection)

        if choix == "2":
            all_products(cursor)

        if choix == "3":
            add_customer(cursor, connection)

        if choix == "4":
            all_customers(cursor)

        if choix == "5":
            add_sale(cursor, connection)
            
        if choix == "6":
            all_sales(cursor)

        if choix == "7":
            total_revenue(cursor)

        if choix == "8":
            products_revenues(cursor)

        if choix == "9":
            revenues_from_customers(cursor)

        elif choix == "q":
            return
            
        else:
            print("Choix invalide")

#--------------------------------------------------------- PRODUCTS -----------------------------------------

def add_product(cursor, connection):

    name = input("Nom : ")
    category = input("Catégorie : ")
    price = float(input("Prix : "))
    stock = int(input("Stock disponible : "))

    cursor.execute("""
        INSERT INTO products (name, category, price, stock)
        VALUES (?, ?, ?, ?)""", (name, category, price, stock))

    connection.commit()

def all_products(cursor):

    cursor.execute("""
        SELECT
            products.id,
            products.name,
            products.category,
            products.price,
            products.stock
        FROM products
    """)

    products = cursor.fetchall()
    display_product(products)

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

def add_sale(cursor, connection):

    all_customers(cursor)
    customer_id = int(input("Client : "))

    all_products(cursor)
    product_id = int(input("Produit : "))

    quantity = int(input("Quantité : "))

    cursor.execute("""
        SELECT stock
        FROM products
        WHERE id = ?
    """, (product_id,))

    stock = cursor.fetchone()[0]

    if stock >= quantity:

        cursor.execute("""
            UPDATE products
            SET stock = stock - ?
            WHERE id = ?
            """, (quantity, product_id,))

        date = input("Date (jj-mm-aa): ")

        cursor.execute("""
            INSERT INTO sales (customer_id, product_id, quantity, date)
            VALUES (?, ?, ?, ?)""", (customer_id, product_id, quantity, date)
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
        products.price * sales.quantity AS total,
        sales.date
    FROM sales
    JOIN customers
        ON sales.customer_id = customers.id
    JOIN products
        ON sales.product_id = products.id
    """)

    result = cursor.fetchall()
    display_sale(result)


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
    print(f"Chiffre d'affaires : {total_revenue}")


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