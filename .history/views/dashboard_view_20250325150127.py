import tkinter as tk
from tkinter import ttk
from dialogs.location_dialogs import LocationDialog
import time

class DashboardView:
    """View class for the dashboard tab with warehouse visualization."""
    
    def __init__(self, parent, warehouse):
        """Initialize the dashboard view."""
        self.parent = parent
        self.warehouse = warehouse
        self.setup_dashboard()
        self.last_hover_time = 0  # For throttling hover events
        self.hover_cooldown = 0.1  # Seconds between hover events
        self.active_cells = {}  # Store references to avoid garbage collection
        
    def setup_dashboard(self):
        """Set up the dashboard tab with warehouse visualization."""
        # Frame for controls
        control_frame = ttk.Frame(self.parent)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        ttk.Label(control_frame, text="Warehouse Layout", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=10)
        ttk.Button(control_frame, text="Refresh", command=self.refresh_warehouse_view).pack(side=tk.RIGHT, padx=10)
        
        # Frame for warehouse grid
        self.warehouse_frame = ttk.Frame(self.parent)
        self.warehouse_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Draw initial warehouse view
        self.draw_warehouse()
        
        # Legend for the warehouse grid
        legend_frame = ttk.Frame(self.parent)
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
                
                # Bind hover event to show location details - using a lambda that captures cell_id
                cell.bind("<Enter>", lambda event, id=cell_id: self.throttled_show_location_info(event, id))
                cell.bind("<Leave>", self.hide_location_info)
                
                # Bind click event to show location actions
                cell.bind("<Button-1>", lambda event, id=cell_id: self.location_click(id))
    
    def throttled_show_location_info(self, event, cell_id):
        """Throttle hover events to prevent performance issues."""
        current_time = time.time()
        if current_time - self.last_hover_time < self.hover_cooldown:
            return
            
        self.last_hover_time = current_time
        self.show_location_info(event, cell_id)
        
    def show_location_info(self, event, cell_id):
        """Show information about a location when hovering over it."""
        if cell_id not in self.active_cells:
            return
            
        cell_data = self.active_cells[cell_id]
        row, col = cell_data["row"], cell_data["col"]
        
        location = self.warehouse.grid[row][col]
        info = f"Location: {location.get_location_code()}\n"
        info += f"Usage: {location.current_stock}/{location.capacity}\n"
        
        if location.inventory:
            info += "Products:\n"
            # Limit to first 5 products to avoid performance issues with large inventories
            items = list(location.inventory.items())[:5]
            for sku, qty in items:
                if sku in self.warehouse.products:
                    product_name = self.warehouse.products[sku].name
                    info += f"- {product_name} ({sku}): {qty}\n"
            
            if len(location.inventory) > 5:
                info += f"... and {len(location.inventory) - 5} more products"
        else:
            info += "Empty location"
            
        # Show tooltip
        self.tooltip = tk.Toplevel(self.parent.winfo_toplevel())
        self.tooltip.wm_overrideredirect(True)
        
        # Get position from the event widget
        x = event.widget.winfo_rootx() + 25
        y = event.widget.winfo_rooty() + 25
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(self.tooltip, text=info, relief=tk.SOLID, background="#ffffe0", padding=5)
        label.pack()
        
    def hide_location_info(self, event):
        """Hide the location info tooltip."""
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()
            
    def location_click(self, cell_id):
        """Handle click on a location cell."""
        if cell_id not in self.active_cells:
            return
            
        cell_data = self.active_cells[cell_id]
        row, col = cell_data["row"], cell_data["col"]
        
        dialog = LocationDialog(self.parent.winfo_toplevel(), self.warehouse, row, col, self.refresh_warehouse_view)
        
    def refresh_warehouse_view(self):
        """Refresh the warehouse grid visualization."""
        self.draw_warehouse()
