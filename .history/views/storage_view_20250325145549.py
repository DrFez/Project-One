import tkinter as tk
from tkinter import ttk
from dialogs.storage_dialogs import StoreProductDialog, RetrieveProductDialog
from dialogs.search_dialogs import SearchProductDialog, ViewLocationDialog

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
        # Left frame for operations
        operations_frame = ttk.LabelFrame(self.parent, text="Operations")
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
        map_frame = ttk.LabelFrame(self.parent, text="Warehouse Map")
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
                
                # Make cells clickable - using lambda to capture current values of r and c
                canvas.tag_bind(cell_id, "<Button-1>", 
                               lambda event, row=r, col=c: self.location_click(row, col))
    
    def location_click(self, row, col):
        """Handle click on a location cell in the mini-map."""
        from dialogs.location_dialogs import LocationDialog
        dialog = LocationDialog(
            self.parent.winfo_toplevel(), 
            self.warehouse, 
            row, 
            col, 
            self.refresh_callback
        )
        
    def refresh_callback(self):
        """Callback function to refresh all views."""
        self.refresh_warehouse_callback()
        self.draw_mini_map()
        self.refresh_product_callback()
    
    def store_product_operation(self):
        """Operation to store a product in the warehouse."""
        dialog = StoreProductDialog(
            self.parent.winfo_toplevel(), 
            self.warehouse, 
            self.refresh_callback
        )
    
    def retrieve_product_operation(self):
        """Operation to retrieve a product from the warehouse."""
        dialog = RetrieveProductDialog(
            self.parent.winfo_toplevel(), 
            self.warehouse, 
            self.refresh_callback
        )
    
    def search_product_operation(self):
        """Operation to search for a product in the warehouse."""
        dialog = SearchProductDialog(
            self.parent.winfo_toplevel(), 
            self.warehouse
        )
    
    def view_location_operation(self):
        """Operation to view details of a specific location."""
        dialog = ViewLocationDialog(
            self.parent.winfo_toplevel(), 
            self.warehouse
        )
