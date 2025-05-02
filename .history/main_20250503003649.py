import tkinter as tk
import os
import platform
import time
import sys
from colorama import init, Fore, Style
from warehouse_app import WarehouseApp

def clear_console():
    """Clear the console screen."""
    os.system('cls' if platform.system() == "Windows" else 'clear')

def display_banner():
    """Display a styled banner for the warehouse application."""
    print(f"""
    {Fore.CYAN}╔════════════════════════════════════════════╗
    ║ {Fore.YELLOW}W A R E H O U S E   M A N A G E M E N T{Fore.CYAN}   ║
    ║ {Fore.YELLOW}         S Y S T E M        {Fore.CYAN}              ║
    ╚════════════════════════════════════════════╝{Style.RESET_ALL}
    """)

def main():
    """Main function to run the warehouse management application."""
    # Initialize colorama for cross-platform colored terminal output
    init(autoreset=True)
    
    # Clear the console
    clear_console()
    
    # Display banner
    display_banner()
    
    print(f"{Fore.GREEN}Welcome to the Warehouse Management System!")
    print(f"{Fore.YELLOW}Please log in to continue.\n")
    
    user = input(f"{Fore.CYAN}Enter username: {Style.RESET_ALL}").strip()
    
    print(f"\n{Fore.GREEN}Welcome, {Fore.YELLOW}{user}{Fore.GREEN}! Loading application...")
    time.sleep(1)  # Small delay for better user experience
    
    # Start the GUI application
    root = tk.Tk()
    app = WarehouseApp(root, user)
    root.mainloop()

if __name__ == "__main__":
    main()
