import tkinter as tk
from tkinter import ttk, messagebox

class SettingsDialog:
    """Dialog for changing application settings."""
    
    def __init__(self, parent, warehouse):
        """Initialize the settings dialog."""
        self.parent = parent
        self.warehouse = warehouse
        self.data_storage = warehouse.data_storage
        self.settings_changed = False
        
        # Load current settings
        self.current_settings = self.data_storage.load_settings()
        
        # Create the dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Warehouse Configuration")
        self.dialog.geometry("450x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Create dialog content
        self.create_widgets()
        
        # Wait for the dialog to close
        self.dialog.wait_window()
    
    def center_dialog(self):
        """Center the dialog on the parent window."""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        
        # Get parent's center position
        parent_x = self.parent.winfo_x() + (self.parent.winfo_width() // 2)
        parent_y = self.parent.winfo_y() + (self.parent.winfo_height() // 2)
        
        # Calculate dialog position
        x = parent_x - (width // 2)
        y = parent_y - (height // 2)
        
        # Ensure dialog is fully visible on screen
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        x = max(0, min(x, screen_width - width))
        y = max(0, min(y, screen_height - height))
        
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create the dialog widgets."""
        # Create main frame with padding
        main_frame = ttk.Frame(self.dialog, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Warehouse Configuration", 
                 font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Warehouse dimensions frame
        dimensions_frame = ttk.LabelFrame(main_frame, text="Warehouse Dimensions")
        dimensions_frame.pack(fill=tk.X, pady=10)
        
        # Grid for form layout
        grid_frame = ttk.Frame(dimensions_frame)
        grid_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Rows
        ttk.Label(grid_frame, text="Number of Rows:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.rows_var = tk.IntVar(value=self.current_settings["warehouse_rows"])
        rows_spinbox = ttk.Spinbox(grid_frame, from_=1, to=26, textvariable=self.rows_var, width=10)
        rows_spinbox.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(grid_frame, text="(1-26)").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Columns
        ttk.Label(grid_frame, text="Number of Columns:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.cols_var = tk.IntVar(value=self.current_settings["warehouse_cols"])
        cols_spinbox = ttk.Spinbox(grid_frame, from_=1, to=99, textvariable=self.cols_var, width=10)
        cols_spinbox.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(grid_frame, text="(1-99)").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Note about restart
        note_text = "Note: Changes to warehouse dimensions will require\nrestarting the application to take effect."
        ttk.Label(main_frame, text=note_text, foreground="gray").pack(pady=15)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Save", command=self.save_settings).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def save_settings(self):
        """Save the settings and close the dialog."""
        # Get values from form
        rows = self.rows_var.get()
        cols = self.cols_var.get()
        
        # Validate input
        if rows < 1 or rows > 26:
            messagebox.showwarning("Invalid Input", "Number of rows must be between 1 and 26.")
            return
            
        if cols < 1 or cols > 99:
            messagebox.showwarning("Invalid Input", "Number of columns must be between 1 and 99.")
            return
        
        # Check if settings have changed
        if (rows != self.current_settings["warehouse_rows"] or 
            cols != self.current_settings["warehouse_cols"]):
            
            # Update settings
            self.current_settings["warehouse_rows"] = rows
            self.current_settings["warehouse_cols"] = cols
            
            # Save settings
            if self.data_storage.save_settings(self.current_settings):
                self.settings_changed = True
                messagebox.showinfo("Settings Saved", 
                                    "Warehouse dimensions updated. The changes will take effect after restarting the application.")
            else:
                messagebox.showerror("Error", "Failed to save settings.")
        
        # Close the dialog
        self.dialog.destroy()
