import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

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
            total_in_warehouse = sum(
                location.inventory.get(product.sku, 0) for row in self.warehouse.grid for location in row
            )
            row_color = "red" if total_in_warehouse != product.quantity else ""
            self.product_tree.insert("", tk.END, values=(
                product.name, 
                product.sku, 
                f"${product.price:.2f}", 
                product.quantity
            ), tags=("mismatch",) if row_color == "red" else ())
        
        # Apply row styling
        self.product_tree.tag_configure("mismatch", background="red")
    
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
        
        # Check for mismatched quantities
        total_in_warehouse = sum(
            location.inventory.get(product.sku, 0) for row in self.warehouse.grid for location in row
        )
        if total_in_warehouse != product.quantity:
            ttk.Label(details_frame, text="⚠️ Mismatched Quantities Detected", foreground="red").pack(anchor=tk.W, padx=10, pady=5)
            ttk.Label(details_frame, text=f"Total in warehouse: {total_in_warehouse}", foreground="red").pack(anchor=tk.W, padx=10, pady=2)
            
            if total_in_warehouse > product.quantity:
                ttk.Button(details_frame, text="Resolve Excess Quantity", 
                           command=lambda: self.resolve_excess_quantity(product, total_in_warehouse)).pack(anchor=tk.W, padx=10, pady=5)
            else:
                ttk.Button(details_frame, text="Auto Fix", command=lambda: self.auto_fix_mismatch(product)).pack(anchor=tk.W, padx=10, pady=5)
        
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
        ttk.Button(action_frame, text="Delete Product", 
                  command=lambda: self.delete_product_action(sku)).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Back", 
                  command=self.setup_right_panel).pack(side=tk.RIGHT, padx=5)
    
    def resolve_excess_quantity(self, product, total_in_warehouse):
        """Handle excess quantity in the warehouse for a product."""
        excess_quantity = total_in_warehouse - product.quantity
        
        def update_product_quantity():
            """Update the product's total quantity to match the warehouse."""
            product.update_quantity(excess_quantity)
            self.warehouse.data_storage.save_products(self.warehouse.products)  # Save updated product data
            self.show_message(f"Product quantity updated to match the warehouse: {total_in_warehouse}")
            self.refresh_product_list()
            self.refresh_warehouse_callback()
            self.show_product_details_by_sku(product.sku)
        
        def remove_excess_from_warehouse():
            """Remove excess quantity from the warehouse."""
            remaining_to_remove = excess_quantity
            for row in self.warehouse.grid:
                for location in row:
                    if remaining_to_remove <= 0:
                        break
                    if product.sku in location.inventory:
                        qty_at_location = location.inventory[product.sku]
                        qty_to_remove = min(remaining_to_remove, qty_at_location)
                        location.remove_product(product.sku, qty_to_remove)
                        remaining_to_remove -= qty_to_remove
            
            # Rebuild the product locations cache to ensure consistency
            self.warehouse._rebuild_location_cache()
            self.warehouse.data_storage.save_locations(self.warehouse.grid)  # Save updated location data
            
            self.show_message(f"Excess quantity removed from the warehouse: {excess_quantity}")
            self.refresh_product_list()
            self.refresh_warehouse_callback()
            self.show_product_details_by_sku(product.sku)
        
        # Prompt user for action
        action_window = tk.Toplevel(self.parent)
        action_window.title("Resolve Excess Quantity")
        action_window.geometry("400x200")
        
        ttk.Label(action_window, text=f"Excess quantity detected for {product.name} (SKU: {product.sku})", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(action_window, text=f"Total in warehouse: {total_in_warehouse}, Reported quantity: {product.quantity}", 
                 foreground="red").pack(pady=5)
        
        ttk.Label(action_window, text="Choose an action:").pack(pady=10)
        
        ttk.Button(action_window, text="Update Product Quantity", 
                   command=lambda: [update_product_quantity(), action_window.destroy()]).pack(pady=5)
        ttk.Button(action_window, text="Remove Excess from Warehouse", 
                   command=lambda: [remove_excess_from_warehouse(), action_window.destroy()]).pack(pady=5)
        ttk.Button(action_window, text="Cancel", command=action_window.destroy).pack(pady=5)
    
    def auto_fix_mismatch(self, product):
        """Automatically fix mismatched quantities for the selected product."""
        quantity_to_distribute = product.quantity - sum(
            location.inventory.get(product.sku, 0) for row in self.warehouse.grid for location in row
        )
        fix_report = []

        for row in self.warehouse.grid:
            for location in row:
                if quantity_to_distribute <= 0:
                    break
                available_space = location.get_available_capacity()
                if available_space > 0:
                    quantity_to_store = min(quantity_to_distribute, available_space)
                    location.add_product(product, quantity_to_store)
                    quantity_to_distribute -= quantity_to_store
                    fix_report.append(
                        f"Moved {quantity_to_store} units of {product.name} (SKU: {product.sku}) to Location {location.get_location_code()} "
                        f"due to available space."
                    )
        
        if quantity_to_distribute > 0:
            fix_report.append(
                f"⚠️ Unable to fully distribute {quantity_to_distribute} units of {product.name} (SKU: {product.sku}) due to insufficient space."
            )
        
        # Refresh UI and show fix report
        self.refresh_product_list()
        self.refresh_warehouse_callback()
        self.show_fix_report(fix_report)
    
    def show_fix_report(self, report):
        """Display the fix report in a popup dialog."""
        report_window = tk.Toplevel(self.parent)
        report_window.title("Fix Report")
        report_window.geometry("500x400")
        
        ttk.Label(report_window, text="Fix Report", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Scrollable text area
        text_area = tk.Text(report_window, wrap=tk.WORD, height=20)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for line in report:
            text_area.insert(tk.END, line + "\n")
        
        text_area.config(state=tk.DISABLED)  # Make the text area read-only
        
        ttk.Button(report_window, text="Close", command=report_window.destroy).pack(pady=10)
    
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
        
        # SKU with Generate button
        ttk.Label(form_frame, text="SKU:").pack(anchor=tk.W, pady=5)
        sku_frame = ttk.Frame(form_frame)
        sku_frame.pack(fill=tk.X, pady=5)
        
        self.sku_var = tk.StringVar()
        ttk.Entry(sku_frame, textvariable=self.sku_var, width=20).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(sku_frame, text="Generate SKU", command=self.generate_sku).pack(side=tk.RIGHT, padx=5)
        
        # Price
        ttk.Label(form_frame, text="Price:").pack(anchor=tk.W, pady=5)
        self.price_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.price_var, width=30).pack(pady=5, fill=tk.X)
        
        # Quantity
        ttk.Label(form_frame, text="Initial Quantity:").pack(anchor=tk.W, pady=5)
        self.quantity_var = tk.StringVar(value="0")
        ttk.Spinbox(form_frame, from_=0, to=10000, textvariable=self.quantity_var).pack(pady=5, fill=tk.X)
        
        # Location assignment option
        ttk.Label(form_frame, text="Location Assignment:").pack(anchor=tk.W, pady=5)
        self.location_option = tk.StringVar(value="automatic")
        options_frame = ttk.Frame(form_frame)
        options_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(options_frame, text="Automatic Distribution", variable=self.location_option, 
                       value="automatic").pack(anchor=tk.W)
        ttk.Radiobutton(options_frame, text="Manual Assignment", variable=self.location_option, 
                       value="manual").pack(anchor=tk.W)
        
        # Action buttons
        btn_frame = ttk.Frame(self.right_panel)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Button(btn_frame, text="Add Product", command=self.add_product_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", 
                  command=self.setup_right_panel).pack(side=tk.RIGHT, padx=5)
    
    def generate_sku(self):
        """Generate a unique SKU based on product name."""
        name = self.name_var.get().strip()
        if not name:
            self.show_message("Please enter a product name first", is_error=True)
            return
            
        # Take first 3 letters of product name (or fewer if name is shorter)
        prefix = ''.join(c for c in name[:3].upper() if c.isalnum())
        if not prefix:
            prefix = 'PRD'  # Default prefix if name has no valid characters
            
        # Try up to 10 times to generate a unique SKU
        for _ in range(10):
            # Generate random 4-digit number
            suffix = ''.join(random.choices(string.digits, k=4))
            sku = f"{prefix}{suffix}"
            
            # Check if SKU is unique
            if sku not in self.warehouse.products:
                self.sku_var.set(sku)
                self.show_message(f"Generated SKU: {sku}")
                return
                
        # If we couldn't generate a unique SKU after 10 tries
        self.show_message("Could not generate a unique SKU. Please enter manually.", is_error=True)
    
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
            
        # Create product and add to warehouse (without auto-distributing)
        product = Product(name, sku, price, quantity)
        
        print(f"DEBUG: Creating new product {sku} with quantity {quantity}")
        if not self.warehouse.add_product(product):
            self.show_message("Failed to add product.", is_error=True)
            return
        
        # Handle location assignment based on user choice
        if self.location_option.get() == "automatic" and quantity > 0:
            # Use warehouse's distribution method
            print(f"DEBUG: Automatic distribution selected for {sku}")
            self.warehouse.distribute_initial_quantity(product)
            self.warehouse.data_storage.save_products(self.warehouse.products)
            self.warehouse.data_storage.save_locations(self.warehouse.grid)
            
            # Force rebuild of location cache to ensure accuracy
            self.warehouse._rebuild_location_cache()
            
            self.warehouse.data_storage.save_log(self.warehouse.user,
                f"Added product {sku} with automatic location assignment")
            
            # Refresh views and show success message
            self.refresh_product_list()
            self.refresh_warehouse_callback()
            self.show_message(f"Product '{name}' added and distributed to warehouse locations.")
            
            # Show product details instead of going back to main panel
            self.show_product_details_by_sku(sku)
        elif self.location_option.get() == "manual" and quantity > 0:
            # Show manual assignment form
            print(f"DEBUG: Manual distribution selected for {sku}")
            self.warehouse.data_storage.save_products(self.warehouse.products)
            self.show_message(f"Product '{name}' added. Please assign locations.")
            self.show_manual_location_assignment(sku)
        else:
            # Zero quantity or unknown option, just log it
            print(f"DEBUG: No distribution needed for {sku} (quantity {quantity})")
            self.warehouse.data_storage.save_products(self.warehouse.products)
            self.warehouse.data_storage.save_log(self.warehouse.user, f"Added product {sku}")
            self.show_message(f"Product '{name}' added successfully.")
            self.refresh_product_list()
            self.setup_right_panel()  # Return to main view
    
    def show_manual_location_assignment(self, sku):
        """Show form for manually assigning product locations."""
        # Create a new dialog for location assignment
        assign_window = tk.Toplevel(self.parent)
        assign_window.title("Assign Product Locations")
        assign_window.geometry("450x500")
        assign_window.transient(self.parent)
        assign_window.grab_set()
        
        product = self.warehouse.products[sku]
        
        # Dialog header
        ttk.Label(assign_window, text=f"Assign Locations for {product.name}", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(assign_window, text=f"Total Quantity: {product.quantity}").pack(pady=5)
        
        # Create scrollable frame for location assignments
        main_frame = ttk.Frame(assign_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas for scrolling
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Remaining quantity display
        remaining_var = tk.IntVar(value=product.quantity)
        
        def update_remaining(event=None):
            """Update the remaining quantity based on current assignments."""
            assigned = sum(int(qty_vars[i].get()) if qty_vars[i].get().isdigit() else 0 
                           for i in range(len(qty_vars)))
            remaining = max(0, product.quantity - assigned)
            remaining_var.set(remaining)
            remaining_label.config(text=f"Remaining Quantity: {remaining}")
        
        # Create location entries
        location_labels = []
        qty_vars = []
        qty_entries = []
        
        row = 0
        for r in range(self.warehouse.rows):
            for c in range(self.warehouse.cols):
                location = self.warehouse.grid[r][c]
                available = location.get_available_capacity()
                
                if available > 0:
                    # Container frame for this location
                    loc_frame = ttk.Frame(scrollable_frame)
                    loc_frame.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
                    
                    # Location info
                    loc_label = ttk.Label(loc_frame, text=f"{location.get_location_code()} (Available: {available})")
                    loc_label.pack(side=tk.LEFT, padx=5)
                    location_labels.append(loc_label)
                    
                    # Quantity entry
                    qty_var = tk.StringVar(value="0")
                    qty_vars.append(qty_var)
                    
                    qty_entry = ttk.Spinbox(loc_frame, from_=0, to=min(available, product.quantity), 
                                          textvariable=qty_var, width=10)
                    qty_entry.pack(side=tk.RIGHT, padx=5)
                    qty_entries.append(qty_entry)
                    
                    # Bind changes to update remaining
                    qty_var.trace_add("write", update_remaining)
                    
                    row += 1
        
        # Display remaining quantity
        remaining_label = ttk.Label(assign_window, text=f"Remaining Quantity: {product.quantity}")
        remaining_label.pack(pady=5)
        
        # Action buttons
        btn_frame = ttk.Frame(assign_window)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)
        
        def assign_locations():
            """Handle the assignment action."""
            assigned = 0
            print(f"DEBUG: Manually assigning locations for {sku}")
            
            # Store product at each selected location
            for i in range(len(qty_vars)):
                try:
                    qty = int(qty_vars[i].get())
                    if qty > 0:
                        # Get location coordinates from label text
                        loc_code = location_labels[i].cget("text").split()[0]
                        row = ord(loc_code[0]) - 65
                        col = int(loc_code[1:]) - 1
                        
                        # Store at location
                        print(f"DEBUG: Storing {qty} of {sku} at {loc_code}")
                        if self.warehouse.store_product(sku, qty, row, col):
                            assigned += qty
                            print(f"DEBUG: Successfully stored {qty} units at {loc_code}")
                        else:
                            print(f"DEBUG: Failed to store at {loc_code}")
                except (ValueError, IndexError) as e:
                    print(f"DEBUG: Error processing location {i}: {e}")
            
            # Check if all quantity was assigned
            product = self.warehouse.products[sku]
            total_assigned = assigned
            if assigned < product.quantity:
                # Update product quantity to match what was assigned
                delta = assigned - product.quantity
                print(f"DEBUG: Updating product quantity from {product.quantity} to {assigned} (delta: {delta})")
                product.update_quantity(delta)
                messagebox.showinfo("Partial Assignment", 
                    f"Only {assigned} of {product.quantity} units were assigned to locations. Product quantity has been updated.")
            
            # Save changes
            self.warehouse.data_storage.save_products(self.warehouse.products)
            self.warehouse.data_storage.save_locations(self.warehouse.grid)
            
            # Log the action
            self.warehouse.data_storage.save_log(self.warehouse.user,
                f"Manually assigned {total_assigned} units of {sku} to locations")
            
            # Close dialog and refresh
            print(f"DEBUG: Assignment complete, refreshing views")
            assign_window.destroy()
            self.refresh_product_list()
            self.refresh_warehouse_callback()
            self.show_product_details_by_sku(sku)
        
        ttk.Button(btn_frame, text="Assign Locations", command=assign_locations).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=assign_window.destroy).pack(side=tk.RIGHT, padx=5)
    
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
        ttk.Button(action_frame, text="Delete Product", 
                  command=lambda: self.delete_product_action(sku)).pack(side=tk.LEFT, padx=5)
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
        
        # log update
        self.warehouse.data_storage.save_log(self.warehouse.user,
            f"Updated product {sku}")
        self.show_message("Product updated successfully.")
        self.refresh_product_list()
        self.show_product_details_by_sku(sku)
    
    def delete_product_action(self, sku):
        """Handle product deletion with confirmation."""
        if messagebox.askyesno("Confirm Delete", 
                f"Are you sure you want to delete product {sku}? This cannot be undone."):
            if self.warehouse.delete_product(sku):
                self.show_message(f"Product {sku} deleted successfully.")
                self.refresh_product_list()
                self.refresh_warehouse_callback()
                self.setup_right_panel()
            else:
                messagebox.showerror("Error", "Failed to delete product.")
