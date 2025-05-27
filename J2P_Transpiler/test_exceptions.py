def main():
    # Test array and ArrayList with exception handling
    try:
        numbers = [None] * 5
        numbers[10] = 100  # This will cause IndexError
    except IndexError as e:
        print(f"Array index out of bounds: {str(e)}")

    # Test multiple catch blocks and finally
    try:
        str_val = None
        str_val.length()  # This will cause AttributeError
    except AttributeError as e:
        print(f"Null pointer found: {str(e)}")
    except Exception as e:
        print(f"General error: {str(e)}")
    finally:
        print("This will always execute")

    # Test method that throws exception
    try:
        divide_numbers(10, 0)
    except ArithmeticError as e:
        print("Cannot divide by zero!")

def divide_numbers(a: int, b: int) -> int:
    if b == 0:
        raise ArithmeticError("Division by zero")
    return a // b

if __name__ == "__main__":
    main() 
