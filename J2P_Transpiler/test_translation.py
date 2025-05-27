import lex_analyzer
import translator
from enhancements import CollectionTranslator, ExceptionHandler

def test_exception_translation():
    # Sample Java code with exception handling
    java_code = """
    try {
        int[] numbers = new int[5];
        numbers[10] = 100;
    } catch (IndexOutOfBoundsException e) {
        System.out.println("Array index out of bounds: " + e.getMessage());
    }
    """
    
    # Test array translation
    array_init = "int[] numbers = new int[5]"
    translated_array = CollectionTranslator.translate_array_init(array_init)
    print("Translated array:", translated_array)
    
    # Test exception handling translation
    translated_code = ExceptionHandler.translate_try_catch(java_code)
    print("\nTranslated exception handling:")
    print(translated_code)

if __name__ == "__main__":
    test_exception_translation() 
