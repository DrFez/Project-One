import tkinter as tk
from warehouse_app import WarehouseApp

def main():
    """Main function to run the warehouse management application."""
    user = input("Enter username: ").strip()
    root = tk.Tk()
    app = WarehouseApp(root, user)
    root.mainloop()

if __name__ == "__main__":
    main()
