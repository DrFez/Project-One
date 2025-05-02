# Part C: Development

## Code Comments and OOP Demonstration

Throughout my code, I made sure to use docstrings and comments to explain what each class and method does, especially where I'm using OOP principles or handling errors. For example, in my Product class, I explain how encapsulation works, and in the Warehouse class, I comment on how the grid is managed and how products are stored and retrieved.

### Examples of Code Comments

#### Logic Comments
```python
# Calculate available space by subtracting current stock from capacity
available_space = location.capacity - location.current_stock

# If the remaining quantity exceeds the location capacity, use maximum capacity
quantity_to_store = min(quantity_to_distribute, available_space)
```

#### OOP Characteristics
```python
class Product:
    """
    Represents a product in the inventory management system.
    
    This class demonstrates encapsulation by controlling access to its attributes
    through methods like update_quantity and update_price, which include validation.
    
    Attributes:
        name (str): The name of the product
        sku (str): Stock Keeping Unit - unique identifier for the product
        price (float): The price of the product
        quantity (int): The quantity of the product in stock
    """
```

#### Exception Handling
```python
try:
    price = float(price_str)
    if price < 0:
        raise ValueError("Price must be non-negative")
except ValueError:
    self.show_message("Please enter a valid price.", is_error=True)
    return
```

#### Validation
```python
def update_price(self, new_price):
    """
    Update the price of the product.
    
    Args:
        new_price (float): The new price value
        
    Returns:
        bool: True if price was updated successfully, False otherwise
    """
    # Validate that price is not negative
    if new_price >= 0:
        self.price = new_price
        return True
    return False
```

#### Parameters and Arguments
```python
def store_product(self, sku, quantity, row, col):
    """
    Store a product at a specific location.
    
    Args:
        sku (str): The SKU of the product to store
        quantity (int): The quantity to store
        row (int): The row coordinate in the warehouse grid
        col (int): The column coordinate in the warehouse grid
            
    Returns:
        bool: True if successful, False otherwise
    """
```

## Debugging Proof

I used multiple debugging techniques throughout the development process to ensure the system worked correctly:

### Print Statements and Breakpoints

I used both print statements and breakpoints to debug my code. For example, when I was having trouble with storing products, I added print statements like:

```python
print(f"DEBUG: Storing {quantity} units of {sku} at ({row},{col})")
```

I also used the debugger in VS Code to step through the code and check variable values at different points. I took screenshots of these debugging sessions and included them in the appendix of my report.

### Colorized Console Debugging with debug_utils

To make debugging more organized and visually distinguishable, I created a `debug_utils.py` module with a `DebugPrint` class that provides colorized console output:

```python
DebugPrint.info(f"Initializing warehouse with dimensions {rows}x{cols}")
DebugPrint.process(f"Adding product {product.sku} with quantity {product.quantity}")
DebugPrint.success(f"Successfully stored {quantity} units of {sku} at ({row},{col})")
DebugPrint.warning(f"Product {sku} already exists")
DebugPrint.error("Failed to load product data")
DebugPrint.database("Saving warehouse data to CSV files")
```

This system allowed me to:
- Categorize debug messages by type (info, warning, success, etc.)
- Include timestamps for tracking execution flow
- Enable/disable debugging output globally
- Easily distinguish between different operations with color coding

### User Action Logging

I implemented a comprehensive logging system that records all user actions to `logs.csv`. This was invaluable for:
- Tracking user behavior during testing
- Identifying the sequence of events leading to a bug
- Monitoring performance issues over time
- Creating an audit trail of inventory changes

The logging system records:
- Timestamp of each action
- Username of the person performing the action
- Description of the action performed

### Log Viewer GUI

To make it easier to review logs during development and testing, I created a `LogView` class that displays the action logs in a graphical interface. This allowed me to:
- Filter and search through logs
- View logs while the application is running
- Share debugging information with testers
- Identify patterns in user behavior that might cause issues

## Unit Testing and Trace Tables

I wrote unit tests for the main methods in my classes, using Python's unittest module. Here's an example:

```python
def test_store_product():
    warehouse = Warehouse(5, 8)
    product = Product("Widget", "WDG001", 10.99, 50)
    warehouse.add_product(product)
    assert warehouse.store_product("WDG001", 10, 0, 0)
```

I also used the provided test data (in data/products.csv and data/locations.csv) to make sure the system worked with real examples.

### Stubs

For some methods, I used stubs to isolate and test specific functionality before the rest of the system was complete. Here are concrete examples of stubs I implemented:

#### Product Validation Stub
```python
def validate_product_stub(name, sku, price, quantity):
    """
    Stub for product validation that returns validation errors without creating products.
    Used for testing validation logic independently from product creation.
    """
    errors = []
    
    # Validate name
    if not name or len(name.strip()) == 0:
        errors.append("Product name cannot be empty")
    
    # Validate SKU
    if not sku or len(sku.strip()) == 0:
        errors.append("SKU cannot be empty")
    elif len(sku) < 3 or len(sku) > 10:
        errors.append("SKU must be between 3-10 characters")
        
    # Validate price
    try:
        price_val = float(price)
        if price_val < 0:
            errors.append("Price cannot be negative")
    except ValueError:
        errors.append("Price must be a valid number")
        
    # Validate quantity
    try:
        qty_val = int(quantity)
        if qty_val < 0:
            errors.append("Quantity cannot be negative")
    except ValueError:
        errors.append("Quantity must be a valid integer")
        
    return errors
```

#### Warehouse Visualization Stub
```python
def visualize_warehouse_stub(rows, cols, filled_locations=None):
    """
    Stub for warehouse visualization that works before full warehouse implementation.
    Used for testing UI grid representation independently.
    
    Args:
        rows (int): Number of rows in warehouse
        cols (int): Number of columns in warehouse
        filled_locations (list): Optional list of tuples (row, col, fill_percent)
    """
    if filled_locations is None:
        filled_locations = []
        
    # Convert filled_locations to a dict for easy lookup
    fill_dict = {(r, c): p for r, c, p in filled_locations}
    
    result = "   " + " ".join(f"{i+1:2}" for i in range(cols)) + "\n"
    
    for r in range(rows):
        row_label = chr(65 + r)
        result += f"{row_label} "
        
        for c in range(cols):
            fill_percent = fill_dict.get((r, c), 0)
            
            if fill_percent == 0:
                result += "□  "  # Empty
            elif fill_percent < 50:
                result += "▲  "  # Less than half full
            elif fill_percent < 100:
                result += "■  "  # More than half full
            else:
                result += "▓  "  # Full
                
        result += "\n"
        
    return result
```

#### CSV Data Loading Stub
```python
def load_products_stub(filename="test_products.csv"):
    """
    Stub for loading products from CSV without requiring real file.
    Used for testing product loading logic before implementing file operations.
    """
    # Return hard-coded test data
    return {
        "WDG001": {"name": "Widget", "price": 10.99, "quantity": 50},
        "GZM002": {"name": "Gizmo", "price": 5.99, "quantity": 30},
        "THG003": {"name": "Thing", "price": 7.50, "quantity": 20}
    }
```

### Trace Tables
I created trace tables for at least three functions to show how the variables change step by step. Here are my examples:

#### Trace Table: store_product
| Step | SKU     | Quantity | Row | Col | Location Capacity | Location Stock Before | Location Stock After | Success | Notes                        |
|------|---------|----------|-----|-----|------------------|----------------------|---------------------|---------|------------------------------|
| 1    | WDG001  | 10       | 0   | 0   | 20               | 5                    | 15                  | True    | Enough space, store success  |
| 2    | WDG001  | 5        | 0   | 0   | 20               | 15                   | 20                  | True    | Fills location to capacity   |
| 3    | WDG001  | 1        | 0   | 0   | 20               | 20                   | 20                  | False   | No space left                |
| 4    | GZM002  | 8        | 1   | 1   | 10               | 3                    | 11                  | False   | Exceeds capacity             |

#### Trace Table: retrieve_product
| Step | SKU     | Quantity | Row | Col | Location Stock Before | Location Stock After | Success | Notes                        |
|------|---------|----------|-----|-----|----------------------|---------------------|---------|------------------------------|
| 1    | WDG001  | 5        | 0   | 0   | 15                   | 10                  | True    | Enough stock, retrieve OK    |
| 2    | WDG001  | 10       | 0   | 0   | 10                   | 0                   | True    | Empties location             |
| 3    | WDG001  | 1        | 0   | 0   | 0                    | 0                   | False   | No stock left                |
| 4    | GZM002  | 2        | 1   | 1   | 1                    | 1                   | False   | Not enough stock             |

#### Trace Table: distribute_initial_quantity
| Step | SKU     | Total Quantity | Available Space | Row | Col | Quantity to Store | Quantity Left | Location Stock After | Notes                        |
|------|---------|---------------|----------------|-----|-----|-------------------|--------------|---------------------|------------------------------|
| 1    | WDG001  | 50            | 20             | 0   | 0   | 20                | 30           | 20                  | First location filled        |
| 2    | WDG001  | 30            | 15             | 0   | 1   | 15                | 15           | 15                  | Second location partially filled |
| 3    | WDG001  | 15            | 20             | 0   | 2   | 15                | 0            | 15                  | All quantity distributed     |
| 4    | GZM002  | 100           | 70             | 0   | 0   | 20                | 80           | 20                  | First location filled        |
| 5    | GZM002  | 80            | 20             | 0   | 1   | 20                | 60           | 20                  | Second location filled       |
| 6    | GZM002  | 60            | 20             | 1   | 0   | 20                | 40           | 20                  | Third location filled        |
| 7    | GZM002  | 40            | 20             | 1   | 1   | 20                | 20           | 20                  | Fourth location filled       |
| 8    | GZM002  | 20            | 20             | 1   | 2   | 20                | 0            | 20                  | All quantity distributed     |

## Live Data Testing

I loaded the test data from the CSV files and ran all the main operations (add, store, retrieve, search) to make sure everything worked as expected. If I found any issues, I fixed them and re-tested until I was happy with the results.

### Test Data Loading Process

1. **Initial Data Load**: I integrated the provided test data files (products.csv and locations.csv) into my application's data storage system.

2. **Data Validation**: I verified that all rows from the CSV files were properly loaded and that relationships between products and locations were maintained.

3. **Interface Testing with Live Data**: I used the loaded data to test search functionality, product updates, and warehouse operations.

4. **Edge Cases**: I deliberately tested edge cases such as:
   - Retrieving more items than available
   - Storing products at locations already at capacity
   - Searching for products not in the database
   - Adding products with duplicate SKUs

5. **Data Consistency**: I confirmed that after various operations, the data remained consistent between the application memory and saved files.

## Additional Notes

- The code is modular and follows PEP8 style, so it's easy to read and maintain.
- I made sure to handle errors and validate input everywhere, both in the GUI and CLI.

