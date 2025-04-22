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
        
    def on_closing(self):
        """Handle window closing event - save data before exit."""
        # Save the current warehouse state
        self.warehouse.save_data()
        messagebox.showinfo("Data Saved", "Warehouse data has been saved successfully.")
        self.root.destroy()
