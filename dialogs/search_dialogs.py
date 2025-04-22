import tkinter as tk
from tkinter import ttk, messagebox

class SearchProductDialog:
    """Dialog for searching for a product in the warehouse."""
    
    def __init__(self, parent, warehouse):
        """Initialize the search product dialog."""
        self.parent = parent
        self.warehouse = warehouse
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Search Product")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the dialog widgets."""
        ttk.Label(self.dialog, text="Search Product in Warehouse", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Search frame
        search_frame = ttk.Frame(self.dialog)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(search_frame, text="Enter SKU or select from list:").pack(anchor=tk.W)
        
        # Product selection
        self.product_var = tk.StringVar()
        product_dropdown = ttk.Combobox(search_frame, textvariable=self.product_var, width=30)
        product_dropdown['values'] = [f"{p.name} ({p.sku})" for p in self.warehouse.products.values()]
        product_dropdown.pack(pady=5, fill=tk.X)
        
        # Alternative: direct SKU entry
        ttk.Label(search_frame, text="OR enter SKU directly:").pack(anchor=tk.W, pady=(10, 0))
        self.sku_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.sku_var, width=30).pack(pady=5, fill=tk.X)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.dialog, text="Search Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollable results
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(results_frame, height=10, yscrollcommand=scrollbar.set)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.results_text.yview)
        
        # Action buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, pady=10, padx=20)
        
        ttk.Button(btn_frame, text="Search", command=self.search_action).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Close", command=self.dialog.destroy).pack(side=tk.RIGHT)
        
    def search_action(self):
        """Handle the search product action."""
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Get SKU either from dropdown or direct entry
        sku = ""
        if self.product_var.get():
            sku = self.product_var.get().split("(")[1].split(")")[0]
        elif self.sku_var.get():
            sku = self.sku_var.get().strip()
            
        if not sku:
            messagebox.showwarning("Input Error", "Please select a product or enter an SKU.")
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


class ViewLocationDialog:
    """Dialog for viewing details of a specific location."""
    
    def __init__(self, parent, warehouse):
        """Initialize the view location dialog."""
        self.parent = parent
        self.warehouse = warehouse
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("View Location")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the dialog widgets."""
        ttk.Label(self.dialog, text="View Warehouse Location", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Location selection
        location_frame = ttk.Frame(self.dialog)
        location_frame.pack(fill=tk.X, padx=20, pady=10)
        
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
        
        # Info display area
        info_frame = ttk.LabelFrame(self.dialog, text="Location Information")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.info_text = tk.Text(info_frame, height=10)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Update information when location is selected
        def update_info(*args):
            self.info_text.delete(1.0, tk.END)
            
            if not self.row_var.get() or not self.col_var.get():
                return
                
            try:
                row = ord(self.row_var.get()) - 65
                col = int(self.col_var.get()) - 1
                
                if row < 0 or row >= self.warehouse.rows or col < 0 or col >= self.warehouse.cols:
                    self.info_text.insert(tk.END, "Invalid location.")
                    return
                    
                location = self.warehouse.grid[row][col]
                self.info_text.insert(tk.END, f"Location: {location.get_location_code()}\n")
                self.info_text.insert(tk.END, f"Capacity: {location.capacity} units\n")
                self.info_text.insert(tk.END, f"Current usage: {location.current_stock} units\n")
                self.info_text.insert(tk.END, f"Available space: {location.get_available_capacity()} units\n\n")
                
                if location.inventory:
                    self.info_text.insert(tk.END, "Products stored at this location:\n")
                    for sku, qty in location.inventory.items():
                        if sku in self.warehouse.products:
                            product_name = self.warehouse.products[sku].name
                            self.info_text.insert(tk.END, f"- {product_name} ({sku}): {qty} units\n")
                else:
                    self.info_text.insert(tk.END, "This location is empty.")
            except:
                self.info_text.insert(tk.END, "Please select a valid location.")
        
        self.row_var.trace("w", update_info)
        self.col_var.trace("w", update_info)
        
        # Action buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, pady=10, padx=20)
        
        ttk.Button(btn_frame, text="Close", command=self.dialog.destroy).pack(side=tk.RIGHT)
