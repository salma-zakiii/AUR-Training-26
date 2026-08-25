def read_stock():
    stock = {}
    try:
        with open("stock.txt", "r") as file:
            for line in file:
                name, quantity = line.strip().split(",")
                stock[name.lower()] = int(quantity)
    except (FileNotFoundError, ValueError):
        print("Error reading stock.txt.")
        return None
    return stock

def show_stock(stock):
    print("Current stock:")
    number = 1
    for name in stock:
        print(number, ".", name, ":", stock[name])
        number += 1

def main():
    stock = read_stock()
    print(stock)
    if stock is None:
        return

    while True:
        print("\n1. Add stock")
        print("2. Remove stock")
        print("3. Show stock")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            show_stock(stock)
            item = input("Enter stock name or ID: ").lower()
            if item.isdigit():
                item_id = int(item)
                names = list(stock.keys())
                if 1 <= item_id <= len(names):
                    item = names[item_id - 1]
                else:
                    print("Invalid ID.")
                    continue

            amount = int(input("Enter how much to add: "))
            stock[item] = stock.get(item, 0) + amount
        elif choice == "2":
            show_stock(stock)
            item = input("Enter stock name or ID: ").lower()
            if item.isdigit():
                item_id = int(item)
                names = list(stock.keys())

                if 1 <= item_id <= len(names):
                    item = names[item_id - 1]
                else:
                    print("Invalid ID.")
                    continue

            if item not in stock:
                print("Stock not found.")
                continue

            amount = int(input("Enter how much to remove: "))
            if amount <= stock[item]:
                stock[item] -= amount
            else:
                print("Not enough stock.")

        elif choice == "3":
            show_stock(stock)

        elif choice == "4":
            with open("stock.txt", "w") as file:
                for name in stock:
                    file.write(f"{name},{stock[name]}\n")

            print("Stock saved.")
            break

        else:
            print("Invalid choice.")


main()