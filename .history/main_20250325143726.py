from product import Product
from warehouse import Warehouse

def print_menu():
    """Display the main menu options."""
    print("\n===== Warehouse Inventory Management System =====")
    print("1. Add new product")
    print("2. Store product in warehouse")
    print("3. Retrieve product from warehouse")
    print("4. View warehouse layout")
    print("5. Search for product")
    print("6. View product details")
    print("7. Exit")
    print("================================================")

def get_integer_input(prompt, min_value=None, max_value=None):
    """Get validated integer input from the user."""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

def add_product(warehouse):
    """Add a new product to the warehouse inventory."""
    print("\n--- Add New Product ---")
    name = input("Enter product name: ")
    sku = input("Enter product SKU: ")
    
    if sku in warehouse.products:
        print("A product with this SKU already exists.")
        return
    
    price = float(input("Enter product price: $"))
    quantity = get_integer_input("Enter initial quantity: ", 0)
    
    product = Product(name, sku, price, quantity)
    warehouse.add_product(product)
    print(f"Product '{name}' added successfully.")

def store_product(warehouse):
    """Store a product at a specific location in the warehouse."""
    print("\n--- Store Product ---")
    sku = input("Enter product SKU: ")
    
    if sku not in warehouse.products:
        print("Product not found.")
        return
    
    product = warehouse.products[sku]
    print(f"Selected: {product}")
    
    quantity = get_integer_input("Enter quantity to store: ", 1)
    
    if quantity > product.quantity:
        print("Not enough quantity available.")
        return
    
    row = get_integer_input("Enter row (0-{}): ".format(warehouse.rows-1), 0, warehouse.rows-1)
    col = get_integer_input("Enter column (0-{}): ".format(warehouse.cols-1), 0, warehouse.cols-1)
    
    if warehouse.store_product(sku, quantity, row, col):
        print("Product stored successfully.")
    else:
        print("Failed to store product. Check location capacity.")

def retrieve_product(warehouse):
    """Retrieve a product from a specific location in the warehouse."""
    print("\n--- Retrieve Product ---")
    sku = input("Enter product SKU: ")
    
    if sku not in warehouse.products:
        print("Product not found.")
        return
    
    locations = warehouse.find_product(sku)
    
    if not locations:
        print("This product is not stored in any location.")
        return
    
    print("Product found at these locations:")
    for i, (r, c) in enumerate(locations):
        location = warehouse.grid[r][c]
        print(f"{i+1}. {location.get_location_code()} - Quantity: {location.inventory[sku]}")
    
    choice = get_integer_input("Select location (number): ", 1, len(locations))
    row, col = locations[choice-1]
    
    quantity = get_integer_input("Enter quantity to retrieve: ", 1)
    
    if warehouse.retrieve_product(sku, quantity, row, col):
        print("Product retrieved successfully.")
    else:
        print("Failed to retrieve product. Not enough quantity at this location.")

def main():
    """Main function to run the warehouse management system."""
    print("Welcome to the Warehouse Inventory Management System!")
    rows = get_integer_input("Enter number of rows for the warehouse: ", 1, 26)
    cols = get_integer_input("Enter number of columns for the warehouse: ", 1, 99)
    
    warehouse = Warehouse(rows, cols)
    
    while True:
        print_menu()
        choice = get_integer_input("Enter your choice (1-7): ", 1, 7)
        
        if choice == 1:
            add_product(warehouse)
        elif choice == 2:
            store_product(warehouse)
        elif choice == 3:
            retrieve_product(warehouse)
        elif choice == 4:
            print("\n--- Warehouse Layout ---")
            print("Legend: □ Empty | ▲ <50% | ■ <100% | ▓ Full")
            print(warehouse.visualize())
        elif choice == 5:
            sku = input("\nEnter product SKU to search: ")
            locations = warehouse.find_product(sku)
            
            if not locations:
                print("Product not found in any location.")
            else:
                print(f"Product found at {len(locations)} locations:")
                for r, c in locations:
                    loc = warehouse.grid[r][c]
                    print(f"- {loc.get_location_code()}: {loc.inventory[sku]} units")
        elif choice == 6:
            sku = input("\nEnter product SKU: ")
            if sku in warehouse.products:
                print(warehouse.products[sku])
            else:
                print("Product not found.")
        elif choice == 7:
            print("Thank you for using the Warehouse Inventory Management System!")
            break

if __name__ == "__main__":
    main()
