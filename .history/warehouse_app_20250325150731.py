import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from warehouse import Warehouse
from views.dashboard_view import DashboardView
from views.product_view import ProductView
from views.storage_view import StorageView
from dialogs.settings_dialog import SettingsDialog

class WarehouseApp:
    """Main application class for the Warehouse Inventory Management System GUI."""
    
    def __init__(self, root):
        """Initialize the application with the root window."""
        self.root = root
        self.root.title("Warehouse Inventory Management System")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        
        # Setup warehouse using settings
        self.setup_warehouse()
        
        # Create main interface
        self.create_widgets()
        
        # Set up window close event handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set up auto-save timer (every 5 minutes)
        self._setup_auto_save()
        
        # Center the application window on the screen
        self.center_window()
        
    def center_window(self):
        """Center the application window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def _setup_auto_save(self):
        """Setup periodic auto-save to prevent data loss without hurting performance."""
        def auto_save():
            self.warehouse.save_data(force=True)
            # Re-schedule auto-save every 5 minutes (300000 ms)
            self.root.after(300000, auto_save)
        
        # Initial scheduling
        self.root.after(300000, auto_save)
        
    def setup_warehouse(self):
        """Set up the warehouse using saved dimensions or prompt on first run."""
        # Create a temporary data storage to load settings
        from data_storage import DataStorage
        data_storage = DataStorage()
        
        # Load settings
        settings = data_storage.load_settings()
        
        # Check if this is the first run
        if settings["first_run"]:
            # Prompt for warehouse dimensions
            rows = simpledialog.askinteger(
                "Warehouse Setup", 
                "Enter number of rows (1-26):", 
                minvalue=1, maxvalue=26, 
                initialvalue=settings["warehouse_rows"]
            )
            
            if not rows:  # User cancelled, use default
                rows = settings["warehouse_rows"]
                
            cols = simpledialog.askinteger(
                "Warehouse Setup", 
                "Enter number of columns (1-99):", 
                minvalue=1, maxvalue=99, 
                initialvalue=settings["warehouse_cols"]
            )
            
            if not cols:  # User cancelled, use default
                cols = settings["warehouse_cols"]
                
            # Update settings
            settings["warehouse_rows"] = rows
            settings["warehouse_cols"] = cols
            settings["first_run"] = False
            
            # Save settings
            data_storage.save_settings(settings)
        else:
            rows = settings["warehouse_rows"]
            cols = settings["warehouse_cols"]
            
        # Create the warehouse with the dimensions from settings
        self.warehouse = Warehouse(rows, cols)
        
        # Try to load previously saved data
        if self.warehouse.load_data():
            messagebox.showinfo("Data Loaded", "Previous warehouse data has been loaded successfully.")
        
    def create_widgets(self):
        """Create all the widgets for the main interface."""
        # Create menu bar
        self.create_menu()
        
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
    
    def create_menu(self):
        """Create the application menu bar."""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Data", command=lambda: self.warehouse.save_data(force=True))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Warehouse Configuration", command=self.open_settings)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def open_settings(self):
        """Open the settings dialog."""
        dialog = SettingsDialog(self.root, self.warehouse)
        
        # If settings were changed, prompt for restart
        if dialog.settings_changed:
            if messagebox.askyesno("Settings Changed", 
                "Warehouse dimensions have been changed. These changes will take effect after restarting the application. Would you like to restart now?"):
                self.on_closing(restart=True)
    
    def show_about(self):
        """Show information about the application."""
        about_window = tk.Toplevel(self.root)
        about_window.title("About Warehouse Inventory System")
        about_window.geometry("400x300")
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Center the window
        about_window.update_idletasks()
        width = about_window.winfo_width()
        height = about_window.winfo_height()
        x = (about_window.winfo_screenwidth() // 2) - (width // 2)
        y = (about_window.winfo_screenheight() // 2) - (height // 2)
        about_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Add content
        ttk.Label(about_window, text="Warehouse Inventory Management System", 
                 font=("Arial", 14, "bold")).pack(pady=20)
        ttk.Label(about_window, text="Version 1.0").pack(pady=5)
        ttk.Label(about_window, text="© 2023 Great Southern Grammar").pack(pady=5)
        
        ttk.Label(about_window, text="\nA modular inventory management system demonstrating\n" +
                                    "object-oriented programming principles.").pack(pady=10)
                                    
        ttk.Button(about_window, text="Close", command=about_window.destroy).pack(pady=20)
        
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
        
    def on_closing(self, restart=False):
        """Handle window closing event - save data before exit."""
        # Save the current warehouse state
        self.warehouse.save_data(force=True)
        messagebox.showinfo("Data Saved", "Warehouse data has been saved successfully.")
        
        self.root.destroy()
        
        # If restarting, relaunch the application
        if restart:
            import os
            import sys
            python = sys.executable
            os.execl(python, python, *sys.argv)
