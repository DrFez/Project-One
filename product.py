class Product:
    """
    Represents a product in the inventory management system.
    
    Attributes:
        name (str): The name of the product
        sku (str): Stock Keeping Unit - unique identifier for the product
        price (float): The price of the product
        quantity (int): The quantity of the product in stock
    """
    
    def __init__(self, name, sku, price, quantity=0, warehouse=None):
        """Initialize a new Product instance."""
        self.name = name
        self.sku = sku
        self.price = price
        self.quantity = quantity
        
    def update_quantity(self, amount):
        """
        Update the quantity of the product.
        
        Args:
            amount (int): The amount to add (positive) or remove (negative)
        
        Returns:
            bool: True if successful, False if would result in negative quantity
        """
        if self.quantity + amount < 0:
            return False
        self.quantity += amount
        return True
    
    def update_price(self, new_price):
        """Update the price of the product."""
        if new_price >= 0:
            self.price = new_price
            return True
        return False
        
    def __str__(self):
        """String representation of the product."""
        return f"{self.name} (SKU: {self.sku}) - ${self.price:.2f}, Qty: {self.quantity}"
