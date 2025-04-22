import tkinter as tk
from tkinter import ttk

class StorageView:
    """View class for the storage operations tab."""
    
    def __init__(self, parent, warehouse, refresh_warehouse_callback, refresh_product_callback):
        """Initialize the storage view."""
        self.parent = parent
        self.warehouse = warehouse
        self.refresh_warehouse_callback = refresh_warehouse_callback
        self.refresh_product_callback = refresh_product_callback
        self.setup_storage_tab()
        
    def setup_storage_tab(self):
        """Set up the storage operations tab."""
        # Main container with horizontal split
        self.main_container = ttk.PanedWindow(self.parent, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for operations and mini-map
        self.left_panel = ttk.Frame(self.main_container)
        self.main_container.add(self.left_panel, weight=1)
        
        # Right panel for forms and results
        self.right_panel = ttk.Frame(self.main_container)
        self.main_container.add(self.right_panel, weight=2)
        
        # Operations frame (left top)
        operations_frame = ttk.LabelFrame(self.left_panel, text="Operations")
        operations_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, expand=False)
        
        # Add operation buttons
        ttk.Button(operations_frame, text="Store Product", 
                   command=self.show_store_product_form, width=20).pack(pady=5, padx=10)
        ttk.Button(operations_frame, text="Retrieve Product", 
                   command=self.show_retrieve_product_form, width=20).pack(pady=5, padx=10)
        ttk.Button(operations_frame, text="Search Product", 
                   command=self.show_search_product_form, width=20).pack(pady=5, padx=10)
        ttk.Button(operations_frame, text="View Location", 
                   command=self.show_view_location_form, width=20).pack(pady=5, padx=10)
        
        # Mini-map frame (left bottom)
        map_frame = ttk.LabelFrame(self.left_panel, text="Warehouse Map")
        map_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=5, pady=5, expand=True)
        
        self.mini_map_frame = ttk.Frame(map_frame)
        self.mini_map_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Draw mini map
        self.draw_mini_map()
        
        # Initial state of right panel
        self.setup_right_panel()
    
    def setup_right_panel(self):
        """Set up the initial state of the right panel."""
        # Clear existing widgets
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        # Show welcome message
        ttk.Label(self.right_panel, text="Warehouse Operations", 
                 font=("Arial", 16, "bold")).pack(pady=20)
        ttk.Label(self.right_panel, 
                 text="Select an operation from the left panel or click on a location in the map.").pack(pady=10)
        
    def draw_mini_map(self):
        """Draw a smaller version of the warehouse map for the storage tab."""
        # Clear existing widgets
        for widget in self.mini_map_frame.winfo_children():
            widget.destroy()
            
        # Create a canvas for the mini-map
        canvas_width = 300
        canvas_height = 200
        
        canvas = tk.Canvas(self.mini_map_frame, width=canvas_width, height=canvas_height, bg="white")
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Calculate cell size
        cell_width = canvas_width / (self.warehouse.cols + 1)
        cell_height = canvas_height / (self.warehouse.rows + 1)
        
        # Draw column labels
        for c in range(self.warehouse.cols):
            canvas.create_text((c+1) * cell_width + cell_width/2, cell_height/2, 
                              text=str(c+1), font=("Arial", 8, "bold"))
            
        # Draw row labels and cells
        for r in range(self.warehouse.rows):
            row_label = chr(65 + r)
            canvas.create_text(cell_width/2, (r+1) * cell_height + cell_height/2, 
                              text=row_label, font=("Arial", 8, "bold"))
            
            for c in range(self.warehouse.cols):
                location = self.warehouse.grid[r][c]
                
                # Determine color based on fill level
                if location.current_stock == 0:
                    fill_color = "white"  # Empty
                elif location.current_stock < location.capacity // 2:
                    fill_color = "light green"  # Less than 50%
                elif location.current_stock < location.capacity:
                    fill_color = "sky blue"  # Less than 100%
                else:
                    fill_color = "orange red"  # Full
                
                # Draw cell
                x1 = (c+1) * cell_width
                y1 = (r+1) * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                
                cell_id = canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")
                
                # Make cells clickable
                canvas.tag_bind(cell_id, "<Button-1>", 
                               lambda event, row=r, col=c: self.show_location_details(row, col))
    
    def refresh_callback(self):
        """Callback function to refresh all views."""
        self.refresh_warehouse_callback()
        self.draw_mini_map()
        self.refresh_product_callback()
    
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
    
    def show_location_details(self, row, col):
        """Show location details in the right panel."""
        # Clear existing widgets
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        location = self.warehouse.grid[row][col]
        
        # Location header
        ttk.Label(self.right_panel, text=f"Location {location.get_location_code()}", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Location details
        details_frame = ttk.LabelFrame(self.right_panel, text="Details")
        details_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(details_frame, text=f"Capacity: {location.capacity} units").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(details_frame, text=f"Current Stock: {location.current_stock} units").pack(anchor=tk.W, padx=10, pady=2)
        ttk.Label(details_frame, text=f"Available Space: {location.get_available_capacity()} units").pack(anchor=tk.W, padx=10, pady=2)
        
        # Product list
        product_frame = ttk.LabelFrame(self.right_panel, text="Products")
        product_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        if location.inventory:
            # Create scrollable list
            scrollbar = ttk.Scrollbar(product_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            product_list = tk.Listbox(product_frame, yscrollcommand=scrollbar.set)
            product_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=product_list.yview)
            
            # Add products to list
            for sku, qty in location.inventory.items():
                if sku in self.warehouse.products:
                    product_name = self.warehouse.products[sku].name
                    product_list.insert(tk.END, f"{product_name} ({sku}): {qty}")
        else:
            ttk.Label(product_frame, text="This location is empty").pack(pady=20)
        
        # Action buttons
        action_frame = ttk.Frame(self.right_panel)
        action_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Button(action_frame, text="Store Product", 
                  command=lambda: self.show_store_location_form(row, col)).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Retrieve Product", 
                  command=lambda: self.show_retrieve_location_form(row, col)).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Back", 
                  command=self.setup_right_panel).pack(side=tk.RIGHT, padx=5)
    
    def show_store_product_form(self):
        """Show form to store a product in the warehouse (general operation)."""
        # Clear existing widgets
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        if not self.warehouse.products:
            ttk.Label(self.right_panel, text="No Products Available", 
                     font=("Arial", 14, "bold")).pack(pady=10)
            ttk.Label(self.right_panel, text="Please add products first.").pack(pady=10)
            ttk.Button(self.right_panel, text="Back", 
                      command=self.setup_right_panel).pack(pady=10)
            return
            
        # Form header
        ttk.Label(self.right_panel, text="Store Product in Warehouse", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Create form
        form_frame = ttk.Frame(self.right_panel)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Product selection
        ttk.Label(form_frame, text="Select Product:").pack(anchor=tk.W, pady=5)
        
        self.product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(form_frame, textvariable=self.product_var, width=30)
        product_dropdown['values'] = [f"{p.name} ({p.sku}) - In Stock: {p.quantity}" 
                                      for p in self.warehouse.products.values()]
        product_dropdown.pack(pady=5, fill=tk.X)
        
        # Quantity selection
        ttk.Label(form_frame, text="Quantity:").pack(anchor=tk.W, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(form_frame, from_=1, to=1000, textvariable=self.quantity_var)
        quantity_entry.pack(pady=5, fill=tk.X)
        
        # Location selection
        ttk.Label(form_frame, text="Select Location:").pack(anchor=tk.W, pady=5)
        location_frame = ttk.Frame(form_frame)
        location_frame.pack(fill=tk.X, pady=5)
        
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
        btn_frame = ttk.Frame(self.right_panel)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Button(btn_frame, text="Store", command=self.store_product_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", 
                  command=self.setup_right_panel).pack(side=tk.RIGHT, padx=5)
    
    def store_product_action(self):
        """Handle the store product action."""
        if not self.product_var.get():
            self.show_message("Please select a product.", is_error=True)
            return
            
        if not self.row_var.get() or not self.col_var.get():
            self.show_message("Please select a location.", is_error=True)
            return
            
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            self.show_message("Please enter a valid quantity.", is_error=True)
            return
            
        # Extract SKU from dropdown selection
        sku = self.product_var.get().split("(")[1].split(")")[0]
        
        # Convert row letter to index (A=0, B=1, etc.)
        row = ord(self.row_var.get()) - 65
        # Convert column number to index (1=0, 2=1, etc.)
        col = int(self.col_var.get()) - 1
        
        if self.warehouse.store_product(sku, quantity, row, col):
            self.show_message(f"Successfully stored {quantity} units at location {self.row_var.get()}{self.col_var.get()}")
            self.refresh_callback()
            # Show the location details after storing
            self.show_location_details(row, col)
        else:
            self.show_message("Failed to store product. Check product quantity and location capacity.", is_error=True)
    
    def show_store_location_form(self, row, col):
        """Show form to store a product at a specific location."""
        # Clear existing widgets
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        location = self.warehouse.grid[row][col]
        
        if not self.warehouse.products:
            ttk.Label(self.right_panel, text="No Products Available", 
                     font=("Arial", 14, "bold")).pack(pady=10)
            ttk.Label(self.right_panel, text="Please add products first.").pack(pady=10)
            ttk.Button(self.right_panel, text="Back", 
                      command=lambda: self.show_location_details(row, col)).pack(pady=10)
            return
            
        # Form header
        ttk.Label(self.right_panel, text=f"Store Product at {location.get_location_code()}", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Create form
        form_frame = ttk.Frame(self.right_panel)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Product selection
        ttk.Label(form_frame, text="Select Product:").pack(anchor=tk.W, pady=5)
        
        self.product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(form_frame, textvariable=self.product_var, width=30)
        product_dropdown['values'] = [f"{p.name} ({p.sku})" for p in self.warehouse.products.values()]
        product_dropdown.pack(pady=5, fill=tk.X)
        
        # Quantity selection
        ttk.Label(form_frame, text="Quantity:").pack(anchor=tk.W, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(form_frame, from_=1, to=1000, textvariable=self.quantity_var)
        quantity_entry.pack(pady=5, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(self.right_panel)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)
        
        def store_action():
            if not self.product_var.get():
                self.show_message("Please select a product.", is_error=True)
                return
                
            try:
                quantity = int(self.quantity_var.get())
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
            except ValueError:
                self.show_message("Please enter a valid quantity.", is_error=True)
                return
                
            # Extract SKU from dropdown selection
            sku = self.product_var.get().split("(")[1].split(")")[0]
            
            if self.warehouse.store_product(sku, quantity, row, col):
                self.show_message(f"Successfully stored {quantity} units at location {location.get_location_code()}")
                self.refresh_callback()
                self.show_location_details(row, col)
            else:
                self.show_message("Failed to store product. Check product quantity and location capacity.", is_error=True)
        
        ttk.Button(btn_frame, text="Store", command=store_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", 
                  command=lambda: self.show_location_details(row, col)).pack(side=tk.RIGHT, padx=5)
    
    def show_retrieve_product_form(self):
        """Show form to retrieve a product from the warehouse (general operation)."""
        # Clear existing widgets
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        # Form header
        ttk.Label(self.right_panel, text="Retrieve Product from Warehouse", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Create form
        form_frame = ttk.Frame(self.right_panel)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # First frame: select product
        product_frame = ttk.LabelFrame(form_frame, text="Step 1: Select Product")
        product_frame.pack(fill=tk.X, pady=10)
        
        self.product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(product_frame, textvariable=self.product_var, width=30)
        product_dropdown['values'] = [f"{p.name} ({p.sku})" for p in self.warehouse.products.values()]
        product_dropdown.pack(padx=10, pady=10, fill=tk.X)
        
        # Second frame: will show locations after product selection
        location_frame = ttk.LabelFrame(form_frame, text="Step 2: Select Location")
        location_frame.pack(fill=tk.X, pady=10)
        
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
        quantity_frame = ttk.LabelFrame(form_frame, text="Step 3: Enter Quantity")
        quantity_frame.pack(fill=tk.X, pady=10)
        
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(quantity_frame, from_=1, to=1000, textvariable=self.quantity_var)
        quantity_entry.pack(padx=10, pady=10, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(self.right_panel)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Button(btn_frame, text="Retrieve", command=self.retrieve_product_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", 
                  command=self.setup_right_panel).pack(side=tk.RIGHT, padx=5)
    
    def retrieve_product_action(self):
        """Handle the retrieve product action."""
        if not self.product_var.get():
            self.show_message("Please select a product.", is_error=True)
            return
            
        selected_location = self.location_list.curselection()
        if not selected_location:
            self.show_message("Please select a location.", is_error=True)
            return
            
        location_text = self.location_list.get(selected_location[0])
        if "not found" in location_text:
            self.show_message("Product not available at any location.", is_error=True)
            return
            
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            self.show_message("Please enter a valid quantity.", is_error=True)
            return
            
        # Extract SKU from dropdown selection
        sku = self.product_var.get().split("(")[1].split(")")[0]
        
        # Extract location code from list selection
        location_code = location_text.split(" - ")[0]
        row = ord(location_code[0]) - 65
        col = int(location_code[1:]) - 1
        
        if self.warehouse.retrieve_product(sku, quantity, row, col):
            self.show_message(f"Successfully retrieved {quantity} units from location {location_code}")
            self.refresh_callback()
            self.show_location_details(row, col)
        else:
            self.show_message("Failed to retrieve product. Check quantity.", is_error=True)
    
    def show_retrieve_location_form(self, row, col):
        """Show form to retrieve a product from a specific location."""
        # Clear existing widgets
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        location = self.warehouse.grid[row][col]
        
        # Form header
        ttk.Label(self.right_panel, text=f"Retrieve Product from {location.get_location_code()}", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        if not location.inventory:
            ttk.Label(self.right_panel, text="This location is empty").pack(pady=20)
            ttk.Button(self.right_panel, text="Back", 
                      command=lambda: self.show_location_details(row, col)).pack(pady=10)
            return
        
        # Create form
        form_frame = ttk.Frame(self.right_panel)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Product selection
        ttk.Label(form_frame, text="Select Product:").pack(anchor=tk.W, pady=5)
        
        product_options = []
        for sku, qty in location.inventory.items():
            if sku in self.warehouse.products:
                product_name = self.warehouse.products[sku].name
                product_options.append(f"{product_name} ({sku}) - Available: {qty}")
        
        self.product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(form_frame, textvariable=self.product_var, width=30)
        product_dropdown['values'] = product_options
        product_dropdown.pack(pady=5, fill=tk.X)
        
        # Quantity selection
        ttk.Label(form_frame, text="Quantity:").pack(anchor=tk.W, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(form_frame, from_=1, to=1000, textvariable=self.quantity_var)
        quantity_entry.pack(pady=5, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(self.right_panel)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)
        
        def retrieve_action():
            if not self.product_var.get():
                self.show_message("Please select a product.", is_error=True)
                return
                
            try:
                quantity = int(self.quantity_var.get())
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
            except ValueError:
                self.show_message("Please enter a valid quantity.", is_error=True)
                return
                
            # Extract SKU from dropdown selection
            selected = self.product_var.get()
            sku = selected.split("(")[1].split(")")[0]
            
            if self.warehouse.retrieve_product(sku, quantity, row, col):
                self.show_message(f"Successfully retrieved {quantity} units from location {location.get_location_code()}")
                self.refresh_callback()
                self.show_location_details(row, col)
            else:
                self.show_message("Failed to retrieve product. Check quantity.", is_error=True)
        
        ttk.Button(btn_frame, text="Retrieve", command=retrieve_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", 
                  command=lambda: self.show_location_details(row, col)).pack(side=tk.RIGHT, padx=5)
    
    def show_search_product_form(self):
        """Show form to search for a product in the warehouse."""
        # Clear existing widgets
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        # Form header
        ttk.Label(self.right_panel, text="Search Product in Warehouse", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Create form
        form_frame = ttk.Frame(self.right_panel)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Enter SKU or select from list:").pack(anchor=tk.W)
        
        # Product selection
        self.search_product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(form_frame, textvariable=self.search_product_var, width=30)
        product_dropdown['values'] = [f"{p.name} ({p.sku})" for p in self.warehouse.products.values()]
        product_dropdown.pack(pady=5, fill=tk.X)
        
        # Alternative: direct SKU entry
        ttk.Label(form_frame, text="OR enter SKU directly:").pack(anchor=tk.W, pady=(10, 0))
        self.search_sku_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.search_sku_var, width=30).pack(pady=5, fill=tk.X)
        
        # Search button
        ttk.Button(form_frame, text="Search", 
                  command=self.search_product_action).pack(pady=10)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.right_panel, text="Search Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollable results
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(results_frame, height=10, yscrollcommand=scrollbar.set)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.results_text.yview)
        
        # Back button
        ttk.Button(self.right_panel, text="Back", 
                  command=self.setup_right_panel).pack(side=tk.BOTTOM, pady=10)
    
    def search_product_action(self):
        """Handle the search product action."""
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Get SKU either from dropdown or direct entry
        sku = ""
        if self.search_product_var.get():
            sku = self.search_product_var.get().split("(")[1].split(")")[0]
        elif self.search_sku_var.get():
            sku = self.search_sku_var.get().strip()
            
        if not sku:
            self.show_message("Please select a product or enter an SKU.", is_error=True)
            return
            
        # Check if product exists
        if sku not in self.warehouse.products:
            self.results_text.insert(tk.END, f"Product with SKU '{sku}' not found in inventory.\n")
            return
            
        # Get product details
        product = self.warehouse.products[sku]
        self.results_text.insert(tk.END, f"Product: {product.name} (SKU: {sku})\n")
        self.results_text.insert(tk.END, f"Price: ${product.price:.2f}\n")
        self.results_text.insert(tk.END, f"Total quantity in inventory: {product.quantity}\n\n")
        
        # Find locations
        locations = self.warehouse.find_product(sku)
        
        if not locations:
            self.results_text.insert(tk.END, "This product is not stored in any warehouse location.\n")
        else:
            self.results_text.insert(tk.END, f"Found at {len(locations)} locations:\n")
            total_in_warehouse = 0
            
            for r, c in locations:
                location = self.warehouse.grid[r][c]
                qty_at_location = location.inventory[sku]
                total_in_warehouse += qty_at_location
                self.results_text.insert(tk.END, f"- Location {location.get_location_code()}: {qty_at_location} units\n")
                
            self.results_text.insert(tk.END, f"\nTotal in warehouse locations: {total_in_warehouse}\n")
    
    def show_view_location_form(self):
        """Show form to view details of a specific location."""
        # Clear existing widgets
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        # Form header
        ttk.Label(self.right_panel, text="View Warehouse Location", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Location selection
        location_frame = ttk.Frame(self.right_panel)
        location_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(location_frame, text="Row:").pack(side=tk.LEFT)
        self.view_row_var = tk.StringVar()
        row_dropdown = ttk.Combobox(location_frame, textvariable=self.view_row_var, width=5)
        row_dropdown['values'] = [chr(65 + r) for r in range(self.warehouse.rows)]
        row_dropdown.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(location_frame, text="Column:").pack(side=tk.LEFT, padx=10)
        self.view_col_var = tk.StringVar()
        col_dropdown = ttk.Combobox(location_frame, textvariable=self.view_col_var, width=5)
        col_dropdown['values'] = [str(c+1) for c in range(self.warehouse.cols)]
        col_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Info display area
        info_frame = ttk.LabelFrame(self.right_panel, text="Location Information")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.info_text = tk.Text(info_frame, height=10)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # View button
        view_btn_frame = ttk.Frame(self.right_panel)
        view_btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(view_btn_frame, text="View Location", 
                  command=self.view_location_action).pack(side=tk.LEFT)
        ttk.Button(view_btn_frame, text="Back", 
                  command=self.setup_right_panel).pack(side=tk.RIGHT)
    
    def view_location_action(self):
        """Handle the view location action."""
        self.info_text.delete(1.0, tk.END)
        
        if not self.view_row_var.get() or not self.view_col_var.get():
            self.show_message("Please select a valid location.", is_error=True)
            return
            
        try:
            row = ord(self.view_row_var.get()) - 65
            col = int(self.view_col_var.get()) - 1
            
            if row < 0 or row >= self.warehouse.rows or col < 0 or col >= self.warehouse.cols:
                self.show_message("Invalid location.", is_error=True)
                return
                
            # Show the detailed view instead
            self.show_location_details(row, col)
        except:
            self.show_message("Please select a valid location.", is_error=True)
