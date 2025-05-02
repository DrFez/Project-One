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

I carefully planned my development schedule over five weeks, breaking down each feature and component to ensure timely completion:

The detailed breakdown helped me track progress and ensure each component received appropriate attention throughout the development lifecycle.
> The Gantt Chart can be found within this directory at: 
<span style="color:#1a0dab; text-decoration:underline;">report/Gantt_Chart.xlsx</span>


## How OOP Helped My Design

I implemented object-oriented programming (OOP) principles throughout the project, which significantly improved the organization, maintainability, and extensibility of my code:

- **Encapsulation:** 
  > "The bundling of data and methods that operate on that data within a single unit, and restricting access to some of the object's components."
  
  I used encapsulation in my Product class to protect critical inventory operations and ensure data integrity. This design choice prevented invalid quantity changes by exposing a controlled update_quantity() method instead of allowing direct manipulation:
  ```python
  # Product class encapsulates product data and operations
  class Product:
      def __init__(self, name, sku, price, quantity=0, warehouse=None):
          self.name = name
          self.sku = sku
          self.price = price
          self.quantity = quantity
      
      def update_quantity(self, amount):
          if self.quantity + amount < 0:
              return False
          self.quantity += amount
          return True
  ```

- **Inheritance:** 
  > "A mechanism where a new class inherits properties and behaviors from an existing class, promoting code reuse and establishing a relationship between parent and derived classes."
  
  I deliberately chose not to implement subclasses in the core system to avoid premature complexity, but I designed the Product class with inheritance in mind. This approach ensures that adding specialized product types in the future will require minimal code changes while preserving existing functionality:
  ```python
  # Future enhancement example:
  class PerishableProduct(Product):
      def __init__(self, name, sku, price, quantity, expiry_date):
          super().__init__(name, sku, price, quantity)
          self.expiry_date = expiry_date
          
      def is_expired(self, current_date):
          return current_date > self.expiry_date
  ```

- **Polymorphism:** 
  > "The ability of different classes to respond to the same method or function call in ways specific to their data type or class."
  
  My design uses polymorphism in the Warehouse class when handling different types of objects through common interfaces. This ensures that if I introduce specialized Product or Location subclasses in the future, existing methods will continue to work without requiring rewrites:
  ```python
  # The Warehouse class interacts with different objects polymorphically
  def store_product(self, sku, quantity, row, col):
      product = self.products[sku]     # Product object
      location = self.grid[row][col]   # Location object
      
      if not location.add_product(product, quantity):
          return False
      
      product.update_quantity(quantity)
      # ...
  ```

- **Abstraction:** 
  > "The concept of hiding complex implementation details while exposing only the necessary features of an object."
  
  In the Location class, abstraction allowed me to shield the complex inventory management logic from external classes. This meant the Warehouse class doesn't need to understand how capacity is calculated or how products are stored—it only needs to know that a location can store items:
  ```python
  # Location class abstracts storage management
  class Location:
      def add_product(self, product, quantity):
          if self.current_stock + quantity > self.capacity:
              return False
          # Complex inventory management hidden from users
          if product.sku in self.inventory:
              self.inventory[product.sku] += quantity
          else:
              self.inventory[product.sku] = quantity  
          self.current_stock += quantity
          return True
  ```

- **Low Coupling:** 
  > "A design principle that reduces the interdependence between components of a system, making it more maintainable and modular."
  
  I deliberately minimized dependencies between classes to make the system more maintainable. For example, the Product class functions independently and knows nothing about the Warehouse or Location classes. This means I can modify how products work without affecting storage logic, and vice versa:
  ```python
  # Warehouse manages the grid and product catalog
  # Location manages individual storage spaces
  # Product manages product-specific details
  
  # Example of low coupling through separate responsibilities
  def distribute_initial_quantity(self, product):
      for row in self.grid:
          for location in row:
              available_space = location.get_available_capacity()
              if available_space > 0:
                  quantity_to_store = min(quantity_to_distribute, available_space)
                  location.add_product(product, quantity_to_store)
  ```

- **High Cohesion:** 
  > "A measure of how strongly related and focused the responsibilities of a single component are, with highly cohesive modules performing a well-defined task."
  
  Each class in my system has a singular, well-defined purpose. The Location class focuses exclusively on managing storage capacity and item tracking at a specific position, while the Product class handles only product-specific attributes. This has made the codebase easier to understand and maintain since each component does one thing well:
  ```python
  # Location class example showing high cohesion
  class Location:
      def get_available_capacity(self):
          """Return the remaining capacity at this location."""
          return self.capacity - self.current_stock
      
      def get_location_code(self):
          """Return a string code representing this location."""
          return f"{chr(65 + self.row)}{self.col + 1}"
  ```

Overall, OOP principles allowed me to break this complex inventory system into manageable components, each with clear responsibilities. This approach has made the code easier to test and maintain, and provides a robust foundation for adding new features in the future, such as different product types or advanced warehouse visualization.
