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
        self.changes_since_save = 0  # Track changes to avoid excessive saves
        self.save_threshold = 5  # Save after this many changes
        
        # Initialize the 2D grid with Location objects
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(Location(r, c))
            self.grid.append(row)
        
        # Location lookup cache for faster product searches
        self.product_locations = {}  # Maps SKU to list of (row, col) tuples
    
    def add_product(self, product):
        """Register a new product in the warehouse."""
        if product.sku not in self.products:
            self.products[product.sku] = product
            self.product_locations[product.sku] = []
            self.distribute_initial_quantity(product)
            self._increment_changes()
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
        
        if not location.add_product(product, quantity):
            return False
        
        # Update product's total quantity
        product.update_quantity(quantity)
        
        # Update location cache
        if (row, col) not in self.product_locations.get(sku, []):
            self.product_locations.setdefault(sku, []).append((row, col))
        
        # Save data immediately
        self.data_storage.save_products(self.products)
        self.data_storage.save_locations(self.grid)
        
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
        
        # Check if the quantity being removed will empty this location for this product
        will_be_empty = location.inventory.get(sku, 0) <= quantity
        
        if not location.remove_product(sku, quantity):
            return False
            
        # Update product's total quantity
        product.update_quantity(-quantity)
        
        # Remove location from cache if it becomes empty
        if will_be_empty:
            self.product_locations[sku].remove((row, col))
            if not self.product_locations[sku]:
                del self.product_locations[sku]
        
        # Save data immediately
        self.data_storage.save_products(self.products)
        self.data_storage.save_locations(self.grid)
        
        return True
    
    def find_product(self, sku):
        """
        Find all locations where a product is stored.
        
        Args:
            sku (str): The SKU of the product
            
        Returns:
            list: List of (row, col) tuples where the product is found
        """
        # Use the cached location data instead of searching the entire grid
        if sku in self.product_locations:
            return self.product_locations[sku].copy()
        
        # Fall back to grid search if cache is empty (should not normally happen)
        locations = []
        for r in range(self.rows):
            for c in range(self.cols):
                if sku in self.grid[r][c].inventory:
                    locations.append((r, c))
        
        # Update cache with found locations
        self.product_locations[sku] = locations.copy()
        return locations
    
    def visualize(self):
        """
        Create a visual representation of the warehouse.
        
        Returns:
            str: A string visualization of the warehouse grid
        """
        result = "   " + " ".join(f"{i+1:2}" for i in range(self.cols)) + "\n"
        
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

    def reset_warehouse(self):
        """Reset the warehouse to its initial state."""
        self.__init__(self.rows, self.cols)
        self.save_data(force=True)
    
    def save_data(self, force=False):
        """
        Save warehouse data to CSV files.
        
        Args:
            force (bool): If True, save regardless of number of changes
        """
        if force or self.changes_since_save >= self.save_threshold:
            self.data_storage.save_products(self.products)
            self.data_storage.save_locations(self.grid)
            self.changes_since_save = 0
    
    def load_data(self):
        """Load warehouse data from CSV files."""
        # Load products
        self.products = self.data_storage.load_products()
        
        # Initialize product locations cache
        self.product_locations = {sku: [] for sku in self.products}
        
        # Load locations
        success = self.data_storage.load_locations(self.grid, self.products)
        
        # Build location cache
        if success:
            self._rebuild_location_cache()
        
        return len(self.products) > 0
    
    def _rebuild_location_cache(self):
        """Rebuild the product locations cache from current warehouse state."""
        self.product_locations = {sku: [] for sku in self.products}
        
        for r in range(self.rows):
            for c in range(self.cols):
                location = self.grid[r][c]
                for sku in location.inventory:
                    if sku in self.product_locations:
                        self.product_locations[sku].append((r, c))
    
    def _increment_changes(self):
        """Increment change counter and save if threshold reached."""
        self.changes_since_save += 1
        if self.changes_since_save >= self.save_threshold:
            self.save_data()

    def validate_quantities(self):
        """
        Validate that the total quantity of each product matches the quantity stored in the warehouse.
        
        Returns:
            list: List of SKUs with mismatched quantities.
        """
        mismatched_skus = []
        for sku, product in self.products.items():
            total_in_warehouse = sum(
                location.inventory.get(sku, 0) for row in self.grid for location in row
            )
            if total_in_warehouse != product.quantity:
                mismatched_skus.append(sku)
        return mismatched_skus

    def distribute_initial_quantity(self, product):
        """
        Distribute the initial quantity of a product across available locations.
        
        Args:
            product (Product): The product to distribute.
        """
        quantity_to_distribute = product.quantity
        for row in self.grid:
            for location in row:
                if quantity_to_distribute <= 0:
                    return
                available_space = location.get_available_capacity()
                if available_space > 0:
                    quantity_to_store = min(quantity_to_distribute, available_space)
                    location.add_product(product, quantity_to_store)
                    quantity_to_distribute -= quantity_to_store
        if quantity_to_distribute > 0:
            print(f"Warning: Not enough space to store the full quantity of {product.sku}. Remaining: {quantity_to_distribute}")
