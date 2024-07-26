import sys
from DEBUG import DEBUG

def parse_interactive(calculator_state):
    print("Welcome to the Jovial Assembler - the first and only assembler for the HP-16C calculator!")
    
    print("Please enter the name or path of the .jov file you would like to assemble.")
    input_file_name = input("File name: ").strip()
    while not input_file_name.endswith(".jov"):
        print("Invalid file type. Please enter a .jov file.")
        input_file_name = input("File name: ")
    
    print("Please enter the name of the output file with the desired extension format (.pdf/.16c).")
    temp = input("Output file name: ").strip()
    # Extract file extension and file name
    output_mode = temp[-4:].lower() if len(temp) > 4 else ""
    output_file_name = temp[:-4] if len(temp) > 4 else ""
    while output_mode not in [".16c", ".pdf"]:
        print("Invalid output file name. Please enter either a file with a '.16c' or '.pdf' extension.")
        temp = input("Output file name: ").strip()
        output_mode = temp[-4:].lower() if len(temp) > 4 else ""
        output_file_name = temp[:-4] if len(temp) > 4 else ""
    output_mode = output_mode[1:]  # trim the '.' from output mode
    if DEBUG: print(f"Output mode determined: {output_mode}")
    if DEBUG: print(f"Output file name: {output_file_name}")

    print("Please enter the initial settings for the calculator.")

    print("Enter the sign mode (0 = Unsigned, 1 = 1's complement, 2 = 2's complement, 3 = floating point).")
    print("If you are unsure, enter 0 for unsigned mode or 2 if you want to use signed numbers.")
    # Checking if sign_mode input is a number
    while True:
        try:
            sign_mode = int(input("Sign mode: "))
            if 0 <= sign_mode <= 3:
                break  # Exit loop if input is a valid number within range
            else:
                print("Invalid sign mode. Please enter a valid number (0, 1, 2, or 3).")
        except ValueError:
            print("Please enter a number.")

    if sign_mode == 3:
        # Word size is automatically 56 bits and base 10
        word_size = 56
        base = 10
    else:
        print("Enter the word size (number of bits in a word) between 4 bits and 64 bits.")
        print("If you are unsure, enter 16 for the standard word size. It has a good balance of register size and memory usage.")
        while True:
            try:
                word_size = int(input("Word size: "))
                if 4 <= word_size <= 64:
                    break  # Exit loop if input is a valid number within range
                else:
                    print("Invalid word size. Please enter a number between 4 and 64.")
            except ValueError:
                print("Please enter a number.")

        print("Enter the starting base of the number being entered (2 = binary, 8 = octal, 10 = decimal, 16 = hexadecimal).")
        print("If you are unsure, enter 10 for decimal. It is the most common base for entering numbers.")
        while True:
            try:
                base = int(input("Base: "))
                if base in [2, 8, 10, 16]:
                    break  # Exit loop if input is a valid number within the specified options
                else:
                    print("Invalid base. Please enter the base of the number being entered (2 = binary, 8 = octal, 10 = decimal, 16 = hexadecimal).")
            except ValueError:
                print("Please enter a number.")

    # Set the calculator state to the user's input
    calculator_state.sign_mode = sign_mode
    calculator_state.word_size = word_size
    calculator_state.update_base(base)
    calculator_state.input_file_name = input_file_name
    calculator_state.output_file_name = output_file_name
    calculator_state.output_mode = output_mode


def parse_cli(argv, calculator_state):
    # Parse the command line arguments
    if len(argv) == 3:
        # Default modes
        sign_mode = 2
        word_size = 16
        base = 10

        input_file_name = argv[1]
        output_file_name = argv[2][:-4] if len(argv[2]) > 4 else ""
        output_mode = argv[2][-3:] if len(argv[2]) > 3 else ""
    elif len(argv) == 6:
        sign_mode = int(argv[3])
        word_size = int(argv[4])
        base = int(argv[5])

        input_file_name = argv[1]
        output_file_name = argv[2][:-4] if len(argv[2]) > 4 else ""
        output_mode = argv[2][-3:] if len(argv[2]) > 3 else ""
    else: 
        # User entered the wrong number of args
        print("Usages:")
        print("python Jovial_Assembler.py [interactive mode - recommended]")
        print("python Jovial_Assembler.py <input file (.jov)> <output file (.16c/.txt/.pdf)> [assumes  2's complement, 16-bit, decimal]")
        print("python Jovial_Assembler.py <input file (.jov)> <output file (.16c/.txt/.pdf)> <sign mode (0/1/2/3)> <word size (4-64)> <base (2/8/10/16)>")
        sys.exit(1)

    # Check if arguments are valid
    if(not input_file_name.endswith(".jov")):
        print("Invalid file type. Please enter a .jov file.")
        sys.exit(1)
    if(output_mode != "16c" and output_mode != "pdf" and output_mode != "txt"):
        print("Invalid output mode. Please use either '.16c', '.pdf', or '.txt'.")
        sys.exit(1)
    if(sign_mode < 0 or sign_mode > 3):
        print("Invalid sign mode. Please use the sign mode (0 = Unsigned, 1 = 1's complement, 2 = 2's complement, 3 = floating point).")
        sys.exit(1)
    if(sign_mode == 3 and word_size != 56):
        # Just set the word size to 56 bits
        word_size = 56
    if(word_size < 4 or word_size > 64):
        print("Invalid word size. Please use a word size between 4 and 64 bits.")
        sys.exit(1)
    if(base != 2 and base != 8 and base != 10 and base != 16):
        print("Invalid base. Please use the base of the number being entered (2 = binary, 8 = octal, 10 = decimal, 16 = hexadecimal).")
        sys.exit(1)

    # Set the calculator state to the command line arguments
    calculator_state.sign_mode = sign_mode
    calculator_state.word_size = word_size
    calculator_state.update_base(base)
    calculator_state.input_file_name = input_file_name
    calculator_state.output_file_name = output_file_name
    calculator_state.output_mode = output_mode
