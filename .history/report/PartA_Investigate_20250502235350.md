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

- **Encapsulation:** Each class encapsulates its data and behavior, hiding implementation details and exposing only necessary interfaces:
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

- **Information Hiding:** I used private attributes and methods to protect internal data and operations from external interference:
  ```python
  class Warehouse:
      def __init__(self, rows, cols):
          self.grid = [[Location(10) for _ in range(cols)] for _ in range(rows)]
          self._products = {}  # Private attribute for product catalog
          self._action_log = []  # Private attribute for logging
      
      def _validate_location(self, row, col):
          # Private method for internal use only
          return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0])
      
      def store_product(self, sku, quantity, row, col):
          if not self._validate_location(row, col):
              return False
          # Rest of implementation
  ```

- **Inheritance:** While I haven't implemented subclasses yet, my design creates a solid foundation for future extension:
  ```python
  # Future enhancement example:
  class PerishableProduct(Product):
      def __init__(self, name, sku, price, quantity, expiry_date):
          super().__init__(name, sku, price, quantity)
          self.expiry_date = expiry_date
          
      def is_expired(self, current_date):
          return current_date > self.expiry_date
  ```

- **Polymorphism:** Methods handle different object types appropriately, enabling code reuse and flexibility:
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

- **Abstraction:** The system hides complex implementation details behind simple interfaces:
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

- **High Cohesion:** Each class has a single, well-defined responsibility with strongly related functionality:
  ```python
  # Product class only handles product-related data and behavior
  class Product:
      def __init__(self, name, sku, price, quantity=0):
          self.name = name
          self.sku = sku
          self.price = price
          self.quantity = quantity
      
      def calculate_value(self):
          return self.price * self.quantity
      
      def is_in_stock(self):
          return self.quantity > 0
  ```

- **Low Coupling:** Classes have minimal dependencies on each other, making the system more modular and easier to maintain:
  ```python
  # GUI class interacts with Warehouse through a clean interface
  class InventoryGUI:
      def __init__(self, warehouse):
          self.warehouse = warehouse
          # No need to know about internal warehouse implementation
      
      def add_product_button_clicked(self):
          name = self.name_entry.get()
          sku = self.sku_entry.get()
          price = float(self.price_entry.get())
          quantity = int(self.quantity_entry.get())
          
          # Simply calls warehouse method without knowing details
          success = self.warehouse.add_product(name, sku, price, quantity)
          if success:
              self.show_message("Product added successfully")
          else:
              self.show_error("Failed to add product")
  ```

- **Composition:** I built complex objects by composing simpler ones, creating a flexible and maintainable structure:
  ```python
  class Warehouse:
      def __init__(self, rows, cols):
          # Warehouse is composed of Location objects
          self.grid = [[Location(10) for _ in range(cols)] for _ in range(rows)]
          self.products = {}
          
          # Logger is composed within Warehouse
          self.logger = ActivityLogger("warehouse_activity.log")
      
      def log_activity(self, action, details):
          self.logger.log(action, details)
  ```

- **Association:** Objects in my system maintain relationships with other objects while existing independently:
  ```python
  class Order:
      def __init__(self, order_id):
          self.order_id = order_id
          self.items = []  # Association to Product objects
          self.customer = None  # Association to a Customer object
      
      def add_item(self, product, quantity):
          self.items.append({"product": product, "quantity": quantity})
      
      def assign_customer(self, customer):
          self.customer = customer
  ```

- **Aggregation:** The system models "has-a" relationships where components can exist independently:
  ```python
  class ShippingDepartment:
      def __init__(self):
          self.pending_orders = []
          self.warehouse = None  # Aggregation: the warehouse can exist independently
      
      def link_warehouse(self, warehouse):
          self.warehouse = warehouse
      
      def process_order(self, order):
          for item in order.items:
              product = item["product"]
              quantity = item["quantity"]
              if not self.warehouse.retrieve_product(product.sku, quantity):
                  return False
          return True
  ```

- **Modularity:** I organized the code into distinct modules with specific responsibilities:
  ```python
  # In models.py - Contains data models
  class Product:
      # Product implementation
  
  class Location:
      # Location implementation
  
  # In warehouse.py - Handles warehouse operations
  class Warehouse:
      # Warehouse implementation
  
  # In gui.py - Handles user interface
  class InventoryGUI:
      # GUI implementation
  
  # In data_manager.py - Handles data persistence
  class CSVDataManager:
      def save_products(self, products, filename):
          # Implementation for saving products to CSV
      
      def load_products(self, filename):
          # Implementation for loading products from CSV
  ```

Overall, OOP principles allowed me to break this complex inventory system into manageable components, each with clear responsibilities. This approach has made the code easier to test and maintain, and provides a robust foundation for adding new features in the future, such as different product types or advanced warehouse visualization.
