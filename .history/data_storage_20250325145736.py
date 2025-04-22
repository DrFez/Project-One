import csv
import os
from product import Product

class DataStorage:
    """
    Handles data persistence for the warehouse inventory system using CSV files.
    Saves and loads product and location data.
    """
    
    def __init__(self, data_dir="data"):
        """Initialize with directory to store data files."""
        self.data_dir = data_dir
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        self.products_file = os.path.join(data_dir, "products.csv")
        self.locations_file = os.path.join(data_dir, "locations.csv")
    
    def save_products(self, products):
        """
        Save products dictionary to CSV.
        
        Args:
            products (dict): Dictionary of SKU to Product objects
        """
        with open(self.products_file, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['sku', 'name', 'price', 'quantity'])
            
            # Write product data
            for product in products.values():
                writer.writerow([
                    product.sku,
                    product.name,
                    product.price,
                    product.quantity
                ])
    
    def load_products(self):
        """
        Load products from CSV.
        
        Returns:
            dict: Dictionary of SKU to Product objects
        """
        products = {}
        
        # If file doesn't exist, return empty dictionary
        if not os.path.exists(self.products_file):
            return products
            
        with open(self.products_file, 'r', newline='') as file:
            reader = csv.reader(file)
            # Skip header
            next(reader, None)
            
            for row in reader:
                if len(row) >= 4:
                    sku = row[0]
                    name = row[1]
                    price = float(row[2])
                    quantity = int(row[3])
                    
                    # Create product and add to dictionary
                    product = Product(name, sku, price, quantity)
                    products[sku] = product
                    
        return products
    
    def save_locations(self, warehouse_grid):
        """
        Save location inventory to CSV.
        
        Args:
            warehouse_grid (list): 2D array of Location objects
        """
        with open(self.locations_file, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['row', 'col', 'sku', 'quantity'])
            
            # Loop through each location in the grid
            for r, row in enumerate(warehouse_grid):
                for c, location in enumerate(row):
                    # Write each product in the location's inventory
                    for sku, quantity in location.inventory.items():
                        writer.writerow([r, c, sku, quantity])
    
    def load_locations(self, warehouse_grid, products):
        """
        Load location inventory from CSV.
        
        Args:
            warehouse_grid (list): 2D array of Location objects
            products (dict): Dictionary of SKU to Product objects
            
        Returns:
            bool: True if successful, False otherwise
        """
        # If file doesn't exist, return False
        if not os.path.exists(self.locations_file):
            return False
            
        try:
            with open(self.locations_file, 'r', newline='') as file:
                reader = csv.reader(file)
                # Skip header
                next(reader, None)
                
                for row in reader:
                    if len(row) >= 4:
                        r = int(row[0])
                        c = int(row[1])
                        sku = row[2]
                        quantity = int(row[3])
                        
                        # Check if location exists in the grid
                        if (r < 0 or r >= len(warehouse_grid) or 
                            c < 0 or c >= len(warehouse_grid[0])):
                            continue
                            
                        # Check if product exists
                        if sku not in products:
                            continue
                            
                        # Add product to location
                        location = warehouse_grid[r][c]
                        product = products[sku]
                        location.add_product(product, quantity)
                        
            return True
        except Exception as e:
            print(f"Error loading locations: {e}")
            return False
