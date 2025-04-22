import tkinter as tk
from tkinter import ttk, messagebox
from dialogs.storage_dialogs import StoreLocationDialog, RetrieveLocationDialog

class LocationDialog:
    """Dialog for viewing and managing a specific location."""
    
    def __init__(self, parent, warehouse, row, col, refresh_callback):
        """Initialize the location dialog."""
        self.parent = parent
        self.warehouse = warehouse
        self.row = row
        self.col = col
        self.location = warehouse.grid[row][col]
        self.refresh_callback = refresh_callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Location {self.location.get_location_code()}")
        self.dialog.geometry("300x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the dialog widgets."""
        ttk.Label(self.dialog, text=f"Location {self.location.get_location_code()}", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(self.dialog, text=f"Capacity: {self.location.current_stock}/{self.location.capacity}").pack(pady=5)
        
        # List products at this location
        if self.location.inventory:
            ttk.Label(self.dialog, text="Products at this location:", font=("Arial", 10, "bold")).pack(pady=5)
            product_frame = ttk.Frame(self.dialog)
            product_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Create scrollable list
            scrollbar = ttk.Scrollbar(product_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            product_list = tk.Listbox(product_frame, yscrollcommand=scrollbar.set)
            product_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=product_list.yview)
            
            for sku, qty in self.location.inventory.items():
                if sku in self.warehouse.products:
                    product_name = self.warehouse.products[sku].name
                    product_list.insert(tk.END, f"{product_name} ({sku}): {qty}")
        else:
            ttk.Label(self.dialog, text="This location is empty").pack(pady=10)
            
        # Action buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Store Product", 
                   command=self.open_store_dialog).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Retrieve Product", 
                   command=self.open_retrieve_dialog).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Close", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=10)
        
    def open_store_dialog(self):
        """Open dialog to store product at this location."""
        self.dialog.destroy()
        dialog = StoreLocationDialog(
            self.parent, 
            self.warehouse, 
            self.row, 
            self.col, 
            self.refresh_callback
        )
        
    def open_retrieve_dialog(self):
        """Open dialog to retrieve product from this location."""
        if not self.location.inventory:
            messagebox.showinfo("Empty Location", "This location is empty.")
            return
            
        self.dialog.destroy()
        dialog = RetrieveLocationDialog(
            self.parent, 
            self.warehouse, 
            self.row, 
            self.col, 
            self.refresh_callback
        )
