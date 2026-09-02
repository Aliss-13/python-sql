RED = "\033[91m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
DIM = "\033[2m"
LIGHT_PINK = "\033[38;5;218m"
LIGHT_GREEN = "\033[38;5;120m"
PURPLE = "\033[95m"
RESET = "\033[0m"

def display_customer(customers):
    for customer_id, name, city in customers:
        print(f'{customer_id} - {YELLOW}{name}{RESET} - Ville : {city}')


def display_product(products):
    for product_id, name, category, price, stock, purchase_price in products:
        print(f'{product_id} - {YELLOW}{name}{RESET} - {category} - Prix : {price} - Prix fournisseur : {purchase_price} - Stock disponible : {stock}')


def display_sale(sales):
    for sale_id, customer_id, product_id, quantity, current_price, selling_price, margin, revenue, date in sales:
        print(f'{sale_id} - {YELLOW}{customer_id}{RESET} - {LIGHT_PINK}{product_id}{RESET} x{quantity} - Prix actuel : {current_price} - Prix vente : {selling_price} - {GREEN}Marge : {margin}{RESET} - {BLUE}CA : {revenue}{RESET} - Date : {date}')


def display_product_revenue(sales):
    for number, (product_name, quantity, price, total_amount) in enumerate(sales, start=1):
        print(f"{number} - {YELLOW}{product_name}{RESET} - Quantité vendue : {quantity} - Prix : {price} - {BLUE}CA : {total_amount}{RESET}")


def display_revenue_from_customer(sales):
    for number, (customer_name, quantity, total_amount) in enumerate(sales, start = 1):
        print(f"{number} - {YELLOW}{customer_name}{RESET} - Objets vendus : {quantity} - {BLUE}CA : {total_amount}{RESET}")


def display_stock_purchase(stock_purchases):
    for stock_id, product_id, name, category, quantity, purchase_price, total_amount, date in stock_purchases:
        print(f"{stock_id} - {product_id} - {YELLOW}{name}{RESET} x{quantity} - {category} - Prix d'achat : {purchase_price} - {RED}Investissement : {total_amount}{RESET} - Date : {date}")