import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from warehouse import Warehouse
from views.dashboard_view import DashboardView
from views.product_view import ProductView
from views.storage_view import StorageView

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
        
        # Set up window close event handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set up auto-save timer (every 5 minutes)
        self._setup_auto_save()
        
    def _setup_auto_save(self):
        """Setup periodic auto-save to prevent data loss without hurting performance."""
        def auto_save():
            self.warehouse.save_data(force=True)
            # Re-schedule auto-save every 5 minutes (300000 ms)
            self.root.after(300000, auto_save)
        
        # Initial scheduling
        self.root.after(300000, auto_save)
        
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
        
        # Try to load previously saved data
        if self.warehouse.load_data():
            messagebox.showinfo("Data Loaded", "Previous warehouse data has been loaded successfully.")
        
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
        
        # Setup each tab with its view class
        self.dashboard_view = DashboardView(self.dashboard_frame, self.warehouse)
        self.product_view = ProductView(self.products_frame, self.warehouse, self.dashboard_view.refresh_warehouse_view)
        self.storage_view = StorageView(
            self.storage_frame, 
            self.warehouse, 
            self.dashboard_view.refresh_warehouse_view,
            self.product_view.refresh_product_list
        )
        
        # Set up tab change event to avoid unnecessary refreshes
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Store current tab
        self.current_tab = 0
        
    def on_tab_changed(self, event):
        """Handle tab changing to refresh only when needed."""
        selected_tab = self.notebook.index(self.notebook.select())
        previous_tab = self.current_tab
        self.current_tab = selected_tab
        
        # Only refresh the newly selected tab if needed
        if selected_tab == 0 and previous_tab != 0:  # Dashboard tab
            self.dashboard_view.refresh_warehouse_view()
        elif selected_tab == 1 and previous_tab != 1:  # Products tab
            self.product_view.refresh_product_list()
        elif selected_tab == 2 and previous_tab != 2:  # Storage tab
            self.storage_view.draw_mini_map()
        
    def on_closing(self):
        """Handle window closing event - save data before exit."""
        # Save the current warehouse state
        self.warehouse.save_data(force=True)
        messagebox.showinfo("Data Saved", "Warehouse data has been saved successfully.")
        self.root.destroy()
