import subprocess
import os
import sys

class JavaRunner:
    @staticmethod
    def compile_and_run(java_file_path: str) -> tuple[str, str]:
        """
        Compiles and runs a Java file, returning both the compilation and runtime output.
        
        Args:
            java_file_path: Path to the Java source file
            
        Returns:
            tuple: (compilation_output, runtime_output)
        """
        try:
            # Convert to absolute path and normalize
            java_file_path = os.path.abspath(java_file_path)
            
            if not os.path.exists(java_file_path):
                return "", f"Error: Java file not found: {java_file_path}"
            
            # Get the directory and filename
            directory = os.path.dirname(java_file_path)
            filename = os.path.basename(java_file_path)
            classname = os.path.splitext(filename)[0]
            
            # Change to the directory containing the Java file
            original_dir = os.getcwd()
            os.chdir(directory)
            
            try:
                # Compile the Java file
                compile_process = subprocess.run(
                    ['javac', filename],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # Run the compiled Java class
                run_process = subprocess.run(
                    ['java', classname],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                return compile_process.stdout, run_process.stdout
                
            except subprocess.CalledProcessError as e:
                if e.stderr:
                    return e.stderr, ""
                return str(e), ""
                
            finally:
                # Clean up the .class file
                class_file = f"{classname}.class"
                if os.path.exists(class_file):
                    try:
                        os.remove(class_file)
                    except:
                        pass  # Ignore cleanup errors
                
                # Change back to original directory
                os.chdir(original_dir)
            
        except Exception as e:
            return "", f"Error running Java code: {str(e)}"

def main():
    # Example usage
    if len(sys.argv) > 1:
        java_file = sys.argv[1]
        compile_output, run_output = JavaRunner.compile_and_run(java_file)
        
        if compile_output:
            print("Compilation output:")
            print(compile_output)
        
        if run_output:
            print("\nProgram output:")
            print(run_output)
    else:
        print("Please provide a Java file path")

if __name__ == "__main__":
    main() 
