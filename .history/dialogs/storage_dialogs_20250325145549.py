import tkinter as tk
from tkinter import ttk, messagebox

class StoreProductDialog:
    """Dialog for storing a product in the warehouse (general operation)."""
    
    def __init__(self, parent, warehouse, refresh_callback):
        """Initialize the store product dialog."""
        self.parent = parent
        self.warehouse = warehouse
        self.refresh_callback = refresh_callback
        
        if not warehouse.products:
            messagebox.showinfo("No Products", "No products available to store. Please add products first.")
            return
            
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Store Product Operation")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the dialog widgets."""
        ttk.Label(self.dialog, text="Store Product in Warehouse", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Product selection
        ttk.Label(self.dialog, text="Select Product:").pack(anchor=tk.W, padx=20, pady=5)
        
        self.product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(self.dialog, textvariable=self.product_var, width=30)
        product_dropdown['values'] = [f"{p.name} ({p.sku}) - In Stock: {p.quantity}" 
                                      for p in self.warehouse.products.values()]
        product_dropdown.pack(padx=20, pady=5, fill=tk.X)
        
        # Quantity selection
        ttk.Label(self.dialog, text="Quantity:").pack(anchor=tk.W, padx=20, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(self.dialog, from_=1, to=1000, textvariable=self.quantity_var)
        quantity_entry.pack(padx=20, pady=5, fill=tk.X)
        
        # Location selection
        ttk.Label(self.dialog, text="Select Location:").pack(anchor=tk.W, padx=20, pady=5)
        location_frame = ttk.Frame(self.dialog)
        location_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(location_frame, text="Row:").pack(side=tk.LEFT)
        self.row_var = tk.StringVar()
        row_dropdown = ttk.Combobox(location_frame, textvariable=self.row_var, width=5)
        row_dropdown['values'] = [chr(65 + r) for r in range(self.warehouse.rows)]
        row_dropdown.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(location_frame, text="Column:").pack(side=tk.LEFT, padx=10)
        self.col_var = tk.StringVar()
        col_dropdown = ttk.Combobox(location_frame, textvariable=self.col_var, width=5)
        col_dropdown['values'] = [str(c+1) for c in range(self.warehouse.cols)]
        col_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, pady=20, padx=20)
        
        ttk.Button(btn_frame, text="Store", command=self.store_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def store_action(self):
        """Handle the store product action."""
        if not self.product_var.get():
            messagebox.showwarning("Input Error", "Please select a product.")
            return
            
        if not self.row_var.get() or not self.col_var.get():
            messagebox.showwarning("Input Error", "Please select a location.")
            return
            
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid quantity.")
            return
            
        # Extract SKU from dropdown selection
        sku = self.product_var.get().split("(")[1].split(")")[0]
        
        # Convert row letter to index (A=0, B=1, etc.)
        row = ord(self.row_var.get()) - 65
        # Convert column number to index (1=0, 2=1, etc.)
        col = int(self.col_var.get()) - 1
        
        if self.warehouse.store_product(sku, quantity, row, col):
            messagebox.showinfo("Success", f"Successfully stored {quantity} units at location {self.row_var.get()}{self.col_var.get()}")
            self.dialog.destroy()
            self.refresh_callback()
        else:
            messagebox.showerror("Error", "Failed to store product. Check product quantity and location capacity.")


class StoreLocationDialog:
    """Dialog for storing a product at a specific location."""
    
    def __init__(self, parent, warehouse, row, col, refresh_callback):
        """Initialize the store location dialog."""
        self.parent = parent
        self.warehouse = warehouse
        self.row = row
        self.col = col
        self.location = warehouse.grid[row][col]
        self.refresh_callback = refresh_callback
        
        if not warehouse.products:
            messagebox.showinfo("No Products", "No products available to store. Please add products first.")
            return
            
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Store Product")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the dialog widgets."""
        ttk.Label(self.dialog, text=f"Store Product at Location {self.location.get_location_code()}", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Product selection
        ttk.Label(self.dialog, text="Select Product:").pack(anchor=tk.W, padx=20, pady=5)
        
        self.product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(self.dialog, textvariable=self.product_var, width=30)
        product_dropdown['values'] = [f"{p.name} ({p.sku})" for p in self.warehouse.products.values()]
        product_dropdown.pack(padx=20, pady=5, fill=tk.X)
        
        # Quantity selection
        ttk.Label(self.dialog, text="Quantity:").pack(anchor=tk.W, padx=20, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(self.dialog, from_=1, to=1000, textvariable=self.quantity_var)
        quantity_entry.pack(padx=20, pady=5, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, pady=20, padx=20)
        
        ttk.Button(btn_frame, text="Store", command=self.store_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def store_action(self):
        """Handle the store product action."""
        if not self.product_var.get():
            messagebox.showwarning("Input Error", "Please select a product.")
            return
            
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid quantity.")
            return
            
        # Extract SKU from dropdown selection
        sku = self.product_var.get().split("(")[1].split(")")[0]
        
        if self.warehouse.store_product(sku, quantity, self.row, self.col):
            messagebox.showinfo("Success", f"Successfully stored {quantity} units at location {self.location.get_location_code()}")
            self.dialog.destroy()
            self.refresh_callback()
        else:
            messagebox.showerror("Error", "Failed to store product. Check product quantity and location capacity.")


class RetrieveProductDialog:
    """Dialog for retrieving a product from the warehouse (general operation)."""
    
    def __init__(self, parent, warehouse, refresh_callback):
        """Initialize the retrieve product dialog."""
        self.parent = parent
        self.warehouse = warehouse
        self.refresh_callback = refresh_callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Retrieve Product Operation")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the dialog widgets."""
        ttk.Label(self.dialog, text="Retrieve Product from Warehouse", font=("Arial", 12, "bold")).pack(pady=10)
        
        # First frame: select product
        product_frame = ttk.LabelFrame(self.dialog, text="Step 1: Select Product")
        product_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(product_frame, textvariable=self.product_var, width=30)
        product_dropdown['values'] = [f"{p.name} ({p.sku})" for p in self.warehouse.products.values()]
        product_dropdown.pack(padx=10, pady=10, fill=tk.X)
        
        # Second frame: will show locations after product selection
        location_frame = ttk.LabelFrame(self.dialog, text="Step 2: Select Location")
        location_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.location_list = tk.Listbox(location_frame, height=5)
        self.location_list.pack(padx=10, pady=10, fill=tk.X)
        
        # Update locations when product is selected
        def update_locations(*args):
            self.location_list.delete(0, tk.END)
            
            if not self.product_var.get():
                return
                
            sku = self.product_var.get().split("(")[1].split(")")[0]
            locations = self.warehouse.find_product(sku)
            
            if not locations:
                self.location_list.insert(tk.END, "Product not found in any location")
            else:
                for r, c in locations:
                    location = self.warehouse.grid[r][c]
                    self.location_list.insert(tk.END, 
                                        f"{location.get_location_code()} - {location.inventory[sku]} units")
        
        self.product_var.trace("w", update_locations)
        
        # Third frame: quantity selection
        quantity_frame = ttk.LabelFrame(self.dialog, text="Step 3: Enter Quantity")
        quantity_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(quantity_frame, from_=1, to=1000, textvariable=self.quantity_var)
        quantity_entry.pack(padx=10, pady=10, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, pady=20, padx=20)
        
        ttk.Button(btn_frame, text="Retrieve", command=self.retrieve_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def retrieve_action(self):
        """Handle the retrieve product action."""
        if not self.product_var.get():
            messagebox.showwarning("Input Error", "Please select a product.")
            return
            
        selected_location = self.location_list.curselection()
        if not selected_location:
            messagebox.showwarning("Input Error", "Please select a location.")
            return
            
        location_text = self.location_list.get(selected_location[0])
        if "not found" in location_text:
            messagebox.showwarning("Error", "Product not available at any location.")
            return
            
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid quantity.")
            return
            
        # Extract SKU from dropdown selection
        sku = self.product_var.get().split("(")[1].split(")")[0]
        
        # Extract location code from list selection
        location_code = location_text.split(" - ")[0]
        row = ord(location_code[0]) - 65
        col = int(location_code[1:]) - 1
        
        if self.warehouse.retrieve_product(sku, quantity, row, col):
            messagebox.showinfo("Success", f"Successfully retrieved {quantity} units from location {location_code}")
            self.dialog.destroy()
            self.refresh_callback()
        else:
            messagebox.showerror("Error", "Failed to retrieve product. Check quantity.")


class RetrieveLocationDialog:
    """Dialog for retrieving a product from a specific location."""
    
    def __init__(self, parent, warehouse, row, col, refresh_callback):
        """Initialize the retrieve location dialog."""
        self.parent = parent
        self.warehouse = warehouse
        self.row = row
        self.col = col
        self.location = warehouse.grid[row][col]
        self.refresh_callback = refresh_callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Retrieve Product")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the dialog widgets."""
        ttk.Label(self.dialog, text=f"Retrieve Product from Location {self.location.get_location_code()}", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Product selection
        ttk.Label(self.dialog, text="Select Product:").pack(anchor=tk.W, padx=20, pady=5)
        
        product_options = []
        for sku, qty in self.location.inventory.items():
            if sku in self.warehouse.products:
                product_name = self.warehouse.products[sku].name
                product_options.append(f"{product_name} ({sku}) - Available: {qty}")
        
        self.product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(self.dialog, textvariable=self.product_var, width=30)
        product_dropdown['values'] = product_options
        product_dropdown.pack(padx=20, pady=5, fill=tk.X)
        
        # Quantity selection
        ttk.Label(self.dialog, text="Quantity:").pack(anchor=tk.W, padx=20, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(self.dialog, from_=1, to=1000, textvariable=self.quantity_var)
        quantity_entry.pack(padx=20, pady=5, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, pady=20, padx=20)
        
        ttk.Button(btn_frame, text="Retrieve", command=self.retrieve_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def retrieve_action(self):
        """Handle the retrieve product action."""
        if not self.product_var.get():
            messagebox.showwarning("Input Error", "Please select a product.")
            return
            
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid quantity.")
            return
            
        # Extract SKU from dropdown selection
        selected = self.product_var.get()
        sku = selected.split("(")[1].split(")")[0]
        
        if self.warehouse.retrieve_product(sku, quantity, self.row, self.col):
            messagebox.showinfo("Success", f"Successfully retrieved {quantity} units from location {self.location.get_location_code()}")
            self.dialog.destroy()
            self.refresh_callback()
        else:
            messagebox.showerror("Error", "Failed to retrieve product. Check quantity.")
