import tkinter as tk
import os
import platform
import time
import sys
from warehouse_app import WarehouseApp

# Simple cross-platform color solution with no dependencies
class Colors:
    """Simple color codes that work on compatible terminals and degrade gracefully elsewhere."""
    # Check if the terminal likely supports ANSI colors
    _use_colors = platform.system() != "Windows" or "ANSICON" in os.environ
    
    # Define colors or empty strings if not supported
    CYAN = "\033[96m" if _use_colors else ""
    GREEN = "\033[92m" if _use_colors else ""
    YELLOW = "\033[93m" if _use_colors else ""
    RESET = "\033[0m" if _use_colors else ""

def clear_console():
    """Clear the console screen."""
    os.system('cls' if platform.system() == "Windows" else 'clear')

def display_banner():
    """Display a styled banner for the warehouse application."""
    print(f"""
    {Colors.CYAN}╔════════════════════════════════════════════╗
    ║   {Colors.YELLOW}W A R E H O U S E   M A N A G E M E N T {Colors.CYAN} ║
    ║ {Colors.YELLOW}            S Y S T E M             {Colors.CYAN}       ║
    ╚════════════════════════════════════════════╝{Colors.RESET}
    """)

def main():
    """Main function to run the warehouse management application."""
    # Clear the console
    clear_console()
    
    # Display banner
    display_banner()
    
    print(f"{Colors.GREEN}Welcome to the Warehouse Management System!")
    print(f"{Colors.YELLOW}Please log in to continue.\n")
    
    user = input(f"{Colors.CYAN}Enter username: {Colors.RESET}").strip()
    
    print(f"\n{Colors.GREEN}Welcome, {Colors.YELLOW}{user}{Colors.GREEN}! Loading application...")
    time.sleep(1)  # Small delay for better user experience
    
    # Start the GUI application
    root = tk.Tk()
    app = WarehouseApp(root, user)
    root.mainloop()

if __name__ == "__main__":
    main()
