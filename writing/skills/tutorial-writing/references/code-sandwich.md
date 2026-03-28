# Code Sandwich Approach

The Code Sandwich Approach is a method for presenting code to learners that maximizes understanding and learning.

## The Problem

Dumping large blocks of code into tutorials and asking readers to copy/paste provides no learning value. Readers don't understand:
* What the code does
* Why it's written that way
* How to modify it for their needs
* What happens if something goes wrong

## The Solution: Code Sandwich

Present code in three layers, like a sandwich:

1. **Top Bread:** Introduce the issue/need
2. **Filling:** Show the code that solves it
3. **Bottom Bread:** Detailed explanation of how it works

## The Three Parts

### 1. Introduce the Issue

Before showing code, explain what you're trying to solve:

* What problem does this code address?
* What functionality will it provide?
* Why is this step necessary?

**Example:**
> To process incoming orders, you need a function that validates the order data before saving it to the database. This prevents invalid orders from corrupting your data.

### 2. Introduce the Code

Show the code that solves the problem:

* Present the code block
* Keep it focused on the current concept
* Use syntax highlighting appropriate to the language

**Example:**
```python
def validate_order(order_data):
    if not order_data.get('customer_id'):
        raise ValueError("customer_id is required")
    if not order_data.get('items'):
        raise ValueError("order must contain items")
    return True
```

### 3. Detailed Explanation

Explain how the code works:

* Call out specific parts of the code
* Explain what they do
* Explain why they're necessary
* Connect it back to the problem being solved

**Example:**
> The `validate_order` function checks two critical pieces of order data. First, it verifies that a `customer_id` exists using the `get()` method, which safely checks for the key without raising an error if it's missing. Second, it ensures the order contains items. If either check fails, the function raises a `ValueError` with a descriptive message, preventing the invalid order from being processed. When validation succeeds, the function returns `True`, signaling that the order can be safely saved.

## Strategic Breakdown

Don't present entire files at once. Break them down strategically:

### By Primary Function

Break code into logical units:
* One function or method at a time
* Related group of functions
* A complete class
* A configuration section

### For Nested Structures

Go deeper when showing complex structures:
* Show the outer structure first
* Then explain inner components (classes, loops, conditionals)
* This doesn't need to be line-by-line
* Focus on understanding, not exhaustive detail

## "Bringing It All Together" Section

After explaining code in pieces, provide the complete section:

* Show the full, unbroken code
* Include all the pieces you explained separately
* This is what readers copy/paste
* Title it "Bringing it all together" or similar

**Example structure:**

```markdown
## Step 3 — Creating the order validation system

In this step, you will create a validation system...

First, create the validation function...

[Code Sandwich for validate_order function]

Next, create the function that saves validated orders...

[Code Sandwich for save_order function]

### Bringing it all together

Now that you understand each component, here's the complete validation module:

```python
[Complete file with all components]
```

Save this as `orders/validation.py`.
```

## Benefits of Code Sandwich Approach

* **Teaches concepts** - Readers learn, not just copy
* **Builds confidence** - Readers understand what they're doing
* **Enables customization** - Readers can modify for their needs
* **Aids troubleshooting** - Readers understand how to debug
* **Feels less overwhelming** - Breaking code into pieces is less intimidating

## Anti-Patterns to Avoid

**DON'T:**
* Dump entire files without explanation
* Show code without context
* Explain after showing everything
* Assume readers understand common patterns
* Skip over "obvious" parts

**DO:**
* Build understanding incrementally
* Explain before and after showing code
* Call out specific lines and what they do
* Assume readers are seeing this for the first time
* Explain the "why" not just the "what"

## Example: Full Code Sandwich in Action

> **Issue:** Your application needs to connect to a database and handle connection errors gracefully.
>
> Add the following function to create a database connection:
>
> ```python
> def get_database_connection():
>     try:
>         conn = psycopg2.connect(
>             host=os.getenv('DB_HOST'),
>             database=os.getenv('DB_NAME'),
>             user=os.getenv('DB_USER'),
>             password=os.getenv('DB_PASSWORD')
>         )
>         return conn
>     except psycopg2.Error as e:
>         print(f"Database connection failed: {e}")
>         return None
> ```
>
> **Explanation:** The `get_database_connection` function attempts to connect to PostgreSQL using the `psycopg2.connect()` method. It pulls connection credentials from environment variables using `os.getenv()`, which keeps sensitive information out of your code. The connection attempt is wrapped in a try-except block to catch any `psycopg2.Error` that might occur, such as incorrect credentials or an unreachable database server. If the connection succeeds, the function returns the connection object. If it fails, the function prints a descriptive error message and returns `None`, allowing your application to handle the failure gracefully rather than crashing.

This example shows all three layers: the issue (need to connect to database), the code (the function), and the explanation (how it works and why).
