class Location:
    """
    Represents a storage location in the warehouse.
    
    Attributes:
        row (int): The row coordinate in the warehouse grid
        col (int): The column coordinate in the warehouse grid
        capacity (int): Maximum number of items this location can hold
        inventory (dict): Dictionary mapping product SKUs to quantities
    """
    
    def __init__(self, row, col, capacity=100):
        """Initialize a new Location instance."""
        self.row = row
        self.col = col
        self.capacity = capacity
        self.inventory = {}  # Maps SKU to quantity
        self.current_stock = 0
    
    def add_product(self, product, quantity):
        """
        Add a product to this location.
        
        Args:
            product: The product object to add
            quantity: The quantity to add
            
        Returns:
            bool: True if successful, False if would exceed capacity
        """
        if self.current_stock + quantity > self.capacity:
            return False
            
        if product.sku in self.inventory:
            self.inventory[product.sku] += quantity
        else:
            self.inventory[product.sku] = quantity
            
        self.current_stock += quantity
        return True
    
    def remove_product(self, product_sku, quantity):
        """
        Remove a product from this location.
        
        Args:
            product_sku: The SKU of the product to remove
            quantity: The quantity to remove
            
        Returns:
            bool: True if successful, False if not enough stock
        """
        if product_sku not in self.inventory or self.inventory[product_sku] < quantity:
            return False
            
        self.inventory[product_sku] -= quantity
        self.current_stock -= quantity
        
        if self.inventory[product_sku] == 0:
            del self.inventory[product_sku]
            
        return True
    
    def get_available_capacity(self):
        """Return the remaining capacity at this location."""
        return self.capacity - self.current_stock
    
    def get_location_code(self):
        """Return a string code representing this location."""
        return f"{chr(65 + self.row)}{self.col + 1}"
    
    def __str__(self):
        """String representation of the location."""
        return f"Location {self.get_location_code()} - {self.current_stock}/{self.capacity} items"
