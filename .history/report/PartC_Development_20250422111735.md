# Part C: Development

## Code Comments and OOP Demonstration
- All classes and methods include detailed docstrings and inline comments explaining logic, OOP principles, and error handling.
- Example:
```python
class Product:
    """Represents a product in the inventory (Encapsulation, Abstraction)."""
    def update_price(self, new_price):
        # Validate input (Validation, Exception Handling)
        if new_price < 0:
            raise ValueError("Price must be non-negative")
        self.price = new_price
```

## Debugging Proof
- **Breakpoints:** Used in IDE (PyCharm/VSCode) to step through methods like `store_product` and `retrieve_product`.
- **Print Statements:**
```python
print(f"DEBUG: Storing {quantity} units of {sku} at ({row},{col})")
```
- Screenshots of breakpoints and print output are included in the appendix of this report.

## Unit Testing
- Automated tests for all major methods using `unittest` or `pytest`.
- Example:
```python
def test_store_product():
    warehouse = Warehouse(5, 5)
    product = Product("Widget", "WDG001", 10.99, 50)
    warehouse.add_product(product)
    assert warehouse.store_product("WDG001", 10, 0, 0)
```
- Trace tables and stubs are used for at least two functions (see appendix).

## Live Data Testing
- The system is tested using the provided test data in `data/products.csv` and `data/locations.csv`.
- All inventory management functions are validated against this data, with results and issues documented.

## Additional Notes
- All code is modular, PEP8-compliant, and ready for future extension.
- Error handling and validation are present throughout.
- See appendix for screenshots and trace tables.
