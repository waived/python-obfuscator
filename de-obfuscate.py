import base64, gzip, sys, os

def main():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    
    if len(sys.argv) != 3:
        sys.exit(f"\r\n Syntax: python3 {sys.argv[0]} <input_path> <output_path>\r\n")
    
    #read file
    try:
        with open(sys.argv[1], 'r') as file:
            obfuscated = file.read()
    except Exception as e:
        sys.exit(e)
        
        
    #pull encoded string from obfuscated code
    code_start = obfuscated.find('base64.b64decode("') + len('base64.b64decode("')
    code_end = obfuscated.find('")', code_start)
    
    if code_start == -1 or code_end == -1:
        sys.exit("\r\nError! This does not appear to be obfuscated. Exiting...\r\n")
    
    encoded = obfuscated[code_start:code_end]
    
    #decode from base-64
    compressed = base64.b64decode(encoded)
    
    #g-zip decompression
    og_code = gzip.decompress(compressed).decode('utf-8')
    
    #output to file
    try:
        with open(sys.argv[2], 'w') as output_file:
            output_file.write(og_code)
    except Exception as e:
        sys.exitt(e)
    
    sys.exit('\r\nOperation complete!\r\n')

if __name__ == "__main__":
    main()
