import tkinter as tk
from tkinter import ttk, messagebox

class SettingsDialog:
    """Dialog for editing warehouse settings."""
    
    def __init__(self, parent, warehouse):
        """Initialize the settings dialog."""
        self.parent = parent
        self.warehouse = warehouse
        self.settings_changed = False
        
        # Create the dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Warehouse Configuration")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Load current settings
        self.current_settings = self.warehouse.data_storage.load_settings()
        
        # Create form for settings
        self.create_form()
        
        # Wait for the dialog to be closed
        self.parent.wait_window(self.dialog)
    
    def create_form(self):
        """Create the settings form."""
        # Header
        ttk.Label(self.dialog, text="Warehouse Configuration", 
                 font=("Arial", 14, "bold")).pack(pady=20)
        
        # Warehouse dimensions
        frame = ttk.Frame(self.dialog, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Row settings
        ttk.Label(frame, text="Number of Rows (1-26):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.rows_var = tk.IntVar(value=self.current_settings["warehouse_rows"])
        ttk.Spinbox(frame, from_=1, to=26, textvariable=self.rows_var, width=10).grid(row=0, column=1, pady=5)
        
        # Column settings
        ttk.Label(frame, text="Number of Columns (1-99):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cols_var = tk.IntVar(value=self.current_settings["warehouse_cols"])
        ttk.Spinbox(frame, from_=1, to=99, textvariable=self.cols_var, width=10).grid(row=1, column=1, pady=5)
        
        # Warning label
        ttk.Label(frame, text="Warning: Changing these settings will require a restart.",
                 foreground="red").grid(row=2, column=0, columnspan=2, pady=20)
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Save", command=self.save_settings).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=10)
    
    def save_settings(self):
        """Save the settings and close the dialog."""
        try:
            rows = self.rows_var.get()
            cols = self.cols_var.get()
            
            if rows < 1 or rows > 26 or cols < 1 or cols > 99:
                raise ValueError("Invalid dimensions")
                
            # Check if settings were changed
            if rows != self.current_settings["warehouse_rows"] or cols != self.current_settings["warehouse_cols"]:
                # Update settings
                self.current_settings["warehouse_rows"] = rows
                self.current_settings["warehouse_cols"] = cols
                
                # Save settings
                self.warehouse.data_storage.save_settings(self.current_settings)
                
                # Flag that settings were changed
                self.settings_changed = True
                
            # Close dialog
            self.dialog.destroy()
            
        except (ValueError, Exception) as e:
            messagebox.showerror("Error", "Please enter valid warehouse dimensions.")
