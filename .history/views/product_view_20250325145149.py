import tkinter as tk
from tkinter import ttk
from dialogs.product_dialogs import AddProductDialog, EditProductDialog

class ProductView:
    """View class for the products management tab."""
    
    def __init__(self, parent, warehouse, refresh_warehouse_callback):
        """Initialize the products view."""
        self.parent = parent
        self.warehouse = warehouse
        self.refresh_warehouse_callback = refresh_warehouse_callback
        self.setup_products_tab()
        
    def setup_products_tab(self):
        """Set up the products management tab."""
        # Frame for controls
        control_frame = ttk.Frame(self.parent)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        ttk.Label(control_frame, text="Product Management", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=10)
        ttk.Button(control_frame, text="Add New Product", 
                   command=self.add_product_dialog).pack(side=tk.RIGHT, padx=10)
        
        # Frame for product list
        self.product_list_frame = ttk.Frame(self.parent)
        self.product_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tree view for products
        self.setup_product_treeview()
    
    def setup_product_treeview(self):
        """Set up the treeview for product listing."""
        # Clear existing widgets
        for widget in self.product_list_frame.winfo_children():
            widget.destroy()
            
        # Create scrollbar
        scrollbar = ttk.Scrollbar(self.product_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        columns = ("name", "sku", "price", "quantity")
        self.product_tree = ttk.Treeview(self.product_list_frame, columns=columns, show="headings", 
                                          yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.product_tree.yview)
        
        # Define headings
        self.product_tree.heading("name", text="Product Name")
        self.product_tree.heading("sku", text="SKU")
        self.product_tree.heading("price", text="Price")
        self.product_tree.heading("quantity", text="Quantity")
        
        # Define columns
        self.product_tree.column("name", width=200)
        self.product_tree.column("sku", width=100)
        self.product_tree.column("price", width=100)
        self.product_tree.column("quantity", width=100)
        
        # Populate with products
        self.refresh_product_list()
        
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click event to edit product
        self.product_tree.bind("<Double-1>", self.edit_product_dialog)
    
    def refresh_product_list(self):
        """Refresh the product list in the treeview."""
        # Clear existing items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
            
        # Add all products
        for product in self.warehouse.products.values():
            self.product_tree.insert("", tk.END, values=(
                product.name, 
                product.sku, 
                f"${product.price:.2f}", 
                product.quantity
            ))
    
    def add_product_dialog(self):
        """Open dialog to add a new product."""
        dialog = AddProductDialog(
            self.parent.winfo_toplevel(), 
            self.warehouse, 
            self.refresh_product_list
        )
    
    def edit_product_dialog(self, event):
        """Open dialog to edit an existing product."""
        # Get selected item
        selected_item = self.product_tree.focus()
        if not selected_item:
            return
            
        # Get item data
        item_data = self.product_tree.item(selected_item, "values")
        if not item_data:
            return
            
        sku = item_data[1]
        if sku not in self.warehouse.products:
            return
            
        dialog = EditProductDialog(
            self.parent.winfo_toplevel(), 
            self.warehouse, 
            sku, 
            self.refresh_product_list
        )
