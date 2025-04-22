import tkinter as tk
from tkinter import ttk

class ProductView:
    """View class for the products management tab."""
    
    def __init__(self, parent, warehouse, refresh_warehouse_callback):
        """Initialize the products view."""
        self.parent = parent
        self.warehouse = warehouse
        self.refresh_warehouse_callback = refresh_warehouse_callback
        self.setup_products_tab()
        
    def setup_products_tab(self):
        """Set up the products management tab."""
        # Main container with horizontal split
        self.main_container = ttk.PanedWindow(self.parent, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for product list
        self.left_panel = ttk.Frame(self.main_container)
        self.main_container.add(self.left_panel, weight=2)
        
        # Right panel for product details/edit/add forms
        self.right_panel = ttk.Frame(self.main_container)
        self.main_container.add(self.right_panel, weight=1)
        
        # Frame for controls in left panel
        control_frame = ttk.Frame(self.left_panel)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        ttk.Label(control_frame, text="Product Management", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Add New Product", 
                   command=self.show_add_product_form).pack(side=tk.RIGHT)
        
        # Frame for product list
        self.product_list_frame = ttk.Frame(self.left_panel)
        self.product_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tree view for products
        self.setup_product_treeview()
        
        # Initial state of right panel
        self.setup_right_panel()
    
    def setup_right_panel(self):
        """Set up the initial state of the right panel."""
        # Clear existing widgets
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        # Show welcome message
        ttk.Label(self.right_panel, text="Product Details", 
                 font=("Arial", 14, "bold")).pack(pady=20)
        ttk.Label(self.right_panel, 
                 text="Select a product from the list to view details\nor click 'Add New Product' to create one.").pack(pady=10)
    
    def setup_product_treeview(self):
        """Set up the treeview for product listing."""
        # Clear existing widgets
        for widget in self.product_list_frame.winfo_children():
            widget.destroy()
            
        # Create scrollbar
        scrollbar = ttk.Scrollbar(self.product_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        columns = ("name", "sku", "price", "quantity")
        self.product_tree = ttk.Treeview(self.product_list_frame, columns=columns, show="headings", 
                                          yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.product_tree.yview)
        
        # Define headings
        self.product_tree.heading("name", text="Product Name")
        self.product_tree.heading("sku", text="SKU")
        self.product_tree.heading("price", text="Price")
        self.product_tree.heading("quantity", text="Quantity")
        
        # Define columns
        self.product_tree.column("name", width=200)
        self.product_tree.column("sku", width=100)
        self.product_tree.column("price", width=100)
        self.product_tree.column("quantity", width=100)
        
        # Populate with products
        self.refresh_product_list()
        
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind click event to show product details
        self.product_tree.bind("<ButtonRelease-1>", self.show_product_details)
    
    def refresh_product_list(self):
        """Refresh the product list in the treeview."""
        # Clear existing items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
            
        # Add all products
        for product in self.warehouse.products.values():
            self.product_tree.insert("", tk.END, values=(
                product.name, 
                product.sku, 
                f"${product.price:.2f}", 
                product.quantity
            ))
    
    def show_message(self, message, is_error=False):
        """Show a message in the UI instead of a popup dialog."""
        # Create a transient message at the bottom of the right panel
        if hasattr(self, 'msg_frame') and self.msg_frame.winfo_exists():
            self.msg_frame.destroy()
            
        self.msg_frame = ttk.Frame(self.right_panel)
        self.msg_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        if is_error:
            bg_color = "#ffcccc"  # Light red for errors
        else:
            bg_color = "#ccffcc"  # Light green for success
            
        msg_label = ttk.Label(self.msg_frame, text=message, background=bg_color, padding=5)
        msg_label.pack(fill=tk.X)
        
        # Auto-remove the message after 3 seconds
        self.parent.after(3000, lambda: self.msg_frame.destroy() if hasattr(self, 'msg_frame') and self.msg_frame.winfo_exists() else None)
    
    def show_product_details(self, event):
        """Show details of the selected product."""
        # Get selected item
        selected_item = self.product_tree.focus()
        if not selected_item:
            return
            
        # Get item data
        item_data = self.product_tree.item(selected_item, "values")
        if not item_data:
            return
            
        sku = item_data[1]
        if sku not in self.warehouse.products:
            return
            
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        product = self.warehouse.products[sku]
        
        # Product header
        ttk.Label(self.right_panel, text=f"Product: {product.name}", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Product details
        details_frame = ttk.LabelFrame(self.right_panel, text="Details")
        details_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(details_frame, text=f"SKU: {product.sku}").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(details_frame, text=f"Price: ${product.price:.2f}").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(details_frame, text=f"Quantity: {product.quantity}").pack(anchor=tk.W, padx=10, pady=2)
        
        # Product locations
        locations = self.warehouse.find_product(sku)
        location_frame = ttk.LabelFrame(self.right_panel, text="Warehouse Locations")
        location_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        if locations:
            # Create scrollable list
            scrollbar = ttk.Scrollbar(location_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            location_list = tk.Listbox(location_frame, yscrollcommand=scrollbar.set)
            location_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=location_list.yview)
            
            # Add locations to list
            for r, c in locations:
                location = self.warehouse.grid[r][c]
                qty = location.inventory[sku]
                location_list.insert(tk.END, f"Location {location.get_location_code()}: {qty} units")
        else:
            ttk.Label(location_frame, text="This product is not stored in any warehouse location").pack(pady=20)
        
        # Action buttons
        action_frame = ttk.Frame(self.right_panel)
        action_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Button(action_frame, text="Edit Product", 
                  command=lambda: self.show_edit_product_form(sku)).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Back", 
                  command=self.setup_right_panel).pack(side=tk.RIGHT, padx=5)
    
    def show_add_product_form(self):
        """Show form to add a new product."""
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        # Form header
        ttk.Label(self.right_panel, text="Add New Product", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Create form
        form_frame = ttk.Frame(self.right_panel)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Product name
        ttk.Label(form_frame, text="Product Name:").pack(anchor=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, width=30).pack(pady=5, fill=tk.X)
        
        # SKU
        ttk.Label(form_frame, text="SKU:").pack(anchor=tk.W, pady=5)
        self.sku_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.sku_var, width=30).pack(pady=5, fill=tk.X)
        
        # Price
        ttk.Label(form_frame, text="Price:").pack(anchor=tk.W, pady=5)
        self.price_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.price_var, width=30).pack(pady=5, fill=tk.X)
        
        # Quantity
        ttk.Label(form_frame, text="Initial Quantity:").pack(anchor=tk.W, pady=5)
        self.quantity_var = tk.StringVar(value="0")
        ttk.Spinbox(form_frame, from_=0, to=10000, textvariable=self.quantity_var).pack(pady=5, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(self.right_panel)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Button(btn_frame, text="Add Product", command=self.add_product_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", 
                  command=self.setup_right_panel).pack(side=tk.RIGHT, padx=5)
    
    def add_product_action(self):
        """Handle the add product action."""
        from product import Product
        
        name = self.name_var.get().strip()
        sku = self.sku_var.get().strip()
        price_str = self.price_var.get().strip()
        quantity_str = self.quantity_var.get().strip()
        
        # Validate inputs
        if not name or not sku:
            self.show_message("Product name and SKU are required.", is_error=True)
            return
            
        if sku in self.warehouse.products:
            self.show_message("A product with this SKU already exists.", is_error=True)
            return
            
        try:
            price = float(price_str)
            if price < 0:
                raise ValueError("Price must be non-negative")
        except ValueError:
            self.show_message("Please enter a valid price.", is_error=True)
            return
            
        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError("Quantity must be non-negative")
        except ValueError:
            self.show_message("Please enter a valid quantity.", is_error=True)
            return
            
        # Create product and add to warehouse
        product = Product(name, sku, price, quantity)
        self.warehouse.add_product(product)
        
        self.show_message(f"Product '{name}' added successfully.")
        self.refresh_product_list()
        # Show the new product details
        self.show_product_details_by_sku(sku)
    
    def show_product_details_by_sku(self, sku):
        """Show product details by SKU."""
        if sku not in self.warehouse.products:
            return
            
        # Select the product in the treeview
        for item in self.product_tree.get_children():
            if self.product_tree.item(item, "values")[1] == sku:
                self.product_tree.selection_set(item)
                self.product_tree.focus(item)
                break
                
        # Show the details
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        product = self.warehouse.products[sku]
        
        # Product header
        ttk.Label(self.right_panel, text=f"Product: {product.name}", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Product details
        details_frame = ttk.LabelFrame(self.right_panel, text="Details")
        details_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(details_frame, text=f"SKU: {product.sku}").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(details_frame, text=f"Price: ${product.price:.2f}").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(details_frame, text=f"Quantity: {product.quantity}").pack(anchor=tk.W, padx=10, pady=2)
        
        # Product locations
        locations = self.warehouse.find_product(sku)
        location_frame = ttk.LabelFrame(self.right_panel, text="Warehouse Locations")
        location_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        if locations:
            # Create scrollable list
            scrollbar = ttk.Scrollbar(location_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            location_list = tk.Listbox(location_frame, yscrollcommand=scrollbar.set)
            location_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=location_list.yview)
            
            # Add locations to list
            for r, c in locations:
                location = self.warehouse.grid[r][c]
                qty = location.inventory[sku]
                location_list.insert(tk.END, f"Location {location.get_location_code()}: {qty} units")
        else:
            ttk.Label(location_frame, text="This product is not stored in any warehouse location").pack(pady=20)
        
        # Action buttons
        action_frame = ttk.Frame(self.right_panel)
        action_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Button(action_frame, text="Edit Product", 
                  command=lambda: self.show_edit_product_form(sku)).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Back", 
                  command=self.setup_right_panel).pack(side=tk.RIGHT, padx=5)
    
    def show_edit_product_form(self, sku):
        """Show form to edit an existing product."""
        if sku not in self.warehouse.products:
            return
            
        product = self.warehouse.products[sku]
        
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        # Form header
        ttk.Label(self.right_panel, text="Edit Product", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Create form
        form_frame = ttk.Frame(self.right_panel)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Product name
        ttk.Label(form_frame, text="Product Name:").pack(anchor=tk.W, pady=5)
        self.edit_name_var = tk.StringVar(value=product.name)
        ttk.Entry(form_frame, textvariable=self.edit_name_var, width=30).pack(pady=5, fill=tk.X)
        
        # SKU (read-only)
        ttk.Label(form_frame, text="SKU (read-only):").pack(anchor=tk.W, pady=5)
        self.edit_sku_var = tk.StringVar(value=product.sku)
        ttk.Entry(form_frame, textvariable=self.edit_sku_var, width=30, state="readonly").pack(pady=5, fill=tk.X)
        
        # Price
        ttk.Label(form_frame, text="Price:").pack(anchor=tk.W, pady=5)
        self.edit_price_var = tk.StringVar(value=str(product.price))
        ttk.Entry(form_frame, textvariable=self.edit_price_var, width=30).pack(pady=5, fill=tk.X)
        
        # Quantity
        ttk.Label(form_frame, text="Quantity:").pack(anchor=tk.W, pady=5)
        self.edit_quantity_var = tk.StringVar(value=str(product.quantity))
        ttk.Spinbox(form_frame, from_=0, to=10000, textvariable=self.edit_quantity_var).pack(pady=5, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(self.right_panel)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Button(btn_frame, text="Update", 
                  command=lambda: self.update_product_action(sku)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", 
                  command=lambda: self.show_product_details_by_sku(sku)).pack(side=tk.RIGHT, padx=5)
    
    def update_product_action(self, sku):
        """Handle the update product action."""
        if sku not in self.warehouse.products:
            return
            
        product = self.warehouse.products[sku]
        
        name = self.edit_name_var.get().strip()
        price_str = self.edit_price_var.get().strip()
        quantity_str = self.edit_quantity_var.get().strip()
        
        # Validate inputs
        if not name:
            self.show_message("Product name is required.", is_error=True)
            return
            
        try:
            price = float(price_str)
            if price < 0:
                raise ValueError("Price must be non-negative")
        except ValueError:
            self.show_message("Please enter a valid price.", is_error=True)
            return
            
        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError("Quantity must be non-negative")
        except ValueError:
            self.show_message("Please enter a valid quantity.", is_error=True)
            return
            
        # Update product
        product.name = name
        product.update_price(price)
        
        # Handle quantity change
        if quantity != product.quantity:
            delta = quantity - product.quantity
            product.update_quantity(delta)
        
        self.show_message("Product updated successfully.")
        self.refresh_product_list()
        self.show_product_details_by_sku(sku)
