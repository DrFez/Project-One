from warehouse import Warehouse
from data_storage import DataStorage

class CLIInterface:
    """Command-line interface for the inventory management system."""
    
    def __init__(self, user):
        self.user = user
        self.data_storage = DataStorage()
        self.warehouse = Warehouse(5, 8)
        self.warehouse.load_data()
    
    def log(self, action):
        """Append a timestamped log of user action."""
        self.data_storage.save_log(self.user, action)
    
    def run(self):
        """Run the CLI interface."""
        while True:
            print("\n--- Warehouse Management CLI ---")
            print("1. Add Product")
            print("2. Store Product")
            print("3. Retrieve Product")
            print("4. View Warehouse")
            print("5. Exit")
            choice = input("Enter your choice: ").strip()
            self.log(f"Chose menu option {choice}")
            
            if choice == "1":
                self.add_product()
            elif choice == "2":
                self.store_product()
            elif choice == "3":
                self.retrieve_product()
            elif choice == "4":
                self.view_warehouse()
            elif choice == "5":
                self.log("Exited CLI")
                self.warehouse.save_data(force=True)
                print("Data saved. Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def add_product(self):
        """Add a new product."""
        name = input("Enter product name: ").strip()
        sku = input("Enter SKU: ").strip()
        price = float(input("Enter price: "))
        quantity = int(input("Enter initial quantity: "))
        success = self.warehouse.add_product(Product(name, sku, price, quantity))
        if success:
            print(f"Product '{name}' added successfully.")
            self.log(f"Added product {name} (SKU:{sku}, price:{price}, qty:{quantity})")
        else:
            print("Product with this SKU already exists.")
    
    def store_product(self):
        """Store a product in the warehouse."""
        sku = input("Enter SKU: ").strip()
        quantity = int(input("Enter quantity: "))
        row = int(input("Enter row (0-indexed): "))
        col = int(input("Enter column (0-indexed): "))
        ok = self.warehouse.store_product(sku, quantity, row, col)
        if ok:
            print("Product stored successfully.")
            self.log(f"Stored SKU {sku}, qty {quantity} at ({row},{col})")
        else:
            print("Failed to store product. Check SKU, quantity, or location capacity.")
    
    def retrieve_product(self):
        """Retrieve a product from the warehouse."""
        sku = input("Enter SKU: ").strip()
        quantity = int(input("Enter quantity: "))
        row = int(input("Enter row (0-indexed): "))
        col = int(input("Enter column (0-indexed): "))
        ok = self.warehouse.retrieve_product(sku, quantity, row, col)
        if ok:
            print("Product retrieved successfully.")
            self.log(f"Retrieved SKU {sku}, qty {quantity} from ({row},{col})")
        else:
            print("Failed to retrieve product. Check SKU, quantity, or location.")
    
    def view_warehouse(self):
        """Display the warehouse grid."""
        print(self.warehouse.visualize())
        self.log("Viewed warehouse map")
