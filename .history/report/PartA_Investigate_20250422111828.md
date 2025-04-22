# Part A: Investigate

## Program Description
The Inventory Management System with 2D Array Visualization is a modular, object-oriented Python application designed for advanced inventory control in a virtual warehouse. The system leverages OOP principles to model products, storage locations, and the warehouse as a whole, providing robust features for adding, removing, and tracking items. The 2D array visualization offers a clear, real-time representation of warehouse storage, supporting both business and educational objectives. The system is designed for extensibility, maintainability, and real-world relevance, with a focus on demonstrating expert-level OOP and software engineering practices.

## Requirements
- **Product Management:** Add, edit, remove products with attributes (name, SKU, price, quantity).
- **Location Management:** Define storage locations with coordinates, capacity, and inventory.
- **Warehouse Operations:** Store/retrieve products, optimize space, and visualize the warehouse as a 2D grid.
- **2D Array Visualization:** Print and display the warehouse grid, showing product distribution and capacity.
- **User Interface:** Command-line interface (CLI) for all operations, with clear prompts and error handling.
- **Data Persistence:** Save/load products and locations from CSV files; log all user actions.
- **Validation & Exception Handling:** Robust input validation and error management throughout.
- **Testing:** Use provided test data for comprehensive validation of all features.
- **Version Control:** Use Git for all development, with clear branching and commit strategies.

## Gantt Chart
![Gantt Chart](gantt_chart.png)

| Task                | Week 1 | Week 2 | Week 3 | Week 4 | Week 5 |
|---------------------|--------|--------|--------|--------|--------|
| Requirements        |   X    |        |        |        |        |
| Design              |   X    |   X    |        |        |        |
| Development         |        |   X    |   X    |        |        |
| Visualization       |        |        |   X    |        |        |
| UI & Features       |        |        |   X    |   X    |        |
| Testing & Debugging |        |        |        |   X    |   X    |
| Evaluation          |        |        |        |        |   X    |

## OOP Characteristics and Their Role in Design
- **Encapsulation:** Each class (Product, Location, Warehouse) manages its own state and exposes only necessary methods, ensuring data integrity and modularity.
- **Inheritance:** The design allows for future extension (e.g., specialized Product subclasses for perishable goods or electronics) by inheriting from base classes.
- **Polymorphism:** Methods such as `add_product` and `store_product` can operate on different subclasses, supporting flexible and reusable code.
- **Abstraction:** The system hides complex operations (e.g., storage optimization, data persistence) behind simple interfaces, making the codebase easier to use and maintain.
- **Cohesion & Coupling:** High cohesion within classes and low coupling between modules, supporting maintainability and scalability.
- **Responsibility-Driven Design:** Each class has a single, well-defined responsibility, following SOLID principles.

> This approach ensures the system is robust, extensible, and easy to maintain, while also providing a clear demonstration of advanced OOP concepts for educational and professional audiences.
