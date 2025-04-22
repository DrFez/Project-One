import tkinter as tk
from tkinter import ttk, messagebox
from product import Product

class AddProductDialog:
    """Dialog for adding a new product."""
    
    def __init__(self, parent, warehouse, refresh_callback):
        """Initialize the add product dialog."""
        self.parent = parent
        self.warehouse = warehouse
        self.refresh_callback = refresh_callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Product")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the dialog widgets."""
        ttk.Label(self.dialog, text="Add New Product", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Product name
        ttk.Label(self.dialog, text="Product Name:").pack(anchor=tk.W, padx=20, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.name_var, width=30).pack(padx=20, pady=5, fill=tk.X)
        
        # SKU
        ttk.Label(self.dialog, text="SKU:").pack(anchor=tk.W, padx=20, pady=5)
        self.sku_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.sku_var, width=30).pack(padx=20, pady=5, fill=tk.X)
        
        # Price
        ttk.Label(self.dialog, text="Price:").pack(anchor=tk.W, padx=20, pady=5)
        self.price_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.price_var, width=30).pack(padx=20, pady=5, fill=tk.X)
        
        # Quantity
        ttk.Label(self.dialog, text="Initial Quantity:").pack(anchor=tk.W, padx=20, pady=5)
        self.quantity_var = tk.StringVar(value="0")
        ttk.Spinbox(self.dialog, from_=0, to=10000, textvariable=self.quantity_var).pack(padx=20, pady=5, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, pady=20, padx=20)
        
        ttk.Button(btn_frame, text="Add Product", command=self.add_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def add_action(self):
        """Handle the add product action."""
        name = self.name_var.get().strip()
        sku = self.sku_var.get().strip()
        price_str = self.price_var.get().strip()
        quantity_str = self.quantity_var.get().strip()
        
        # Validate inputs
        if not name or not sku:
            messagebox.showwarning("Input Error", "Product name and SKU are required.")
            return
            
        if sku in self.warehouse.products:
            messagebox.showwarning("Duplicate SKU", "A product with this SKU already exists.")
            return
            
        try:
            price = float(price_str)
            if price < 0:
                raise ValueError("Price must be non-negative")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid price.")
            return
            
        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError("Quantity must be non-negative")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid quantity.")
            return
            
        # Create product and add to warehouse
        product = Product(name, sku, price, quantity)
        self.warehouse.add_product(product)
        
        messagebox.showinfo("Success", f"Product '{name}' added successfully.")
        self.dialog.destroy()
        self.refresh_callback()


class EditProductDialog:
    """Dialog for editing an existing product."""
    
    def __init__(self, parent, warehouse, sku, refresh_callback):
        """Initialize the edit product dialog."""
        self.parent = parent
        self.warehouse = warehouse
        self.sku = sku
        self.product = warehouse.products[sku]
        self.refresh_callback = refresh_callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Product")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the dialog widgets."""
        ttk.Label(self.dialog, text="Edit Product", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Product name
        ttk.Label(self.dialog, text="Product Name:").pack(anchor=tk.W, padx=20, pady=5)
        self.name_var = tk.StringVar(value=self.product.name)
        ttk.Entry(self.dialog, textvariable=self.name_var, width=30).pack(padx=20, pady=5, fill=tk.X)
        
        # SKU (read-only)
        ttk.Label(self.dialog, text="SKU (read-only):").pack(anchor=tk.W, padx=20, pady=5)
        self.sku_var = tk.StringVar(value=self.product.sku)
        ttk.Entry(self.dialog, textvariable=self.sku_var, width=30, state="readonly").pack(padx=20, pady=5, fill=tk.X)
        
        # Price
        ttk.Label(self.dialog, text="Price:").pack(anchor=tk.W, padx=20, pady=5)
        self.price_var = tk.StringVar(value=str(self.product.price))
        ttk.Entry(self.dialog, textvariable=self.price_var, width=30).pack(padx=20, pady=5, fill=tk.X)
        
        # Quantity
        ttk.Label(self.dialog, text="Quantity:").pack(anchor=tk.W, padx=20, pady=5)
        self.quantity_var = tk.StringVar(value=str(self.product.quantity))
        ttk.Spinbox(self.dialog, from_=0, to=10000, textvariable=self.quantity_var).pack(padx=20, pady=5, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, pady=20, padx=20)
        
        ttk.Button(btn_frame, text="Update", command=self.update_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def update_action(self):
        """Handle the update product action."""
        name = self.name_var.get().strip()
        price_str = self.price_var.get().strip()
        quantity_str = self.quantity_var.get().strip()
        
        # Validate inputs
        if not name:
            messagebox.showwarning("Input Error", "Product name is required.")
            return
            
        try:
            price = float(price_str)
            if price < 0:
                raise ValueError("Price must be non-negative")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid price.")
            return
            
        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError("Quantity must be non-negative")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid quantity.")
            return
            
        # Update product
        self.product.name = name
        self.product.update_price(price)
        
        # Handle quantity change
        if quantity != self.product.quantity:
            delta = quantity - self.product.quantity
            self.product.update_quantity(delta)
        
        messagebox.showinfo("Success", "Product updated successfully.")
        self.dialog.destroy()
        self.refresh_callback()
