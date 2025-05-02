import csv
import os
import threading
import json
import time
from product import Product
from utils.debug_utils import DebugPrint  # <— added

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
            DebugPrint.database(f"Creating data directory: {data_dir}")  # <— debug
            os.makedirs(data_dir)
            
        self.products_file = os.path.join(data_dir, "products.csv")
        self.locations_file = os.path.join(data_dir, "locations.csv")
        self.settings_file = os.path.join(data_dir, "settings.json")
        self.logs_file = os.path.join(data_dir, "logs.csv")
        
        # For thread safety
        self.lock = threading.Lock()
    
    def save_products(self, products):
        """
        Save products dictionary to CSV.
        
        Args:
            products (dict): Dictionary of SKU to Product objects
        """
        DebugPrint.database(f"Starting thread to save {len(products)} products")  # <— debug
        # Use a separate thread for file operations to avoid blocking the UI
        threading.Thread(target=self._save_products_thread, args=(products,)).start()
    
    def _save_products_thread(self, products):
        """Thread function to save products without blocking."""
        with self.lock:
            try:
                DebugPrint.database(f"Saving {len(products)} products to {self.products_file}")  # <— debug
                # Create a temporary file first to avoid data corruption if interrupted
                temp_file = self.products_file + ".tmp"
                
                with open(temp_file, 'w', newline='') as file:
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
                
                # Replace the original file with the temp file
                if os.path.exists(self.products_file):
                    os.remove(self.products_file)
                os.rename(temp_file, self.products_file)
                DebugPrint.success("Products saved successfully")  # <— debug
            except Exception as e:
                DebugPrint.error(f"Error saving products: {e}")  # <— debug
    
    def load_products(self):
        """
        Load products from CSV.
        
        Returns:
            dict: Dictionary of SKU to Product objects
        """
        DebugPrint.database("Loading products from CSV")  # <— debug
        products = {}
        
        # If file doesn't exist, return empty dictionary
        if not os.path.exists(self.products_file):
            return products
        
        with self.lock:    
            try:
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
                DebugPrint.success(f"Loaded {len(products)} products")  # <— debug
            except Exception as e:
                DebugPrint.error(f"Error loading products: {e}")  # <— debug
                    
        return products
    
    def save_locations(self, warehouse_grid):
        """
        Save location inventory to CSV.
        
        Args:
            warehouse_grid (list): 2D array of Location objects
        """
        DebugPrint.database("Starting thread to save locations")  # <— debug
        # Use a separate thread for file operations to avoid blocking the UI
        threading.Thread(target=self._save_locations_thread, args=(warehouse_grid,)).start()
    
    def _save_locations_thread(self, warehouse_grid):
        """Thread function to save locations without blocking."""
        with self.lock:
            try:
                DebugPrint.database(f"Saving locations to {self.locations_file}")  # <— debug
                # Create a temporary file first to avoid data corruption if interrupted
                temp_file = self.locations_file + ".tmp"
                
                with open(temp_file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    # Write header
                    writer.writerow(['row', 'col', 'sku', 'quantity'])
                    
                    # Loop through each location in the grid
                    for r, row in enumerate(warehouse_grid):
                        for c, location in enumerate(row):
                            # Write each product in the location's inventory
                            for sku, quantity in location.inventory.items():
                                writer.writerow([r, c, sku, quantity])
                
                # Replace the original file with the temp file
                if os.path.exists(self.locations_file):
                    os.remove(self.locations_file)
                os.rename(temp_file, self.locations_file)
                DebugPrint.success("Locations saved successfully")  # <— debug
            except Exception as e:
                DebugPrint.error(f"Error saving locations: {e}")  # <— debug
    
    def load_locations(self, warehouse_grid, products):
        """
        Load location inventory from CSV.
        
        Args:
            warehouse_grid (list): 2D array of Location objects
            products (dict): Dictionary of SKU to Product objects
            
        Returns:
            bool: True if successful, False otherwise
        """
        DebugPrint.database("Loading locations from CSV")  # <— debug
        # If file doesn't exist, return False
        if not os.path.exists(self.locations_file):
            return False
        
        with self.lock:    
            try:
                with open(self.locations_file, 'r', newline='') as file:
                    reader = csv.reader(file)
                    # Skip header
                    next(reader, None)
                    
                    # Group locations by position for batch processing
                    location_data = {}
                    for row in reader:
                        if len(row) >= 4:
                            r = int(row[0])
                            c = int(row[1])
                            sku = row[2]
                            quantity = int(row[3])
                            
                            # Skip invalid locations and products
                            if (r < 0 or r >= len(warehouse_grid) or 
                                c < 0 or c >= len(warehouse_grid[0]) or
                                sku not in products):
                                continue
                                
                            # Group by location for more efficient processing
                            loc_key = (r, c)
                            if loc_key not in location_data:
                                location_data[loc_key] = []
                            location_data[loc_key].append((sku, quantity))
                    
                    # Process locations in batches
                    for (r, c), items in location_data.items():
                        location = warehouse_grid[r][c]
                        for sku, quantity in items:
                            product = products[sku]
                            location.add_product(product, quantity)
                            
                DebugPrint.success("Locations loaded successfully")  # <— debug
                return True
            except Exception as e:
                DebugPrint.error(f"Error loading locations: {e}")  # <— debug
                return False
    
    def save_settings(self, settings):
        """
        Save application settings to JSON file.
        
        Args:
            settings (dict): Dictionary of application settings
        """
        DebugPrint.database("Saving settings to JSON")  # <— debug
        try:
            with self.lock:
                # Create a temporary file first to avoid data corruption
                temp_file = self.settings_file + ".tmp"
                
                with open(temp_file, 'w') as file:
                    json.dump(settings, file, indent=4)
                
                # Replace the original file with the temp file
                if os.path.exists(self.settings_file):
                    os.remove(self.settings_file)
                os.rename(temp_file, self.settings_file)
                
            DebugPrint.success("Settings saved")  # <— debug
            return True
        except Exception as e:
            DebugPrint.error(f"Error saving settings: {e}")  # <— debug
            return False
    
    def load_settings(self):
        """
        Load application settings from JSON file.
        
        Returns:
            dict: Dictionary of application settings, or default settings if file doesn't exist
        """
        DebugPrint.database("Loading settings from JSON")  # <— debug
        default_settings = {
            "warehouse_rows": 5,
            "warehouse_cols": 8,
            "first_run": True
        }
        
        if not os.path.exists(self.settings_file):
            return default_settings
        
        try:
            with self.lock:
                with open(self.settings_file, 'r') as file:
                    settings = json.load(file)
                    
                DebugPrint.success("Settings loaded")  # <— debug
                # Ensure all required settings exist
                for key, value in default_settings.items():
                    if key not in settings:
                        settings[key] = value
                        
                return settings
        except Exception as e:
            DebugPrint.error(f"Error loading settings: {e}")  # <— debug
            return default_settings
    
    def save_log(self, user, action):
        """Append a timestamped log entry (user, action) to logs_file."""
        DebugPrint.database(f"Logging action: {user} - {action}")  # <— debug
        threading.Thread(target=self._save_log_thread, args=(user, action)).start()

    def _save_log_thread(self, user, action):
        with self.lock:
            header = not os.path.exists(self.logs_file)
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # Append file
            with open(self.logs_file, "a", newline="") as f:
                writer = csv.writer(f)
                if header:
                    writer.writerow(["timestamp", "user", "action"])
                writer.writerow([ts, user, action])

    def load_logs(self):
        """Return list of (timestamp, user, action) from logs_file."""
        DebugPrint.database("Loading logs from CSV")  # <— debug
        if not os.path.exists(self.logs_file):
            return []
        with self.lock:
            with open(self.logs_file, "r", newline="") as f:
                reader = csv.reader(f)
                rows = list(reader)
        DebugPrint.success(f"Loaded {len(rows) - 1} log entries")  # <— debug
        # skip header
        return rows[1:] if len(rows) > 1 else []
