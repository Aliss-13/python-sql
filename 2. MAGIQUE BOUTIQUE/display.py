RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
DIM = "\033[2m"
LIGHT_PINK = "\033[38;5;218m"
PURPLE = "\033[95m"
RESET = "\033[0m"

def display_customer(customers):
    for customer_id, name, city in customers:
        print(f'{customer_id} - {YELLOW}{name}{RESET} - Ville : {city}')


def display_product(products):
    for product_id, name, category, price, stock in products:
        print(f'{product_id} - {YELLOW}{name}{RESET} - Catégorie : {category} - Prix : {price} - Stock disponible : {stock}')


def display_sale(sales):
    for id, customer_id, product_id, quantity, amount, date in sales:
        print(f'{id} - {YELLOW}{customer_id}{RESET} - {LIGHT_PINK}{product_id}{RESET} - Quantité : {quantity} - Montant : {amount} - Date : {date}')


def display_product_revenue(sales):
    for number, (product_name, quantity, price, total_amount) in enumerate(sales, start=1):
        print(f"{number} - {YELLOW}{product_name}{RESET} - Quantité vendue : {quantity} - Prix : {price} - {CYAN}CA : {total_amount}{RESET}")


def display_revenue_from_customer(sales):
    for number, (customer_name, quantity, total_amount) in enumerate(sales, start = 1):
        print(f"{number} - {YELLOW}{customer_name}{RESET} - Objets vendus : {quantity} - {CYAN}CA : {total_amount}{RESET}")