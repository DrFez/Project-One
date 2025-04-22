# Part C: Development

## Code Comments
- All classes and methods include docstrings.
- Inline comments explain logic, error handling, and OOP usage.

## Debugging Proof
```python
# Example: Debugging with print statements
print("DEBUG: Storing product", sku, "at", row, col)
# Example: Breakpoint (screenshot in actual report)
```

## Unit Testing
- Use `unittest` or `pytest` for automated tests.
- Example test:
```python
def test_add_product():
    warehouse = Warehouse(5, 8)
    product = Product("Test", "SKU1", 10.0, 5)
    assert warehouse.add_product(product)
```

## Live Data Testing
- Use provided CSV/JSON files in `data/` for real-world testing.
- Document test results and issues found.
