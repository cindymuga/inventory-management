import requests

BASE_URL = "http://127.0.0.1:5000"


def show_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        products = response.json()

        for product in products:
            print(product)
    else:
        print("Could not get inventory")


def add_item():
    barcode = input("Enter barcode: ")
    name = input("Enter product name: ")
    brand = input("Enter brand: ")
    price = float(input("Enter price: "))
    stock = int(input("Enter stock: "))

    data = {
        "barcode": barcode,
        "name": name,
        "brand": brand,
        "price": price,
        "stock": stock
    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=data
    )

    print(response.json())


def update_item():
    item_id = input("Enter item ID: ")
    price = float(input("Enter new price: "))
    stock = int(input("Enter new stock: "))

    data = {
        "price": price,
        "stock": stock
    }

    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )

    print(response.json())


def delete_item():
    item_id = input("Enter item ID: ")

    response = requests.delete(
        f"{BASE_URL}/inventory/{item_id}"
    )

    print(response.json())


def find_product():
    name = input("Enter product name: ")

    response = requests.get(
        f"{BASE_URL}/lookup",
        params={"name": name}
    )

    print(response.json())


def main():
    while True:
        print("\nInventory Management")
        print("1. View inventory")
        print("2. Add item")
        print("3. Update item")
        print("4. Delete item")
        print("5. Find product")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            show_inventory()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            find_product()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()