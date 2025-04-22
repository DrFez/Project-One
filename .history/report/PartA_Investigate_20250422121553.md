# Part A: Investigate

## Program Description

For this project, I set out to build an Inventory Management System that uses a 2D array to visualize a warehouse. I wanted to make something that would actually help me (or anyone else) keep track of products, where they're stored, and how much stock is available. I wrote the system in Python and made sure it had a graphical user interface (GUI) that would be intuitive and easy to use.

The main idea is that every product has a name, SKU, price, and quantity, and every location in the warehouse is represented as a cell in a grid. I can add, edit, and remove products, and then store or retrieve them from specific locations. The GUI makes it easy to see the whole warehouse at a glance, allowing users to quickly identify which areas are full, empty, or partially filled.

## Requirements

Here’s what I needed my system to do (and what I actually implemented):

- Let me add, edit, and remove products, each with a name, SKU, price, and quantity.
- Store and retrieve products in specific warehouse locations, each with a set capacity.
- Show the warehouse as a 2D grid, so I can see which locations are full, empty, or partially filled.
- Provide a GUI (for visual management) with an intuitive interface making it easy to visualize the warehouse layout and perform all inventory operations.
- Save and load all product and location data using CSV files, so nothing is lost between sessions.
- Log all user actions for traceability (e.g., adding products, storing, retrieving).
- Validate all user input and handle errors gracefully (like trying to store too many items in one location).
- Use Git for version control, with clear commit messages and branches for different features.

## Gantt Chart
## Gantt Chart

I carefully planned my development schedule over five weeks, breaking down each feature and component to ensure timely completion:

| Task | Week 1 | Week 2 | Week 3 | Week 4 | Week 5 |
|------|--------|--------|--------|--------|--------|
| **Requirements Analysis** |||||
| - User needs assessment | 🔵🔵🔵 |  |  |  |  |
| - Feature prioritization | 🔵🔵🔵 |  |  |  |  |
| - System constraints definition | 🔵🔵🔵 |  |  |  |  |
| **Design** |||||
| - Class hierarchy planning | 🟢🟢 | 🟢🟢 |  |  |  |
| - Database schema design | 🟢🟢 | 🟢🟢 |  |  |  |
| - UI wireframing |  | 🟢🟢🟢🟢 |  |  |  |
| - API endpoints planning |  | 🟢🟢🟢🟢 |  |  |  |
| **Core Development** |||||
| - Product class implementation |  | 🟡🟡🟡🟡 |  |  |  |
| - Location class implementation |  | 🟡🟡🟡🟡 |  |  |  |
| - Warehouse class implementation |  | 🟡🟡 | 🟡🟡 |  |  |
| - Data persistence layer |  |  | 🟡🟡🟡🟡 |  |  |
| **Visualization** |||||
| - 2D grid representation |  |  | 🟣🟣🟣🟣 |  |  |
| - Status indicators for locations |  |  | 🟣🟣🟣🟣 |  |  |
| - Dynamic updates |  |  | 🟣🟣🟣🟣 |  |  |
| **UI & Features** |||||
| - Product management interface |  |  | 🟠🟠 | 🟠🟠 |  |
| - Location management interface |  |  | 🟠🟠 | 🟠🟠 |  |
| - Search functionality |  |  |  | 🟠🟠🟠🟠 |  |
| - Reporting capabilities |  |  |  | 🟠🟠🟠🟠 |  |
| - CSV import/export |  |  |  | 🟠🟠🟠🟠 |  |
| **Testing & Debugging** |||||
| - Unit testing |  |  |  | 🔴🔴 | 🔴🔴 |
| - Integration testing |  |  |  | 🔴🔴 | 🔴🔴 |
| - Error handling implementation |  |  |  | 🔴🔴 | 🔴🔴 |
| - Performance optimization |  |  |  |  | 🔴🔴🔴🔴 |
| **Evaluation & Documentation** |||||
| - User acceptance testing |  |  |  |  | ⚪⚪⚪⚪ |
| - Documentation finalization |  |  |  |  | ⚪⚪⚪⚪ |
| - Code review and refactoring |  |  |  |  | ⚪⚪⚪⚪ |

This detailed breakdown helped me track progress and ensure each component received appropriate attention throughout the development lifecycle.

## How OOP Helped My Design

I used object-oriented programming (OOP) throughout the project, and it made a huge difference in how organized and maintainable my code is:

- **Encapsulation:** Each class (Product, Location, Warehouse) keeps its own data and methods. For example, the Product class only deals with product details, and the Location class only manages what’s stored at a specific spot in the warehouse.
- **Inheritance:** While I haven’t made subclasses yet, my design means I could easily add new types of products or locations in the future by extending the base classes.
- **Polymorphism:** Methods like `add_product` and `store_product` work with different objects, so I can reuse code and keep things flexible.
- **Abstraction:** The user doesn’t need to know how the data is stored or how the grid is managed—they just use the interface. All the complexity is hidden inside the classes.
- **Low Coupling, High Cohesion:** Each class has a clear job, and they don’t depend on each other more than necessary. This makes it easier to fix bugs or add new features without breaking everything else.

Overall, OOP let me break the project into manageable pieces, made the code easier to test, and means I can add new features later without having to rewrite everything.
