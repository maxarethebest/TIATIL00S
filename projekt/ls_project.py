import csv
import os
import locale
from colorama import Fore, Back



#Colors
GREY1 = "\033[38;2;128;128;128m"
YELLOW = Fore.YELLOW
LIGHTBLUE = Fore.LIGHTBLUE_EX
GREY2 = "\033[38;2;128;128;128m"
DARKBLUE = "\033[38;2;0;0;128m"
WHITE = Fore.WHITE
RED = Fore.RED
GREEN = Fore.GREEN

def format_currency(value):
    return locale.currency(value,grouping=True)

products = []

def load_data(filename): 
    with open(filename, "r") as file:       #Öppnar fil i läs-läge
        reader = csv.DictReader(file)
        for row in reader:      #loopar genom filen, gör till dicten "products"
            id = int(row['id'])
            name = row['name']
            desc = row['description']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            products.append(
                {                   
                    "id": id,       
                    "name": name,
                    "description": desc,
                    "price": price,
                    "quantity": quantity
                }
            )
    return products

def save_data(products, filename):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "description", "price", "quantity"])
        writer.writeheader()
        writer.writerows(products)

def make_change(products):                          #Låter dig göra ändringar i products av nedanstående val
    change_type = input('''Vad vill du göra?
                        
Visa produkt (v):
Lägg till produkt (a):
Ändra produkt (c)
Ta bort produkt (r):\n''')
    match change_type:
        case "v":
            view_product(products)
        case "a":
            add_product(products)
        case "c":
            change_product(products)
        case "r":
            remove_product(products)
        case _:
            print("ERROR! Kontrollera inmatning. (Felkod 01)")

def view_product(products): #Visar namn, desc, quantity, och price av inmatat input
    try:
        viewed_id = int(input("Mata in ID för produkt att visa: "))
    except:
        print("ERROR! Kontrollera inmatning. (Felkod 02)")
        return

    # Find the product with matching id
    # if found:
    for i in products:
        if i["id"] == viewed_id:
            print(YELLOW + "Name: " + WHITE + i["name"] + ", " + LIGHTBLUE + "Description: " + WHITE + i["description"] + ", " + DARKBLUE + "Quantity: " + WHITE + str(i["quantity"]) + ", " + GREY2 + ", Price: " + WHITE + str(i["price"]))
            break
    else:
        print("Hittade inte ID, kontrollera inmatning.")

def add_product(products):
    new_name = input("Mata in " + YELLOW + "namn " + WHITE + "för ny produkt: ")
    new_desc = input("Mata in " + LIGHTBLUE +  "beskrivning " + WHITE + "för ny produkt: ")
    try:
        new_quantity = int(input("Mata in " + DARKBLUE + "antal " + WHITE + "för ny produkt: "))
    except:
        print("ERROR! Kontrollera inmatning. (Felkod 11)")
        return
    try:
        new_price = int(input("Mata in " + GREY2 + "pris " + WHITE + "för ny produkt: "))
    except:
        print("ERROR! Kontrollera inmatning. (Felkod 12)")
        return
        
    new_id = max(products, key=lambda id: id["id"])["id"] + 1
    products.append(
    {
        "id": new_id,
        "name": new_name,
        "description": new_desc,
        "price": new_price,
        "quantity": new_quantity
    })
    save_data(products, FIL)
    print(f"Produkt sparad till ID {new_id}.")

def change_product(products):
    change_id = input('''Mata in ID för produkt att ta ändra\n(Skriv "x" för att få en lista på alla produkter): ''')
    if change_id == "x" or change_id == "X":
        for id in products:
            print(GREY1 + "ID: " + WHITE + str(id["id"]) + " " + YELLOW + "Name: " + WHITE + id["name"])
        change_id = input('''Mata in ID för produkt att ta ändra: ''')

    while True:
        try:
            change_id = int(change_id)
            break
        except:
            print("ERROR! Kontrollera inmatning. (Felkod 41)")
            change_id = input('''Mata in ID för produkt att ta ändra: ''')
    
    for i in products:
        if i["id"] == change_id:
            print(YELLOW + "Name: " + WHITE + i["name"] + ", " + LIGHTBLUE + "Description: " + WHITE + i["description"] + ", " + DARKBLUE + "Quantity: " + WHITE + str(i["quantity"]) + ", " + GREY2 + ", Price: " + WHITE + str(i["price"]))
            break
    change_property = input("Vad vill du ändra?\n1. Namn\n2. Description\n3. Pris\n4. Antal\n\n")
    
    match(change_property):
        case "Name" | "name" | "N"| "n" | "1":
            new_name = input("Nuvarande namn är " + YELLOW + products[change_id]["name"] + WHITE + ", vad vill du ändra det till?: ")
            products[change_id]["name"] = new_name
        case "Description" | "description" | "Desc" | "desc" | "D" | "d" | "2":
            new_description = input("Nuvarande beskrivning är " + LIGHTBLUE + products[change_id]["description"] + WHITE + ", vad vill du ändra den till?: ")
            products[change_id]["description"] = new_description
        case "Price" | "price" | "P" | "p" | "3":
            while True:
                try: 
                    new_price = float(input("Nuvarande pris är " + GREY2 + str(products[change_id]["price"]) + WHITE + ", vad vill du ändra det till?: "))
                    products[change_id]["price"] = new_price
                    break
                except:
                    print("ERROR! Kontrollera inmatning. (Felkod 43)")
        case "Quantity" | "quantity" | "Q" | "q" | "4":
            while True:
                try:
                    new_quantity = int(input("Nuvarande antal är " + DARKBLUE + str(products[change_id]["quantity"]) + WHITE + ", vad vill du ändra det till?: "))
                    products[change_id]["quantity"] = new_quantity
                except:
                    print("ERROR! Kontrollera inmatning. (Felkod 44)")
        case _:
            print("ERROR! Kontrollera inmatning. (Felkod 42)")
    save_data(products, FIL)

def remove_product(products):
    remove_id = input('''Mata in ID för produkt att ta bort\n(Skriv "x" för att få en lista på alla produkter): ''')
    if remove_id == "x" or remove_id == "X":
        for id in products:
            print(GREY1 + "ID: " + WHITE + str(id["id"]) + " " + YELLOW + "Name: " + WHITE + id["name"])
        remove_id = input('''Mata in ID för produkt att ta bort: ''')
            
    while True:
        try:
            remove_id = int(remove_id)
            break
        except:
            print("ERROR! Kontrollera inmatning. (Felkod 21)")
            remove_id = input('''Mata in ID för produkt att ta bort: ''')
    for i, j in enumerate(products):
        if i == remove_id:
            print(GREY1 + "ID: " + WHITE + str(products[i]["id"]) + " " + YELLOW + "Name: " + WHITE + products[i]["name"] + ", " + LIGHTBLUE+ "Description: " + WHITE + products[i]["description"] + ", " + DARKBLUE + "Quantity: " + WHITE + str(products[i]["quantity"]) + ", " + GREY2 + "Price: " + WHITE + str(products[i]["price"]))
            double_check = input("Are you sure you want to remove this product? (" + GREEN + "Y" + WHITE + "/" + RED + "N" + WHITE + "): ").lower()
            if double_check == "y": 
                products.remove(j)
                print("Product removed.")
                break
            elif double_check == "n":
                print("Remove product cancelled.", end=" ")
    save_data(products, FIL)


FIL = "C:/Users/max.valentin/Documents/TIATIL00S/projekt/db_products.csv"

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')
# print(load_data(FIL))



load_data(FIL)


make_change(products)

while True:
    
    done = input("Do you want to make more changes? (" + GREEN + "Y" + WHITE + "/" + RED + "N" + WHITE + "): ").lower()
    if done == "n":
        break
    elif done == "y":
        make_change(products)
    else:
        print("ERROR! Kontrollera inmatning. (Felkod 03)")
        break
    