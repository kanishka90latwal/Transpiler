import os
from translator import translate_and_run

def main():
    # Get the absolute path to the test file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    java_file = os.path.join(current_dir, "test_exceptions.java")
    
    print("Processing Java file:", java_file)
    print("\n" + "="*50)
    
    compile_output, run_output, python_translation = translate_and_run(java_file)
    
    print("Java Compilation Output:")
    print("-"*30)
    if compile_output:
        print(compile_output)
    else:
        print("No compilation errors")
    
    print("\nJava Program Output:")
    print("-"*30)
    print(run_output)
    
    print("\nPython Translation:")
    print("-"*30)
    print("".join(python_translation))

if __name__ == "__main__":
    main() 
