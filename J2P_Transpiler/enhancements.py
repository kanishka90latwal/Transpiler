from typing import List, Dict, Set, Any, Optional

class CollectionTranslator:
    """Handles translation of Java collections to Python equivalents."""
    
    @staticmethod
    def translate_array_init(java_array: str) -> str:
        """Converts Java array initialization to Python list."""
        # Handle cases like: int[] arr = new int[10];
        # or String[] names = {"John", "Jane"};
        if "new" in java_array:
            # Handle array size initialization
            size_start = java_array.find("[") + 1
            size_end = java_array.find("]")
            if size_start > 0 and size_end > 0:
                size = java_array[size_start:size_end]
                return f"[None] * {size}"
        elif "{" in java_array:
            # Handle direct initialization
            content = java_array[java_array.find("{") + 1:java_array.find("}")]
            return f"[{content}]"
        return "[]"

    @staticmethod
    def translate_arraylist(java_list: str) -> str:
        """Converts Java ArrayList operations to Python list operations."""
        # Map common ArrayList methods to Python list methods
        java_to_python = {
            ".add(": ".append(",
            ".remove(": ".remove(",
            ".get(": "[",
            ".set(": "[",
            ".size()": "len(",
            ".clear()": ".clear()",
            ".isEmpty()": "not ",
        }
        
        result = java_list
        for java_op, python_op in java_to_python.items():
            result = result.replace(java_op, python_op)
            
        # Handle special case for .get() and .set()
        if "](" in result:  # From .get( or .set(
            result = result.replace("](", "] = ")
            
        return result

    @staticmethod
    def translate_hashmap(java_map: str) -> str:
        """Converts Java HashMap operations to Python dict operations."""
        # Map common HashMap methods to Python dict methods
        java_to_python = {
            ".put(": "[",
            ".get(": ".get(",
            ".remove(": ".pop(",
            ".containsKey(": " in ",
            ".size()": "len(",
            ".clear()": ".clear()",
            ".isEmpty()": "not ",
        }
        
        result = java_map
        for java_op, python_op in java_to_python.items():
            result = result.replace(java_op, python_op)
            
        # Handle special case for .put()
        if "](" in result:  # From .put(
            result = result.replace("](", "] = ")
            
        return result

class ExceptionHandler:
    """Handles translation of Java exception handling to Python."""
    
    # Mapping of common Java exceptions to Python exceptions
    EXCEPTION_MAP = {
        "Exception": "Exception",
        "RuntimeException": "RuntimeError",
        "IllegalArgumentException": "ValueError",
        "NullPointerException": "AttributeError",
        "IndexOutOfBoundsException": "IndexError",
        "IOException": "IOError",
        "FileNotFoundException": "FileNotFoundError",
        "ArithmeticException": "ArithmeticError",
        "NumberFormatException": "ValueError",
    }

    @staticmethod
    def translate_try_catch(java_code: str) -> str:
        """Converts Java try-catch blocks to Python try-except."""
        lines = java_code.split("\n")
        python_code = []
        in_try_block = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("try {"):
                python_code.append("try:")
                in_try_block = True
            elif line.startswith("catch ("):
                # Extract exception type and variable
                catch_info = line[line.find("(")+1:line.find(")")]
                exception_type, var_name = catch_info.split()
                
                # Map Java exception to Python equivalent
                python_exception = ExceptionHandler.EXCEPTION_MAP.get(
                    exception_type, "Exception")
                
                python_code.append(f"except {python_exception} as {var_name}:")
            elif line.startswith("finally {"):
                python_code.append("finally:")
            elif line == "}":
                if in_try_block:
                    in_try_block = False
            else:
                # Add indentation for block contents
                if line:
                    python_code.append("    " + line)
        
        return "\n".join(python_code)

    @staticmethod
    def translate_throws(method_signature: str) -> str:
        """Handles Java throws declarations in method signatures."""
        # In Python, we don't need throws declarations
        # This method removes them from the signature
        if "throws" in method_signature:
            return method_signature[:method_signature.find("throws")].strip()
        return method_signature 
