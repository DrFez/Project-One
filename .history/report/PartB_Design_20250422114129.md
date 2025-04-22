# Part B: Design

## Data Structures and OOP Implementation

When I started designing the system, I knew I wanted to keep things modular and easy to understand. I broke the project into three main classes: Product, Location, and Warehouse. Here’s how I approached each one:

### Product Class
- **Attributes:** name, sku, price, quantity
- **Methods:** update_price, update_quantity, __str__, and validation methods
- **OOP:** This class is all about encapsulating product data. I made sure it only handles product-specific logic, so if I want to add more product types later, I can just extend this class.

### Location Class
- **Attributes:** row, col, capacity, inventory (dict of SKU to quantity)
- **Methods:** add_product, remove_product, get_available_capacity, get_location_code
- **OOP:** Each location manages its own inventory. This keeps the logic for storage separate from the rest of the system, and makes it easy to check or update what’s in a specific spot.

### Warehouse Class
- **Attributes:** rows, cols, grid (2D list of Location), products (dict of SKU to Product)
- **Methods:** add_product, store_product, retrieve_product, find_product, validate_quantities, load_data, save_data
- **OOP:** The Warehouse class ties everything together. It manages the grid, keeps track of all products, and handles the main operations. If I want to add more advanced features later, I can do it here without messing up the rest of the code.
## Pseudocode for Three Classes and Mainline

### Product Class
```
CLASS Product
    FUNCTION initialize(name, sku, price, quantity)
        VALIDATE name is non-empty string
        VALIDATE sku is non-empty string
        VALIDATE price is non-negative number
        VALIDATE quantity is non-negative integer
        
        SET this.name = name
        SET this.sku = sku
        SET this.price = price
        SET this.quantity = quantity
    END FUNCTION
    
    FUNCTION update_price(new_price)
        VALIDATE new_price is non-negative number
        SET this.price = new_price
        RETURN true
    END FUNCTION
    
    FUNCTION update_quantity(delta)
        SET new_quantity = this.quantity + delta
        VALIDATE new_quantity is not negative
        SET this.quantity = new_quantity
        RETURN true
    END FUNCTION
    
    FUNCTION to_string()
        RETURN formatted string with product details
    END FUNCTION
END CLASS
```

### Location Class
```
CLASS Location
    FUNCTION initialize(row, col, capacity)
        VALIDATE row is non-negative integer
        VALIDATE col is non-negative integer
        VALIDATE capacity is positive integer
        
        SET this.row = row
        SET this.col = col
        SET this.capacity = capacity
        SET this.inventory = empty dictionary
    END FUNCTION
    
    FUNCTION add_product(sku, qty)
        VALIDATE sku is non-empty string
        VALIDATE qty is positive integer
        
        SET current_usage = sum of all values in this.inventory
        VALIDATE current_usage + qty <= this.capacity
        
        IF sku exists in this.inventory THEN
            INCREMENT this.inventory[sku] by qty
        ELSE
            SET this.inventory[sku] = qty
        END IF
        
        RETURN true
    END FUNCTION
    
    FUNCTION remove_product(sku, qty)
        VALIDATE sku is non-empty string
        VALIDATE qty is positive integer
        VALIDATE sku exists in this.inventory
        VALIDATE this.inventory[sku] >= qty
        
        DECREMENT this.inventory[sku] by qty
        IF this.inventory[sku] equals 0 THEN
            REMOVE sku from this.inventory
        END IF
        
        RETURN true
    END FUNCTION
    
    FUNCTION get_available_capacity()
        SET current_usage = sum of all values in this.inventory
        RETURN this.capacity - current_usage
    END FUNCTION
    
    FUNCTION get_location_code()
        SET row_letter = character at position (65 + this.row) in ASCII
        RETURN row_letter concatenated with (this.col + 1)
    END FUNCTION
END CLASS
```

### Warehouse Class
```
CLASS Warehouse
    FUNCTION initialize(rows, cols)
        VALIDATE rows is positive integer
        VALIDATE cols is positive integer
        
        SET this.rows = rows
        SET this.cols = cols
        
        CREATE 2D array this.grid with dimensions rows x cols
        FOR each position r, c in grid
            SET this.grid[r][c] = new Location(r, c, 100)
        END FOR
        
        SET this.products = empty dictionary
    END FUNCTION
    
    FUNCTION add_product(product)
        VALIDATE product is a Product object
        VALIDATE product.sku does not exist in this.products
        
        SET this.products[product.sku] = product
        RETURN true
    END FUNCTION
    
    FUNCTION store_product(sku, qty, row, col)
        VALIDATE sku exists in this.products
        VALIDATE qty is positive integer
        VALIDATE row is within bounds of this.rows
        VALIDATE col is within bounds of this.cols
        
        CALL this.grid[row][col].add_product(sku, qty)
        CALL this.products[sku].update_quantity(qty)
        RETURN true
    END FUNCTION
    
    FUNCTION retrieve_product(sku, qty, row, col)
        VALIDATE sku exists in this.products
        VALIDATE qty is positive integer
        VALIDATE row is within bounds of this.rows
        VALIDATE col is within bounds of this.cols
        
        CALL this.grid[row][col].remove_product(sku, qty)
        CALL this.products[sku].update_quantity(-qty)
        RETURN true
    END FUNCTION
    
    FUNCTION find_product(sku)
        VALIDATE sku is non-empty string
        
        SET locations = empty array
        FOR each row r in range(0, this.rows)
            FOR each column c in range(0, this.cols)
                SET location = this.grid[r][c]
                IF sku exists in location.inventory THEN
                    ADD location details to locations array
                END IF
            END FOR
        END FOR
        
        RETURN locations
    END FUNCTION
    
    FUNCTION validate_quantities()
        SET errors = empty array
        
        FOR each sku, product in this.products
            SET total_quantity = 0
            FOR each location in this.grid
                IF sku exists in location.inventory THEN
                    ADD location.inventory[sku] to total_quantity
                END IF
            END FOR
            
            IF total_quantity != product.quantity THEN
                ADD discrepancy details to errors array
            END IF
        END FOR
        
        RETURN errors
    END FUNCTION
    
    FUNCTION load_data()
        TRY
            OPEN "products.csv" for reading
            SKIP header line
            FOR each line in file
                PARSE line to get name, sku, price, quantity
                CREATE new Product with parsed values
                ADD product to this.products
            END FOR
            
            OPEN "locations.csv" for reading
            SKIP header line
            FOR each line in file
                PARSE line to get sku, row, col, quantity
                CALL this.grid[row][col].add_product(sku, quantity)
            END FOR
            
            RETURN true
        CATCH error
            PRINT error message
            RETURN false
        END TRY
    END FUNCTION
    
    FUNCTION save_data()
        TRY
            OPEN "products.csv" for writing
            WRITE header line
            FOR each product in this.products
                WRITE product details to file
            END FOR
            
            OPEN "locations.csv" for writing
            WRITE header line
            FOR each location in this.grid
                FOR each sku, quantity in location.inventory
                    WRITE location and product details to file
                END FOR
            END FOR
            
            RETURN true
        CATCH error
            PRINT error message
            RETURN false
        END TRY
    END FUNCTION
END CLASS
```

### Mainline
```
FUNCTION main()
    GET username from user
    PRINT welcome message
    
    CREATE warehouse with 5 rows and 8 columns
    
    CALL warehouse.load_data()
    IF load unsuccessful THEN
        PRINT warning message
    END IF
    
    LOOP
        DISPLAY menu options
        GET user choice
        
        IF choice is "Add new product" THEN
            GET product details from user
            TRY
                CREATE new Product with entered details
                CALL warehouse.add_product(product)
                PRINT success message
            CATCH error
                PRINT error message
            END TRY
        
        ELSE IF choice is "Store product" THEN
            GET storage details from user
            TRY
                CALL warehouse.store_product with entered details
                PRINT success message
            CATCH error
                PRINT error message
            END TRY
        
        ELSE IF choice is "Retrieve product" THEN
            GET retrieval details from user
            TRY
                CALL warehouse.retrieve_product with entered details
                PRINT success message
            CATCH error
                PRINT error message
            END TRY
        
        ELSE IF choice is "Find product" THEN
            GET sku from user
            SET locations = warehouse.find_product(sku)
            IF locations is empty THEN
                PRINT not found message
            ELSE
                PRINT locations
            END IF
        
        ELSE IF choice is "Update price" THEN
            GET sku and new price from user
            IF sku exists in warehouse.products THEN
                TRY
                    CALL warehouse.products[sku].update_price(new_price)
                    PRINT success message
                CATCH error
                    PRINT error message
                END TRY
            ELSE
                PRINT not found message
            END IF
        
        ELSE IF choice is "Validate inventory" THEN
            SET errors = warehouse.validate_quantities()
            IF errors is empty THEN
                PRINT success message
            ELSE
                PRINT discrepancies
            END IF
        
        ELSE IF choice is "Save data" THEN
            CALL warehouse.save_data()
            IF save successful THEN
                PRINT success message
            ELSE
                PRINT error message
            END IF
        
        ELSE IF choice is "Exit" THEN
            PRINT goodbye message
            EXIT LOOP
        
        ELSE
            PRINT invalid choice message
        END IF
    END LOOP
END FUNCTION

CALL main()
```

## Version Control Planning

I used Git for version control. I kept my main branch stable, and did all my new features and bug fixes in separate branches. I tried to write clear commit messages so I could track what I changed and why. I also pushed to GitHub regularly so I wouldn't lose my work.

## Exception Handling and Validation (Pseudocode)

```
TRY
    GET price from user input
    CONVERT price to number
    IF price < 0 THEN
        THROW ValueError with message "Price must be non-negative"
    END IF
CATCH ValueError as error
    PRINT "Input error: " + error message
END TRY
```

## Algorithm Design and Testing

### Validation
- I made sure to check all user inputs for type, range, and business rules (like unique SKUs and positive quantities).
- When loading data from files, I checked for missing or invalid entries.

### Testing Plan
- I wrote unit tests for the main class methods (add, store, retrieve, validation).
- I tested workflows like adding a product, storing it, and retrieving it, both in the GUI and CLI.
- I used the provided test data to make sure everything worked as expected.
- I also did manual testing, trying out edge cases and intentionally entering bad data to see if the system handled it.

### Writing for Maintenance
- I added docstrings to all my classes and methods, describing what they do, their parameters, and return values.
- I used consistent formatting and added detailed comments for complex logic.
- I structured the code in a readable way with clear separation of concerns between classes.
- I designed the architecture to be extensible, making it easy to add new features in the future.
- I created a detailed README file with setup instructions and usage examples.
- The code is modular, so if I want to add new features or fix bugs later, I can do it without breaking the rest of the system.
- I left comments explaining tricky parts or important design decisions.
