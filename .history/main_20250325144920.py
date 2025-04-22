import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from product import Product
from warehouse import Warehouse

class WarehouseApp:
    """Main application class for the Warehouse Inventory Management System GUI."""
    
    def __init__(self, root):
        """Initialize the application with the root window."""
        self.root = root
        self.root.title("Warehouse Inventory Management System")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        
        # Setup warehouse
        self.setup_warehouse()
        
        # Create main interface
        self.create_widgets()
        
    def setup_warehouse(self):
        """Set up the warehouse dimensions through a dialog."""
        # Default warehouse dimensions
        rows = 5
        cols = 8
        
        # Try to get dimensions from user
        try:
            rows_input = simpledialog.askinteger("Warehouse Setup", "Enter number of rows (1-26):", 
                                                minvalue=1, maxvalue=26, initialvalue=5)
            if rows_input:
                rows = rows_input
                
            cols_input = simpledialog.askinteger("Warehouse Setup", "Enter number of columns (1-99):", 
                                                minvalue=1, maxvalue=99, initialvalue=8)
            if cols_input:
                cols = cols_input
        except:
            pass  # Use defaults if dialog is cancelled
            
        self.warehouse = Warehouse(rows, cols)
        
    def create_widgets(self):
        """Create all the widgets for the main interface."""
        # Create a notebook for tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.products_frame = ttk.Frame(self.notebook)
        self.storage_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.notebook.add(self.products_frame, text="Products")
        self.notebook.add(self.storage_frame, text="Storage Operations")
        
        # Setup each tab
        self.setup_dashboard()
        self.setup_products_tab()
        self.setup_storage_tab()
        
    def setup_dashboard(self):
        """Set up the dashboard tab with warehouse visualization."""
        # Frame for controls
        control_frame = ttk.Frame(self.dashboard_frame)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        ttk.Label(control_frame, text="Warehouse Layout", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=10)
        ttk.Button(control_frame, text="Refresh", command=self.refresh_warehouse_view).pack(side=tk.RIGHT, padx=10)
        
        # Frame for warehouse grid
        self.warehouse_frame = ttk.Frame(self.dashboard_frame)
        self.warehouse_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Draw initial warehouse view
        self.draw_warehouse()
        
        # Legend for the warehouse grid
        legend_frame = ttk.Frame(self.dashboard_frame)
        legend_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        ttk.Label(legend_frame, text="Legend:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Label(legend_frame, text="□ Empty", background="white").pack(side=tk.LEFT, padx=5)
        ttk.Label(legend_frame, text="▲ <50% Full", background="light green").pack(side=tk.LEFT, padx=5)
        ttk.Label(legend_frame, text="■ <100% Full", background="sky blue").pack(side=tk.LEFT, padx=5)
        ttk.Label(legend_frame, text="▓ Full", background="orange red").pack(side=tk.LEFT, padx=5)
        
    def draw_warehouse(self):
        """Draw the warehouse grid visualization."""
        # Clear existing widgets
        for widget in self.warehouse_frame.winfo_children():
            widget.destroy()
            
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
                
                # Create cell with hover info
                cell = tk.Label(self.warehouse_frame, text=text, width=3, height=1, 
                                relief=tk.RAISED, bg=bg_color)
                cell.grid(row=r+1, column=c+1, padx=2, pady=2)
                
                # Bind hover event to show location details
                cell.bind("<Enter>", lambda event, r=r, c=c: self.show_location_info(event, r, c))
                cell.bind("<Leave>", self.hide_location_info)
                
                # Bind click event to show location actions
                cell.bind("<Button-1>", lambda event, r=r, c=c: self.location_click(r, c))
        
    def show_location_info(self, event, row, col):
        """Show information about a location when hovering over it."""
        location = self.warehouse.grid[row][col]
        info = f"Location: {location.get_location_code()}\n"
        info += f"Usage: {location.current_stock}/{location.capacity}\n"
        
        if location.inventory:
            info += "Products:\n"
            for sku, qty in location.inventory.items():
                if sku in self.warehouse.products:
                    product_name = self.warehouse.products[sku].name
                    info += f"- {product_name} ({sku}): {qty}\n"
        else:
            info += "Empty location"
            
        # Show tooltip
        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.wm_overrideredirect(True)
        x, y, _, _ = event.widget.bbox("insert")
        x += event.widget.winfo_rootx() + 25
        y += event.widget.winfo_rooty() + 25
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(self.tooltip, text=info, relief=tk.SOLID, background="#ffffe0", padding=5)
        label.pack()
        
    def hide_location_info(self, event):
        """Hide the location info tooltip."""
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()
            
    def location_click(self, row, col):
        """Handle click on a location cell."""
        location = self.warehouse.grid[row][col]
        location_code = location.get_location_code()
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Location {location_code}")
        dialog.geometry("300x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Location {location_code}", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(dialog, text=f"Capacity: {location.current_stock}/{location.capacity}").pack(pady=5)
        
        # List products at this location
        if location.inventory:
            ttk.Label(dialog, text="Products at this location:", font=("Arial", 10, "bold")).pack(pady=5)
            product_frame = ttk.Frame(dialog)
            product_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Create scrollable list
            scrollbar = ttk.Scrollbar(product_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            product_list = tk.Listbox(product_frame, yscrollcommand=scrollbar.set)
            product_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=product_list.yview)
            
            for sku, qty in location.inventory.items():
                if sku in self.warehouse.products:
                    product_name = self.warehouse.products[sku].name
                    product_list.insert(tk.END, f"{product_name} ({sku}): {qty}")
        else:
            ttk.Label(dialog, text="This location is empty").pack(pady=10)
            
        # Action buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Store Product", 
                   command=lambda: self.open_store_dialog(row, col, dialog)).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Retrieve Product", 
                   command=lambda: self.open_retrieve_dialog(row, col, dialog)).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Close", command=dialog.destroy).pack(side=tk.RIGHT, padx=10)
        
    def open_store_dialog(self, row, col, parent_dialog=None):
        """Open dialog to store product at a specific location."""
        if not self.warehouse.products:
            messagebox.showinfo("No Products", "No products available to store. Please add products first.")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Store Product")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        location = self.warehouse.grid[row][col]
        
        ttk.Label(dialog, text=f"Store Product at Location {location.get_location_code()}", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Product selection
        ttk.Label(dialog, text="Select Product:").pack(anchor=tk.W, padx=20, pady=5)
        
        product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(dialog, textvariable=product_var, width=30)
        product_dropdown['values'] = [f"{p.name} ({p.sku})" for p in self.warehouse.products.values()]
        product_dropdown.pack(padx=20, pady=5, fill=tk.X)
        
        # Quantity selection
        ttk.Label(dialog, text="Quantity:").pack(anchor=tk.W, padx=20, pady=5)
        quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(dialog, from_=1, to=1000, textvariable=quantity_var)
        quantity_entry.pack(padx=20, pady=5, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, pady=20, padx=20)
        
        def store_action():
            if not product_var.get():
                messagebox.showwarning("Input Error", "Please select a product.")
                return
                
            try:
                quantity = int(quantity_var.get())
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid quantity.")
                return
                
            # Extract SKU from dropdown selection
            sku = product_var.get().split("(")[1].split(")")[0]
            
            if self.warehouse.store_product(sku, quantity, row, col):
                messagebox.showinfo("Success", f"Successfully stored {quantity} units at location {location.get_location_code()}")
                dialog.destroy()
                if parent_dialog:
                    parent_dialog.destroy()
                self.refresh_warehouse_view()
            else:
                messagebox.showerror("Error", "Failed to store product. Check product quantity and location capacity.")
        
        ttk.Button(btn_frame, text="Store", command=store_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
        
    def open_retrieve_dialog(self, row, col, parent_dialog=None):
        """Open dialog to retrieve product from a specific location."""
        location = self.warehouse.grid[row][col]
        
        if not location.inventory:
            messagebox.showinfo("Empty Location", "This location is empty.")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Retrieve Product")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Retrieve Product from Location {location.get_location_code()}", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Product selection
        ttk.Label(dialog, text="Select Product:").pack(anchor=tk.W, padx=20, pady=5)
        
        product_options = []
        for sku, qty in location.inventory.items():
            if sku in self.warehouse.products:
                product_name = self.warehouse.products[sku].name
                product_options.append(f"{product_name} ({sku}) - Available: {qty}")
        
        product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(dialog, textvariable=product_var, width=30)
        product_dropdown['values'] = product_options
        product_dropdown.pack(padx=20, pady=5, fill=tk.X)
        
        # Quantity selection
        ttk.Label(dialog, text="Quantity:").pack(anchor=tk.W, padx=20, pady=5)
        quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(dialog, from_=1, to=1000, textvariable=quantity_var)
        quantity_entry.pack(padx=20, pady=5, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, pady=20, padx=20)
        
        def retrieve_action():
            if not product_var.get():
                messagebox.showwarning("Input Error", "Please select a product.")
                return
                
            try:
                quantity = int(quantity_var.get())
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid quantity.")
                return
                
            # Extract SKU from dropdown selection
            selected = product_var.get()
            sku = selected.split("(")[1].split(")")[0]
            
            if self.warehouse.retrieve_product(sku, quantity, row, col):
                messagebox.showinfo("Success", f"Successfully retrieved {quantity} units from location {location.get_location_code()}")
                dialog.destroy()
                if parent_dialog:
                    parent_dialog.destroy()
                self.refresh_warehouse_view()
            else:
                messagebox.showerror("Error", "Failed to retrieve product. Check quantity.")
        
        ttk.Button(btn_frame, text="Retrieve", command=retrieve_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
        
    def refresh_warehouse_view(self):
        """Refresh the warehouse grid visualization."""
        self.draw_warehouse()
        
    def setup_products_tab(self):
        """Set up the products management tab."""
        # Frame for controls
        control_frame = ttk.Frame(self.products_frame)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        ttk.Label(control_frame, text="Product Management", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=10)
        ttk.Button(control_frame, text="Add New Product", command=self.add_product_dialog).pack(side=tk.RIGHT, padx=10)
        
        # Frame for product list
        self.product_list_frame = ttk.Frame(self.products_frame)
        self.product_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tree view for products
        self.setup_product_treeview()
    
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
        
        # Bind double-click event to edit product
        self.product_tree.bind("<Double-1>", self.edit_product_dialog)
    
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
    
    def add_product_dialog(self):
        """Open dialog to add a new product."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Product")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Add New Product", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Product name
        ttk.Label(dialog, text="Product Name:").pack(anchor=tk.W, padx=20, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=30).pack(padx=20, pady=5, fill=tk.X)
        
        # SKU
        ttk.Label(dialog, text="SKU:").pack(anchor=tk.W, padx=20, pady=5)
        sku_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=sku_var, width=30).pack(padx=20, pady=5, fill=tk.X)
        
        # Price
        ttk.Label(dialog, text="Price:").pack(anchor=tk.W, padx=20, pady=5)
        price_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=price_var, width=30).pack(padx=20, pady=5, fill=tk.X)
        
        # Quantity
        ttk.Label(dialog, text="Initial Quantity:").pack(anchor=tk.W, padx=20, pady=5)
        quantity_var = tk.StringVar(value="0")
        ttk.Spinbox(dialog, from_=0, to=10000, textvariable=quantity_var).pack(padx=20, pady=5, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, pady=20, padx=20)
        
        def add_action():
            name = name_var.get().strip()
            sku = sku_var.get().strip()
            price_str = price_var.get().strip()
            quantity_str = quantity_var.get().strip()
            
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
            dialog.destroy()
            self.refresh_product_list()
        
        ttk.Button(btn_frame, text="Add Product", command=add_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def edit_product_dialog(self, event):
        """Open dialog to edit an existing product."""
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
            
        product = self.warehouse.products[sku]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Product")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Edit Product", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Product name
        ttk.Label(dialog, text="Product Name:").pack(anchor=tk.W, padx=20, pady=5)
        name_var = tk.StringVar(value=product.name)
        ttk.Entry(dialog, textvariable=name_var, width=30).pack(padx=20, pady=5, fill=tk.X)
        
        # SKU (read-only)
        ttk.Label(dialog, text="SKU (read-only):").pack(anchor=tk.W, padx=20, pady=5)
        sku_var = tk.StringVar(value=product.sku)
        ttk.Entry(dialog, textvariable=sku_var, width=30, state="readonly").pack(padx=20, pady=5, fill=tk.X)
        
        # Price
        ttk.Label(dialog, text="Price:").pack(anchor=tk.W, padx=20, pady=5)
        price_var = tk.StringVar(value=str(product.price))
        ttk.Entry(dialog, textvariable=price_var, width=30).pack(padx=20, pady=5, fill=tk.X)
        
        # Quantity
        ttk.Label(dialog, text="Quantity:").pack(anchor=tk.W, padx=20, pady=5)
        quantity_var = tk.StringVar(value=str(product.quantity))
        ttk.Spinbox(dialog, from_=0, to=10000, textvariable=quantity_var).pack(padx=20, pady=5, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, pady=20, padx=20)
        
        def update_action():
            name = name_var.get().strip()
            price_str = price_var.get().strip()
            quantity_str = quantity_var.get().strip()
            
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
            product.name = name
            product.update_price(price)
            
            # Handle quantity change
            if quantity != product.quantity:
                delta = quantity - product.quantity
                product.update_quantity(delta)
            
            messagebox.showinfo("Success", "Product updated successfully.")
            dialog.destroy()
            self.refresh_product_list()
        
        ttk.Button(btn_frame, text="Update", command=update_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def setup_storage_tab(self):
        """Set up the storage operations tab."""
        # Left frame for operations
        operations_frame = ttk.LabelFrame(self.storage_frame, text="Operations")
        operations_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10, expand=False)
        
        # Add operation buttons
        ttk.Button(operations_frame, text="Store Product", 
                   command=self.store_product_operation, width=20).pack(pady=10, padx=20)
        ttk.Button(operations_frame, text="Retrieve Product", 
                   command=self.retrieve_product_operation, width=20).pack(pady=10, padx=20)
        ttk.Button(operations_frame, text="Search Product", 
                   command=self.search_product_operation, width=20).pack(pady=10, padx=20)
        ttk.Button(operations_frame, text="View Location", 
                   command=self.view_location_operation, width=20).pack(pady=10, padx=20)
        
        # Right frame for warehouse mini-map
        map_frame = ttk.LabelFrame(self.storage_frame, text="Warehouse Map")
        map_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)
        
        self.mini_map_frame = ttk.Frame(map_frame)
        self.mini_map_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Draw mini map
        self.draw_mini_map()
    
    def draw_mini_map(self):
        """Draw a smaller version of the warehouse map for the storage tab."""
        # Clear existing widgets
        for widget in self.mini_map_frame.winfo_children():
            widget.destroy()
            
        # Create a canvas for the mini-map
        canvas_width = 400
        canvas_height = 300
        
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
                               lambda event, r=r, c=c: self.location_click(r, c))
        
    def store_product_operation(self):
        """Operation to store a product in the warehouse."""
        if not self.warehouse.products:
            messagebox.showinfo("No Products", "No products available to store. Please add products first.")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Store Product Operation")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Store Product in Warehouse", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Product selection
        ttk.Label(dialog, text="Select Product:").pack(anchor=tk.W, padx=20, pady=5)
        
        product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(dialog, textvariable=product_var, width=30)
        product_dropdown['values'] = [f"{p.name} ({p.sku}) - In Stock: {p.quantity}" 
                                      for p in self.warehouse.products.values()]
        product_dropdown.pack(padx=20, pady=5, fill=tk.X)
        
        # Quantity selection
        ttk.Label(dialog, text="Quantity:").pack(anchor=tk.W, padx=20, pady=5)
        quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(dialog, from_=1, to=1000, textvariable=quantity_var)
        quantity_entry.pack(padx=20, pady=5, fill=tk.X)
        
        # Location selection
        ttk.Label(dialog, text="Select Location:").pack(anchor=tk.W, padx=20, pady=5)
        location_frame = ttk.Frame(dialog)
        location_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(location_frame, text="Row:").pack(side=tk.LEFT)
        row_var = tk.StringVar()
        row_dropdown = ttk.Combobox(location_frame, textvariable=row_var, width=5)
        row_dropdown['values'] = [chr(65 + r) for r in range(self.warehouse.rows)]
        row_dropdown.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(location_frame, text="Column:").pack(side=tk.LEFT, padx=10)
        col_var = tk.StringVar()
        col_dropdown = ttk.Combobox(location_frame, textvariable=col_var, width=5)
        col_dropdown['values'] = [str(c+1) for c in range(self.warehouse.cols)]
        col_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, pady=20, padx=20)
        
        def store_action():
            if not product_var.get():
                messagebox.showwarning("Input Error", "Please select a product.")
                return
                
            if not row_var.get() or not col_var.get():
                messagebox.showwarning("Input Error", "Please select a location.")
                return
                
            try:
                quantity = int(quantity_var.get())
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid quantity.")
                return
                
            # Extract SKU from dropdown selection
            sku = product_var.get().split("(")[1].split(")")[0]
            
            # Convert row letter to index (A=0, B=1, etc.)
            row = ord(row_var.get()) - 65
            # Convert column number to index (1=0, 2=1, etc.)
            col = int(col_var.get()) - 1
            
            if self.warehouse.store_product(sku, quantity, row, col):
                messagebox.showinfo("Success", f"Successfully stored {quantity} units at location {row_var.get()}{col_var.get()}")
                dialog.destroy()
                self.refresh_warehouse_view()
                self.draw_mini_map()
                self.refresh_product_list()
            else:
                messagebox.showerror("Error", "Failed to store product. Check product quantity and location capacity.")
        
        ttk.Button(btn_frame, text="Store", command=store_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def retrieve_product_operation(self):
        """Operation to retrieve a product from the warehouse."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Retrieve Product Operation")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Retrieve Product from Warehouse", font=("Arial", 12, "bold")).pack(pady=10)
        
        # First frame: select product
        product_frame = ttk.LabelFrame(dialog, text="Step 1: Select Product")
        product_frame.pack(fill=tk.X, padx=20, pady=10)
        
        product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(product_frame, textvariable=product_var, width=30)
        product_dropdown['values'] = [f"{p.name} ({p.sku})" for p in self.warehouse.products.values()]
        product_dropdown.pack(padx=10, pady=10, fill=tk.X)
        
        # Second frame: will show locations after product selection
        location_frame = ttk.LabelFrame(dialog, text="Step 2: Select Location")
        location_frame.pack(fill=tk.X, padx=20, pady=10)
        
        location_list = tk.Listbox(location_frame, height=5)
        location_list.pack(padx=10, pady=10, fill=tk.X)
        
        # Update locations when product is selected
        def update_locations(*args):
            location_list.delete(0, tk.END)
            
            if not product_var.get():
                return
                
            sku = product_var.get().split("(")[1].split(")")[0]
            locations = self.warehouse.find_product(sku)
            
            if not locations:
                location_list.insert(tk.END, "Product not found in any location")
            else:
                for r, c in locations:
                    location = self.warehouse.grid[r][c]
                    location_list.insert(tk.END, 
                                        f"{location.get_location_code()} - {location.inventory[sku]} units")
        
        product_var.trace("w", update_locations)
        
        # Third frame: quantity selection
        quantity_frame = ttk.LabelFrame(dialog, text="Step 3: Enter Quantity")
        quantity_frame.pack(fill=tk.X, padx=20, pady=10)
        
        quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(quantity_frame, from_=1, to=1000, textvariable=quantity_var)
        quantity_entry.pack(padx=10, pady=10, fill=tk.X)
        
        # Action buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, pady=20, padx=20)
        
        def retrieve_action():
            if not product_var.get():
                messagebox.showwarning("Input Error", "Please select a product.")
                return
                
            selected_location = location_list.curselection()
            if not selected_location:
                messagebox.showwarning("Input Error", "Please select a location.")
                return
                
            location_text = location_list.get(selected_location[0])
            if "not found" in location_text:
                messagebox.showwarning("Error", "Product not available at any location.")
                return
                
            try:
                quantity = int(quantity_var.get())
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid quantity.")
                return
                
            # Extract SKU from dropdown selection
            sku = product_var.get().split("(")[1].split(")")[0]
            
            # Extract location code from list selection
            location_code = location_text.split(" - ")[0]
            row = ord(location_code[0]) - 65
            col = int(location_code[1:]) - 1
            
            if self.warehouse.retrieve_product(sku, quantity, row, col):
                messagebox.showinfo("Success", f"Successfully retrieved {quantity} units from location {location_code}")
                dialog.destroy()
                self.refresh_warehouse_view()
                self.draw_mini_map()
                self.refresh_product_list()
            else:
                messagebox.showerror("Error", "Failed to retrieve product. Check quantity.")
        
        ttk.Button(btn_frame, text="Retrieve", command=retrieve_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def search_product_operation(self):
        """Operation to search for a product in the warehouse."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Search Product")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Search Product in Warehouse", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Search frame
        search_frame = ttk.Frame(dialog)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(search_frame, text="Enter SKU or select from list:").pack(anchor=tk.W)
        
        # Product selection
        product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(search_frame, textvariable=product_var, width=30)
        product_dropdown['values'] = [f"{p.name} ({p.sku})" for p in self.warehouse.products.values()]
        product_dropdown.pack(pady=5, fill=tk.X)
        
        # Alternative: direct SKU entry
        ttk.Label(search_frame, text="OR enter SKU directly:").pack(anchor=tk.W, pady=(10, 0))
        sku_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=sku_var, width=30).pack(pady=5, fill=tk.X)
        
        # Results frame
        results_frame = ttk.LabelFrame(dialog, text="Search Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollable results
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        results_text = tk.Text(results_frame, height=10, yscrollcommand=scrollbar.set)
        results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=results_text.yview)
        
        # Action buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, pady=10, padx=20)
        
        def search_action():
            # Clear previous results
            results_text.delete(1.0, tk.END)
            
            # Get SKU either from dropdown or direct entry
            sku = ""
            if product_var.get():
                sku = product_var.get().split("(")[1].split(")")[0]
            elif sku_var.get():
                sku = sku_var.get().strip()
                
            if not sku:
                messagebox.showwarning("Input Error", "Please select a product or enter an SKU.")
                return
                
            # Check if product exists
            if sku not in self.warehouse.products:
                results_text.insert(tk.END, f"Product with SKU '{sku}' not found in inventory.\n")
                return
                
            # Get product details
            product = self.warehouse.products[sku]
            results_text.insert(tk.END, f"Product: {product.name} (SKU: {sku})\n")
            results_text.insert(tk.END, f"Price: ${product.price:.2f}\n")
            results_text.insert(tk.END, f"Total quantity in inventory: {product.quantity}\n\n")
            
            # Find locations
            locations = self.warehouse.find_product(sku)
            
            if not locations:
                results_text.insert(tk.END, "This product is not stored in any warehouse location.\n")
            else:
                results_text.insert(tk.END, f"Found at {len(locations)} locations:\n")
                total_in_warehouse = 0
                
                for r, c in locations:
                    location = self.warehouse.grid[r][c]
                    qty_at_location = location.inventory[sku]
                    total_in_warehouse += qty_at_location
                    results_text.insert(tk.END, f"- Location {location.get_location_code()}: {qty_at_location} units\n")
                    
                results_text.insert(tk.END, f"\nTotal in warehouse locations: {total_in_warehouse}\n")
        
        ttk.Button(btn_frame, text="Search", command=search_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Close", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def view_location_operation(self):
        """Operation to view details of a specific location."""
        dialog = tk.Toplevel(self.root)
        dialog.title("View Location")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="View Warehouse Location", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Location selection
        location_frame = ttk.Frame(dialog)
        location_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(location_frame, text="Row:").pack(side=tk.LEFT)
        row_var = tk.StringVar()
        row_dropdown = ttk.Combobox(location_frame, textvariable=row_var, width=5)
        row_dropdown['values'] = [chr(65 + r) for r in range(self.warehouse.rows)]
        row_dropdown.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(location_frame, text="Column:").pack(side=tk.LEFT, padx=10)
        col_var = tk.StringVar()
        col_dropdown = ttk.Combobox(location_frame, textvariable=col_var, width=5)
        col_dropdown['values'] = [str(c+1) for c in range(self.warehouse.cols)]
        col_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Info display area
        info_frame = ttk.LabelFrame(dialog, text="Location Information")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        info_text = tk.Text(info_frame, height=10)
        info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Update information when location is selected
        def update_info(*args):
            info_text.delete(1.0, tk.END)
            
            if not row_var.get() or not col_var.get():
                return
                
            try:
                row = ord(row_var.get()) - 65
                col = int(col_var.get()) - 1
                
                if row < 0 or row >= self.warehouse.rows or col < 0 or col >= self.warehouse.cols:
                    info_text.insert(tk.END, "Invalid location.")
                    return
                    
                location = self.warehouse.grid[row][col]
                info_text.insert(tk.END, f"Location: {location.get_location_code()}\n")
                info_text.insert(tk.END, f"Capacity: {location.capacity} units\n")
                info_text.insert(tk.END, f"Current usage: {location.current_stock} units\n")
                info_text.insert(tk.END, f"Available space: {location.get_available_capacity()} units\n\n")
                
                if location.inventory:
                    info_text.insert(tk.END, "Products stored at this location:\n")
                    for sku, qty in location.inventory.items():
                        if sku in self.warehouse.products:
                            product_name = self.warehouse.products[sku].name
                            info_text.insert(tk.END, f"- {product_name} ({sku}): {qty} units\n")
                else:
                    info_text.insert(tk.END, "This location is empty.")
            except:
                info_text.insert(tk.END, "Please select a valid location.")
        
        row_var.trace("w", update_info)
        col_var.trace("w", update_info)
        
        # Action buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, pady=10, padx=20)
        
        ttk.Button(btn_frame, text="Close", command=dialog.destroy).pack(side=tk.RIGHT)

def main():
    """Main function to run the warehouse management application."""
    root = tk.Tk()
    app = WarehouseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
