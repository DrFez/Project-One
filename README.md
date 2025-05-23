# Warehouse Inventory Management System

This system provides a comprehensive solution for managing warehouse inventory with a visual 2D grid representation of storage locations. It allows users to add, update, and track products across warehouse locations through an intuitive graphical user interface.

## Student Information

👨‍💻 **Student:**         		Colin Ferreira  
📧 **Contact:**               	colin.ferreira@student.gsg.wa.edu.au  
🗓️ **Last Updated:**         	02 May 2025

## Requirements

- Python 3.6 or higher
- Tkinter (included in standard Python installation)
- A markdown viewer for viewing report files (not needed if viewing on GitHub)

## Installation & Setup

1. **Clone the repository**
   ```
   git clone https://github.com/DrFez/Project-One.git
   ```

2. **Navigate to the project directory**
   ```
   cd Project-One
   ```

3. **Verify Python installation**
   ```
   python --version
   ```
   Ensure the version is 3.6 or higher

## Running the Program

1. **Launch the application**
   ```
   python main.py
   ```

2. **Login Process**
   - Enter your username when prompted (for logging purposes)
   - The main warehouse management interface will appear (you may have to open it to view from your taskbar)

3. **Using the Interface**
   - **Dashboard Tab**: View warehouse visualization and interact with locations
   - **Products Tab**: Manage products (add, edit, delete)
   - **Logs**: Access logs through the Logs menu in the top menu bar

## Project Documentation

### Report Location
All project documentation is located in the `/report` folder:

- **Part A - Analysis**: `PartA_Analysis.md` - Project analysis and planning
- **Part B - Design**: `PartB_Design.md` - System design and architecture
- **Part C - Development**: `PartC_Development.md` - Development process and testing
- **Part D - Evaluation**: `PartD_Evaluation.md` - Project evaluation and reflection
- **Gantt Chart**: `gantt_chart.xlsx` - Project timeline and planning

### Viewing Markdown Files
The easiest way to view the markdown (.md) files is directly in the GitHub repository:

1. **Using GitHub (Recommended)**:
   - Browse to https://github.com/DrFez/Project-One
   - Navigate to the `/report` folder
   - Click on any .md file to view it rendered with formatting

2. **Using Visual Studio Code**:
   - Open VS Code after cloning the repository
   - Install the "Markdown Preview Enhanced" or "Markdown All in One" extension
   - Open any .md file
   - Press Ctrl+Shift+V (or ⌘+Shift+V on Mac) or click the preview button in the top-right corner

3. **Using a Markdown Editor**:
   - Applications like Typora, Marked 2, or MacDown can open and render markdown files

## Features

- **Product Management**: Add, edit, and delete products with details like name, SKU, price, and quantity
- **Warehouse Visualization**: Interactive 2D grid showing location fill levels
- **Location Management**: Store and retrieve products at specific warehouse coordinates
- **Search Functionality**: Find products by SKU or name
- **Quantity Validation**: Automatic detection and resolution of quantity mismatches
- **Data Persistence**: Automatic saving of inventory data to CSV files
- **Activity Logging**: Comprehensive logging of all user actions
- **Visual Debugging**: Color-coded console output for development and troubleshooting

## Troubleshooting

- **Program doesn't start**: Ensure Python 3.6+ is installed and in your PATH
- **GUI doesn't appear**: Verify Tkinter is available (run `python -m tkinter` to test)
- **Data doesn't save**: Check write permissions in the application folder
- **Warehouse doesn't load**: Ensure the data files in the `/data` folder haven't been corrupted

## License

>
> This project was created for educational purposes as part of an assessment. 
> Unauthorized copying, distribution, or use of this code outside of its 
> educational context is prohibited without express permission from the author.
>
> ***© Colin Ferreira 2025. All rights reserved.***
