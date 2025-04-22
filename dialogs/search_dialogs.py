import tkinter as tk
from tkinter import ttk

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
