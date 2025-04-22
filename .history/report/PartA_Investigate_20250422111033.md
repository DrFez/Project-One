# Part A: Investigate

## Program Description
This project is a warehouse management system with a graphical user interface (GUI) and command-line interface (CLI) built using Python. It allows users to manage products, locations, and inventory, supporting storage, retrieval, and search operations.

## Requirements
- User authentication (username input)
- Add, edit, and remove products
- Store and retrieve products in warehouse locations
- View warehouse layout and product locations
- Search for products and view details
- Log user actions
- Save/load data from CSV/JSON files

## Gantt Chart
| Task                | Week 1 | Week 2 | Week 3 | Week 4 |
|---------------------|--------|--------|--------|--------|
| Requirements        |   X    |        |        |        |
| Design              |        |   X    |        |        |
| Development         |        |   X    |   X    |        |
| Testing & Debugging |        |        |   X    |   X    |
| Evaluation          |        |        |        |   X    |

## OOP Characteristics in Design
- **Encapsulation:** Each class (Product, Location, Warehouse) manages its own data and methods.
- **Inheritance:** Base classes can be extended for specialized behavior if needed.
- **Polymorphism:** Methods like `add_product` or `store_product` can be used with different object types.
- **Abstraction:** The user interacts with high-level operations, not internal data structures.
