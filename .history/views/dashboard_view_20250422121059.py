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
        
        # Add legend labels for grid symbols/colors
        ttk.Label(legend_frame, text="Legend:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Label(legend_frame, text="□ Empty", background="white").pack(side=tk.LEFT, padx=5)
        ttk.Label(legend_frame, text="▲ <50% Full", background="light green").pack(side=tk.LEFT, padx=5)
        ttk.Label(legend_frame, text="■ <100% Full", background="sky blue").pack(side=tk.LEFT, padx=5)
        ttk.Label(legend_frame, text="▓ Full", background="orange red").pack(side=tk.LEFT, padx=5)
        
        # Setup right panel - initially with instructions
        self.setup_detail_panel()
        
        # Notification section for mismatched quantities
        self.notification_frame = ttk.LabelFrame(self.right_panel, text="Notifications")
        self.notification_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.refresh_notifications()
        
        # Draw initial warehouse view
        self.draw_warehouse()
        
    def setup_detail_panel(self):
        """Set up the right panel for details and actions."""
        # Clear existing widgets in the right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        # Setup initial state with instructions
        ttk.Label(self.right_panel, text="Location Details", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(self.right_panel, text="Click on a location to view details").pack(pady=20)
        
    def draw_warehouse(self):
        """Draw the warehouse grid visualization."""
        # Clear existing widgets in the warehouse frame
        for widget in self.warehouse_frame.winfo_children():
            widget.destroy()
        
        # Reset active cells dictionary
        self.active_cells = {}
            
        # Create grid labels (column headers)
        ttk.Label(self.warehouse_frame, text="").grid(row=0, column=0)
        for c in range(self.warehouse.cols):
            ttk.Label(self.warehouse_frame, text=f"{c+1}", font=("Arial", 10, "bold")).grid(row=0, column=c+1, padx=2, pady=2)
            
        # Create cells for the warehouse grid
        for r in range(self.warehouse.rows):
            row_label = chr(65 + r)
            ttk.Label(self.warehouse_frame, text=row_label, font=("Arial", 10, "bold")).grid(row=r+1, column=0, padx=2, pady=2)
            
            for c in range(self.warehouse.cols):
                location = self.warehouse.grid[r][c]
                
                # Determine color and symbol based on fill level
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
                
                # Store cell reference with its coordinates for event handling
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
        # Log dashboard click
        loc = self.warehouse.grid[row][col].get_location_code()
        self.warehouse.data_storage.save_log(self.warehouse.user,
            f"Dashboard clicked location {loc}")
        
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
            # Create scrollable list for products at this location
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
        
        # Action buttons for storing/retrieving products
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
        
        # Create form for product selection and quantity
        form_frame = ttk.Frame(self.right_panel)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Product selection dropdown
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
        
        # Action buttons for store/cancel
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
        
        # Create form for product selection and quantity
        form_frame = ttk.Frame(self.right_panel)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Product selection dropdown
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
        
        # Action buttons for retrieve/cancel
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
    
    def refresh_notifications(self):
        """Refresh the notification section with flagged issues."""
        # Clear previous notification widgets
        for widget in self.notification_frame.winfo_children():
            widget.destroy()
        
        mismatched_skus = self.warehouse.validate_quantities()
        if mismatched_skus:
            # Show warning for mismatched quantities
            ttk.Label(self.notification_frame, text="⚠️ Mismatched Quantities Detected:", foreground="red").pack(anchor=tk.W, padx=10, pady=5)
            for sku in mismatched_skus:
                product = self.warehouse.products[sku]
                ttk.Label(self.notification_frame, text=f"- {product.name} (SKU: {sku})", foreground="red").pack(anchor=tk.W, padx=20)
            
            # Add Fix button
            ttk.Button(self.notification_frame, text="Fix Issues", command=self.fix_mismatched_quantities).pack(anchor=tk.W, padx=10, pady=10)
        else:
            ttk.Label(self.notification_frame, text="✅ All quantities are accounted for.", foreground="green").pack(anchor=tk.W, padx=10, pady=5)

    def fix_mismatched_quantities(self):
        """Automatically handle mismatched quantities and inform the user."""
        mismatched_skus = self.warehouse.validate_quantities()
        fix_report = []

        for sku in mismatched_skus:
            product = self.warehouse.products[sku]
            total_in_warehouse = sum(
                location.inventory.get(sku, 0) for row in self.warehouse.grid for location in row
            )
            
            if total_in_warehouse > product.quantity:
                # Excess quantity detected
                excess_quantity = total_in_warehouse - product.quantity
                self.handle_excess_quantity(product, total_in_warehouse, excess_quantity, fix_report)
            else:
                # Distribute missing quantities
                quantity_to_distribute = product.quantity - total_in_warehouse
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
                                f"Moved {quantity_to_store} units of {product.name} (SKU: {sku}) to Location {location.get_location_code()} "
                                f"due to available space."
                            )
                if quantity_to_distribute > 0:
                    fix_report.append(
                        f"⚠️ Unable to fully distribute {quantity_to_distribute} units of {product.name} (SKU: {sku}) due to insufficient space."
                    )
                # Save updated location data
                self.warehouse.data_storage.save_locations(self.warehouse.grid)
        
        # Display the fix report
        self.show_fix_report(fix_report)
        self.refresh_notifications()
        self.refresh_warehouse_view()

    def handle_excess_quantity(self, product, total_in_warehouse, excess_quantity, fix_report):
        """Handle excess quantities for a product."""
        def update_product_quantity():
            """Update the product's total quantity to match the warehouse."""
            product.update_quantity(excess_quantity)
            fix_report.append(
                f"Updated product quantity for {product.name} (SKU: {product.sku}) to match the warehouse: {total_in_warehouse}."
            )
            self.update_fix_report_live(fix_report[-1])  # Update fix report live
            # Save updated product data
            self.warehouse.data_storage.save_products(self.warehouse.products)
            self.refresh_notifications()
            self.refresh_warehouse_view()

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
                        fix_report.append(
                            f"Removed {qty_to_remove} units of {product.name} (SKU: {product.sku}) from Location {location.get_location_code()}."
                        )
                        self.update_fix_report_live(fix_report[-1])  # Update fix report live
            self.warehouse._rebuild_location_cache()
            # Save updated location data
            self.warehouse.data_storage.save_locations(self.warehouse.grid)
            self.refresh_notifications()
            self.refresh_warehouse_view()

        # Prompt user for action to resolve excess
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

    def show_fix_report(self, report):
        """Display the fix report in a popup dialog."""
        self.report_window = tk.Toplevel(self.parent)
        self.report_window.title("Fix Report")
        self.report_window.geometry("500x400")
        
        ttk.Label(self.report_window, text="Fix Report", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Scrollable text area for fix report
        self.text_area = tk.Text(self.report_window, wrap=tk.WORD, height=20)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for line in report:
            self.text_area.insert(tk.END, line + "\n")
        
        self.text_area.config(state=tk.DISABLED)  # Make the text area read-only
        
        ttk.Button(self.report_window, text="Close", command=self.report_window.destroy).pack(pady=10)

    def update_fix_report_live(self, new_entry):
        """Update the fix report live by appending a new entry."""
        if hasattr(self, 'text_area') and self.text_area.winfo_exists():
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, new_entry + "\n")
            self.text_area.config(state=tk.DISABLED)
    
    def refresh_warehouse_view(self):
        """Refresh the warehouse grid visualization and notifications."""
        self.draw_warehouse()
        self.refresh_notifications()
