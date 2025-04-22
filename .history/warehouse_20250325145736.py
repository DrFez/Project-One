from location import Location
from data_storage import DataStorage

class Warehouse:
    """
    Represents the warehouse with a 2D grid of storage locations.
    
    Attributes:
        rows (int): Number of rows in the warehouse grid
        cols (int): Number of columns in the warehouse grid
        grid (list): 2D array of Location objects
        products (dict): Dictionary mapping SKUs to Product objects
    """
    
    def __init__(self, rows, cols):
        """Initialize a new Warehouse instance."""
        self.rows = rows
        self.cols = cols
        self.grid = []
        self.products = {}  # Maps SKU to Product object
        self.data_storage = DataStorage()
        
        # Initialize the 2D grid with Location objects
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(Location(r, c))
            self.grid.append(row)
    
    def add_product(self, product):
        """Register a new product in the warehouse."""
        if product.sku not in self.products:
            self.products[product.sku] = product
            return True
        return False
    
    def store_product(self, sku, quantity, row, col):
        """
        Store a product at a specific location.
        
        Args:
            sku (str): The SKU of the product
            quantity (int): The quantity to store
            row (int): The row coordinate
            col (int): The column coordinate
            
        Returns:
            bool: True if successful, False otherwise
        """
        if sku not in self.products:
            return False
            
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
            
        product = self.products[sku]
        location = self.grid[row][col]
        
        if not product.update_quantity(-quantity):
            return False
            
        if not location.add_product(product, quantity):
            # Rollback the product quantity change
            product.update_quantity(quantity)
            return False
            
        # Save the updated state
        self.save_data()
        return True
    
    def retrieve_product(self, sku, quantity, row, col):
        """
        Retrieve a product from a specific location.
        
        Args:
            sku (str): The SKU of the product
            quantity (int): The quantity to retrieve
            row (int): The row coordinate
            col (int): The column coordinate
            
        Returns:
            bool: True if successful, False otherwise
        """
        if sku not in self.products:
            return False
            
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
            
        product = self.products[sku]
        location = self.grid[row][col]
        
        if not location.remove_product(sku, quantity):
            return False
            
        product.update_quantity(quantity)
        
        # Save the updated state
        self.save_data()
        return True
    
    def find_product(self, sku):
        """
        Find all locations where a product is stored.
        
        Args:
            sku (str): The SKU of the product
            
        Returns:
            list: List of (row, col) tuples where the product is found
        """
        locations = []
        
        for r in range(self.rows):
            for c in range(self.cols):
                if sku in self.grid[r][c].inventory:
                    locations.append((r, c))
                    
        return locations
    
    def visualize(self):
        """
        Create a visual representation of the warehouse.
        
        Returns:
            str: A string visualization of the warehouse grid
        """
        result = "  " + " ".join(f"{i+1:2}" for i in range(self.cols)) + "\n"
        
        for r in range(self.rows):
            row_label = chr(65 + r)
            result += f"{row_label} "
            
            for c in range(self.cols):
                location = self.grid[r][c]
                if location.current_stock == 0:
                    result += "□  "
                elif location.current_stock < location.capacity // 2:
                    result += "▲  "
                elif location.current_stock < location.capacity:
                    result += "■  "
                else:
                    result += "▓  "
                    
            result += "\n"
            
        return result
    
    def save_data(self):
        """Save warehouse data to CSV files."""
        self.data_storage.save_products(self.products)
        self.data_storage.save_locations(self.grid)
    
    def load_data(self):
        """Load warehouse data from CSV files."""
        # Load products
        self.products = self.data_storage.load_products()
        
        # Load locations
        self.data_storage.load_locations(self.grid, self.products)
        
        return len(self.products) > 0
