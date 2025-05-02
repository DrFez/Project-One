# Part C: Development

## Code Comments and OOP Demonstration

Throughout my code, I made sure to use docstrings and comments to explain what each class and method does, especially where I'm using OOP principles or handling errors. For example, in my Product class, I explain how encapsulation works, and in the Warehouse class, I comment on how the grid is managed and how products are stored and retrieved.

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
For some methods, I used stubs to isolate and test specific functionality before the rest of the system was complete. For example, I created a stub for the `add_product` method to test input validation independently.

### Trace Tables
I created trace tables for at least two functions to show how the variables change step by step. Here are two examples with multiple steps:

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

## Live Data Testing

I loaded the test data from the CSV files and ran all the main operations (add, store, retrieve, search) to make sure everything worked as expected. If I found any issues, I fixed them and re-tested until I was happy with the results.

## Additional Notes

- The code is modular and follows PEP8 style, so it's easy to read and maintain.
- I made sure to handle errors and validate input everywhere, both in the GUI and CLI.

