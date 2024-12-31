import random
import string
import sys
import base64
import gzip
import re
import os

# Helper function to generate a random string of given length
def generate_random_name(length=8):
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    # Ensure the name doesn't start with a digit
    while random_name[0].isdigit():
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return random_name

# Function to rename variables in the Python code
def rename_variables_in_code(code):
    # Find all variable assignments (single equal sign)
    # Capture leading spaces for indentation in group 1, variable name in group 2, and value in group 3
    variable_pattern = r'(^\s*)([a-zA-Z_]\w*)\s*=\s*(.+)$'
    
    # Create a dictionary to map old variable names to new random names
    rename_map = {}
    for match in re.finditer(variable_pattern, code, re.MULTILINE):
        var_name = match.group(2)  # The actual variable name
        # Generate a random name for the variable
        random_name = generate_random_name()
        rename_map[var_name] = random_name

    # Replace variable declarations with the new names while preserving indentation
    def replace_var_name(match):
        old_var = match.group(2)
        new_var = rename_map[old_var]
        indentation = match.group(1)  # The leading spaces are preserved here
        return f"{indentation}{new_var} = {match.group(3)}"

    # Apply the renaming to the code
    code = re.sub(variable_pattern, replace_var_name, code, flags=re.MULTILINE)

    # Replace variable references (in expressions) throughout the code while preserving indentation
    def replace_var_reference(match):
        var_name = match.group(1)
        if var_name in rename_map:
            return rename_map[var_name]
        return match.group(0)  # If it's not a variable, leave it unchanged

    # Apply renaming for variable references throughout the code
    code = re.sub(r'(\b[a-zA-Z_]\w*\b)', replace_var_reference, code)

    return code

# Function to rename functions in the Python code
def rename_functions_in_code(code):
    # Find all function definitions
    function_pattern = r"def (\w+)\("  # Matches function definitions like def function_name(
    functions = re.findall(function_pattern, code)

    # Create a dictionary to map old function names to new random names
    rename_map = {}
    for func in functions:
        random_name = generate_random_name()  # Generate a random name for the function
        rename_map[func] = random_name

    # Rename function definitions
    def replace_func_name(match):
        old_func = match.group(1)
        new_func = rename_map[old_func]
        return f"def {new_func}("

    code = re.sub(function_pattern, replace_func_name, code)

    # Replace function calls
    call_pattern = r"(\w+)\("  # Matches function calls like function_name(
    
    def replace_func_call(match):
        called_func = match.group(1)
        if called_func in rename_map:
            new_name = rename_map[called_func]
            return f"{new_name}("
        return match.group(0)  # If it's not a function, leave it unchanged

    code = re.sub(call_pattern, replace_func_call, code)

    return code

# Function to wrap the modified code with gzip and base64
def compress_and_encode(code):
    # Compress the modified code using gzip
    compressed = gzip.compress(code.encode('utf-8'))

    # Encode the compressed code using base64
    encoded = base64.b64encode(compressed).decode('utf-8')

    # Return the base64 encoded string for the obfuscated script
    return encoded

# Main function to handle the command-line arguments
def main():
    if len(sys.argv) != 3:
        sys.exit(f"\r\nSyntax: python3 {sys.argv[0]} <input_path> <output_path>\r\n")

    input_script = sys.argv[1]
    output_script = sys.argv[2]

    # Read the content of the input file
    try:
        with open(input_script, 'r') as file:
            original_code = file.read()
    except Exception as e:
        sys.exit(e)

    # Apply variable renaming
    code = rename_variables_in_code(original_code)

    # Apply function renaming
    code = rename_functions_in_code(code)

    # Compress and encode the modified code
    encoded_code = compress_and_encode(code)

    # Build the final obfuscated script
    obfuscated_script = f"""import base64, gzip
exec(gzip.decompress(base64.b64decode("{encoded_code}")))
"""

    # Write the obfuscated script to the output file
    try:
        with open(output_script, 'w') as file:
            file.write(obfuscated_script)
    except Exception as e:
        sys.exit(e)

    sys.exit('\r\nOperation complete! Obfuscated script saved.\r\n')

# Entry point for the script
if __name__ == "__main__":
    main()
