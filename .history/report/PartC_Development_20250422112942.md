# Part C: Development

## Code Comments and OOP Demonstration

Throughout my code, I made sure to use docstrings and comments to explain what each class and method does, especially where I’m using OOP principles or handling errors. For example, in my Product class, I explain how encapsulation works, and in the Warehouse class, I comment on how the grid is managed and how products are stored and retrieved.

## Debugging Proof

I used both print statements and breakpoints to debug my code. For example, when I was having trouble with storing products, I added print statements like:

```python
print(f"DEBUG: Storing {quantity} units of {sku} at ({row},{col})")
```

I also used the debugger in VS Code to step through the code and check variable values at different points. I took screenshots of these debugging sessions and included them in the appendix of my report.

## Unit Testing

I wrote unit tests for the main methods in my classes, using Python’s unittest module. Here’s an example:

```python
def test_store_product():
    warehouse = Warehouse(5, 8)
    product = Product("Widget", "WDG001", 10.99, 50)
    warehouse.add_product(product)
    assert warehouse.store_product("WDG001", 10, 0, 0)
```

I also used the provided test data (in data/products.csv and data/locations.csv) to make sure the system worked with real examples.

## Live Data Testing

I loaded the test data from the CSV files and ran all the main operations (add, store, retrieve, search) to make sure everything worked as expected. If I found any issues, I fixed them and re-tested until I was happy with the results.

## Additional Notes

- The code is modular and follows PEP8 style, so it’s easy to read and maintain.
- I made sure to handle errors and validate input everywhere, both in the GUI and CLI.
- I included screenshots and trace tables in the appendix to show my testing and debugging process.
