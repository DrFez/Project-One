import tkinter as tk
from tkinter import ttk
import time

class DashboardView:
    """View class for the dashboard tab with warehouse visualization."""
    
    def __init__(self, parent, warehouse):
        """Initialize the dashboard view."""
        self.parent = parent
        self.warehouse = warehouse
        self.last_hover_time = 0  # For throttling hover events
        self.hover_cooldown = 0.1  # Seconds between hover events
        self.active_cells = {}  # Store references to avoid garbage collection
        self.setup_dashboard()
        
    def setup_dashboard(self):
        """Set up the dashboard tab with warehouse visualization."""
        # Main container with horizontal split
        self.main_container = ttk.PanedWindow(self.parent, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for warehouse visualization
        self.left_panel = ttk.Frame(self.main_container)
        self.main_container.add(self.left_panel, weight=2)
        
        # Right panel for details and actions
        self.right_panel = ttk.Frame(self.main_container)
        self.main_container.add(self.right_panel, weight=1)
        
        # Frame for controls in left panel
        control_frame = ttk.Frame(self.left_panel)
        control_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        ttk.Label(control_frame, text="Warehouse Layout", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="Refresh", command=self.refresh_warehouse_view).pack(side=tk.RIGHT)
        
        # Frame for warehouse grid
        self.warehouse_frame = ttk.Frame(self.left_panel)
        self.warehouse_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Legend for the warehouse grid
        legend_frame = ttk.Frame(self.left_panel)
        legend_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        ttk.Label(legend_frame, text="Legend:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Label(legend_frame, text="□ Empty", background="white").pack(side=tk.LEFT, padx=5)
        ttk.Label(legend_frame, text="▲ <50% Full", background="light green").pack(side=tk.LEFT, padx=5)
        ttk.Label(legend_frame, text="■ <100% Full", background="sky blue").pack(side=tk.LEFT, padx=5)
        ttk.Label(legend_frame, text="▓ Full", background="orange red").pack(side=tk.LEFT, padx=5)
        
        # Setup right panel - initially with instructions
        self.setup_detail_panel()
        
        # Draw initial warehouse view
        self.draw_warehouse()
        
    def setup_detail_panel(self):
        """Set up the right panel for details and actions."""
        # Clear existing widgets
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        # Setup initial state with instructions
        ttk.Label(self.right_panel, text="Location Details", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(self.right_panel, text="Click on a location to view details").pack(pady=20)
        
    def draw_warehouse(self):
        """Draw the warehouse grid visualization."""
        # Clear existing widgets
        for widget in self.warehouse_frame.winfo_children():
            widget.destroy()
        
        # Reset active cells
        self.active_cells = {}
            
        # Create grid labels
        ttk.Label(self.warehouse_frame, text="").grid(row=0, column=0)
        for c in range(self.warehouse.cols):
            ttk.Label(self.warehouse_frame, text=f"{c+1}", font=("Arial", 10, "bold")).grid(row=0, column=c+1, padx=2, pady=2)
            
        # Create cells for the warehouse grid
        for r in range(self.warehouse.rows):
            row_label = chr(65 + r)
            ttk.Label(self.warehouse_frame, text=row_label, font=("Arial", 10, "bold")).grid(row=r+1, column=0, padx=2, pady=2)
            
            for c in range(self.warehouse.cols):
                location = self.warehouse.grid[r][c]
                
                # Determine color based on fill level
                if location.current_stock == 0:
                    bg_color = "white"  # Empty
                    text = "□"
                elif location.current_stock < location.capacity // 2:
                    bg_color = "light green"  # Less than 50%
                    text = "▲"
                elif location.current_stock < location.capacity:
                    bg_color = "sky blue"  # Less than 100%
                    text = "■"
                else:
                    bg_color = "orange red"  # Full
                    text = "▓"
                
                # Create cell with hover info
                cell = tk.Label(self.warehouse_frame, text=text, width=3, height=1, 
                                relief=tk.RAISED, bg=bg_color)
                cell.grid(row=r+1, column=c+1, padx=2, pady=2)
                
                # Store cell reference with its coordinates
                cell_id = f"r{r}c{c}"
                self.active_cells[cell_id] = {
                    "widget": cell,
                    "row": r,
                    "col": c
                }
                
                # Bind click event to show location actions
                cell.bind("<Button-1>", lambda event, id=cell_id: self.location_click(id))
    
    def location_click(self, cell_id):
        """Handle click on a location cell."""
        if cell_id not in self.active_cells:
            return
            
        cell_data = self.active_cells[cell_id]
        row, col = cell_data["row"], cell_data["col"]
        
        # Show location details in the right panel
        self.show_location_details(row, col)
        
    def show_location_details(self, row, col):
        """Show location details in the right panel."""
        # Clear the right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        location = self.warehouse.grid[row][col]
        
        # Location header
        ttk.Label(self.right_panel, text=f"Location {location.get_location_code()}", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
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
                  command=lambda: self.show_store_product_form(row, col)).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Retrieve Product", 
                  command=lambda: self.show_retrieve_product_form(row, col)).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Back", 
                  command=self.setup_detail_panel).pack(side=tk.RIGHT, padx=5)
                  
    def show_store_product_form(self, row, col):
        """Show form to store a product at a specific location."""
        # Clear the right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        location = self.warehouse.grid[row][col]
        
        # Form header
        ttk.Label(self.right_panel, text=f"Store Product at {location.get_location_code()}", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Create form
        form_frame = ttk.Frame(self.right_panel)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Product selection
        ttk.Label(form_frame, text="Select Product:").pack(anchor=tk.W, pady=5)
        
        product_var = tk.StringVar()
        product_options = [f"{p.name} ({p.sku})" for p in self.warehouse.products.values()]
        
        if product_options:
            product_dropdown = ttk.Combobox(form_frame, textvariable=product_var, width=30)
            product_dropdown['values'] = product_options
            product_dropdown.pack(pady=5, fill=tk.X)
        else:
            ttk.Label(form_frame, text="No products available").pack(pady=5)
            product_var = None
        
        # Quantity selection
        ttk.Label(form_frame, text="Quantity:").pack(anchor=tk.W, pady=5)
        quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(form_frame, from_=1, to=1000, textvariable=quantity_var)
        quantity_entry.pack(pady=5, fill=tk.X)
        
        # Action buttons
        action_frame = ttk.Frame(self.right_panel)
        action_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Store action function
        def store_action():
            if not product_var or not product_var.get():
                self.show_message("Please select a product")
                return
                
            try:
                quantity = int(quantity_var.get())
                if quantity <= 0:
                    raise ValueError()
            except ValueError:
                self.show_message("Please enter a valid quantity")
                return
                
            # Extract SKU
            sku = product_var.get().split("(")[1].split(")")[0]
            
            # Perform store operation
            if self.warehouse.store_product(sku, quantity, row, col):
                self.show_message(f"Successfully stored {quantity} units")
                self.refresh_warehouse_view()
                self.show_location_details(row, col)
            else:
                self.show_message("Failed to store product. Check product quantity and location capacity.")
        
        ttk.Button(action_frame, text="Store", command=store_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Cancel", 
                  command=lambda: self.show_location_details(row, col)).pack(side=tk.RIGHT, padx=5)
                  
    def show_retrieve_product_form(self, row, col):
        """Show form to retrieve a product from a specific location."""
        # Clear the right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        location = self.warehouse.grid[row][col]
        
        # Form header
        ttk.Label(self.right_panel, text=f"Retrieve Product from {location.get_location_code()}", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
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
        
        product_var = tk.StringVar()
        product_options = []
        
        for sku, qty in location.inventory.items():
            if sku in self.warehouse.products:
                product_name = self.warehouse.products[sku].name
                product_options.append(f"{product_name} ({sku}) - Available: {qty}")
        
        product_dropdown = ttk.Combobox(form_frame, textvariable=product_var, width=30)
        product_dropdown['values'] = product_options
        product_dropdown.pack(pady=5, fill=tk.X)
        
        # Quantity selection
        ttk.Label(form_frame, text="Quantity:").pack(anchor=tk.W, pady=5)
        quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(form_frame, from_=1, to=1000, textvariable=quantity_var)
        quantity_entry.pack(pady=5, fill=tk.X)
        
        # Action buttons
        action_frame = ttk.Frame(self.right_panel)
        action_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Retrieve action function
        def retrieve_action():
            if not product_var.get():
                self.show_message("Please select a product")
                return
                
            try:
                quantity = int(quantity_var.get())
                if quantity <= 0:
                    raise ValueError()
            except ValueError:
                self.show_message("Please enter a valid quantity")
                return
                
            # Extract SKU
            selected = product_var.get()
            sku = selected.split("(")[1].split(")")[0]
            
            # Perform retrieve operation
            if self.warehouse.retrieve_product(sku, quantity, row, col):
                self.show_message(f"Successfully retrieved {quantity} units")
                self.refresh_warehouse_view()
                self.show_location_details(row, col)
            else:
                self.show_message("Failed to retrieve product. Check quantity.")
        
        ttk.Button(action_frame, text="Retrieve", command=retrieve_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Cancel", 
                  command=lambda: self.show_location_details(row, col)).pack(side=tk.RIGHT, padx=5)
    
    def show_message(self, message, is_error=False):
        """Show a message in the UI instead of a popup dialog."""
        # Create a transient message at the bottom of the right panel
        msg_frame = ttk.Frame(self.right_panel)
        msg_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        if is_error:
            bg_color = "#ffcccc"  # Light red for errors
        else:
            bg_color = "#ccffcc"  # Light green for success
            
        msg_label = ttk.Label(msg_frame, text=message, background=bg_color, padding=5)
        msg_label.pack(fill=tk.X)
        
        # Auto-remove the message after 3 seconds
        self.parent.after(3000, lambda: msg_frame.destroy())
    
    def refresh_warehouse_view(self):
        """Refresh the warehouse grid visualization."""
        self.draw_warehouse()
