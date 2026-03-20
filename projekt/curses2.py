import curses
import csv

FIL = "C:/Users/max.valentin/Documents/TIATIL00S/projekt/db_products.csv"
COL_ID = 5
COL_NAME = 30
COL_PRICE = 15
COL_QTY = 15

def load_data(filename):
    products = []
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append({
                "id": int(row['id']),
                "name": row['name'],
                "description": row['description'],
                "price": float(row['price']),
                "quantity": int(row['quantity'])
            })
    return products

def save_data(products, filename):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "description", "price", "quantity"])
        writer.writeheader()
        writer.writerows(products)

def show_products(stdscr, products):
    curses.curs_set(0)
    stdscr.keypad(True)
    index = 0

    while True:
        stdscr.clear()

        # Titelrad
        header = (
            f"{'#'.ljust(COL_ID)}"
            f"{'Name'.ljust(COL_NAME)}"
            f"{'Price'.ljust(COL_PRICE)}"
            f"{'Qty'.ljust(COL_QTY)}"
        )
        stdscr.addstr(0, 0, header)
        stdscr.addstr(1, 0, "-" * (COL_ID + COL_NAME + COL_PRICE + COL_QTY))

        for i, j in enumerate(products):
            name = j['name']
            if len(name) > COL_NAME - 5:  
                name = name[:COL_NAME - 5] + "..."   

            line = (
                f"{str(j['id']).ljust(COL_ID)}"
                f"{name.ljust(COL_NAME)}"  #ÄNDRAT HÄR!!!!!!!!!!
                f"{str(j['price']).ljust(COL_PRICE)}"
                f"{str(j['quantity']).ljust(COL_QTY)}"
            )
            if i == index:
                stdscr.addstr(i + 2, 0, line, curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 0, line)

        stdscr.refresh()

        key = stdscr.getch()

        # Piltangenter upp/ner
        if key == curses.KEY_UP:
            index = max(0, index - 1)
        elif key == curses.KEY_DOWN:
            index = min(len(products) - 1, index + 1)
        # ESC för att avsluta
        elif key == 27:
            break

def main(stdscr):
    products = load_data(FIL)
    show_products(stdscr, products)

curses.wrapper(main)
