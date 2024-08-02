import logging
import sys
import argparse
import textwrap

def parse_arguments(calculator_state):
    # Set up parser
    parser = argparse.ArgumentParser(
        prog='jovial', 
        description='My description (WIP)',
        epilog='If no arguments are provided, the program will run in interactive mode.',
        formatter_class=argparse.RawTextHelpFormatter
        )

    parser.add_argument('-i', '--input_file', 
        #required=True, 
        help='Input file to assemble with .jov extension (required)', 
        type=str,
        # Eventually gonna add nargs='+' to allow multiple input files
        )  # Input file argument
    parser.add_argument('-o', '--output_file',
        #required=True, 
        help=textwrap.dedent('''\
        Output file with desired extension format (.pdf/.16c/.txt) (required)  
        .pdf = printable PDF file for typing into a physical HP-16C calculator  
        .16c = 16C file for the JRPN Simulator (not that this file is not compatible with the HP16C Emulator, despite the identical file extension)  
        .txt = TXT file for the HP16C Emulator (select filetype 'HP16C Program Text' when loading the file)  
        '''), 
        type=str,
        )  # Output file argument
    parser.add_argument('-s', '--sign_mode', 
        type=int, 
        choices=[0, 1, 2, 3], 
        #default=2, 
        #help = 'HP-16C starting sign mode (0 = Unsigned, 1 = 1\'s complement, 2 = 2\'s complement, 3 = floating point) (default = 2)',
        help = 'HP-16C starting sign mode (0 = Unsigned, 1 = 1\'s complement, 2 = 2\'s complement, 3 = floating point)',
        ) # Sign mode argument
    parser.add_argument('-w', '--word_size',
        type=int, 
        choices=range(4, 65), 
        metavar='{4-64}',
        #default=16,
        #help='HP-16C starting word size (number of bits in a word) between 4 bits and 64 bits (default = 16)',
        help='HP-16C starting word size (number of bits in a word) between 4 bits and 64 bits',
        ) # Word size argument
    parser.add_argument(
        '-b', '--base', 
        type=int, 
        choices=[2, 8, 10, 16], 
        #default=10,
        #help='Starting base of the number being entered (2 = binary, 8 = octal, 10 = decimal, 16 = hexadecimal) (default = 10) (note that base must be 10 for floating point numbers)',
        help='Starting base of the number being entered (2 = binary, 8 = octal, 10 = decimal, 16 = hexadecimal)',
        ) # Base argument
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.2.0',   #! This is where the version number is set
        ) # Version argument
    parser.add_argument(
        '-d', '--debug',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Set the logging level (default = INFO)',
        ) # Debug argument
    
    # Parse the arguments
    args = parser.parse_args()

    # Determine if in CLI mode or interactive mode, then parse accordingly
    if len(sys.argv) == 1:
        parse_interactive(calculator_state)
    else:
        print(args)
        calculator_state.input_file_name = args.input_file if args.input_file is not None else ""
        calculator_state.output_file_name = args.output_file[:-4] if (args.output_file is not None and len(args.output_file)) > 4 else ""
        calculator_state.output_mode = args.output_file[-3:] if (args.output_file is not None and len(args.output_file) > 3) else ""
        calculator_state.sign_mode = args.sign_mode
        calculator_state.word_size = args.word_size
        calculator_state.update_base(args.base)
        calculator_state.logger_level = args.debug

        # Do some error checking
        if calculator_state.input_file_name == "":
            logging.critical("No input file provided. Please provide an input file.")
            sys.exit(1)
        if not calculator_state.input_file_name.endswith(".jov"):
            logging.critical("Invalid input file type. Please enter a .jov file.")
            sys.exit(1)
        if calculator_state.output_mode == "":
            logging.critical("No output file provided. Please provide an output file.")
            sys.exit(1)
        if calculator_state.output_mode not in ["16c", "pdf", "txt"]:
            logging.critical("Invalid output file type. Please use either '.16c', '.pdf', or '.txt'.")
            sys.exit(1)

        if calculator_state.sign_mode == 3 and calculator_state.word_size != 56:
            logging.warning("Floating point mode selected. Word size automatically set to 56 bits.")
            calculator_state.word_size = 56
        if calculator_state.sign_mode != 3 and calculator_state.base != 10:
            logging.warning("Floating point mode selected. Base automatically set to 10.")
            calculator_state.update_base(10)

def parse_interactive(calculator_state):
    print("Welcome to the Jovial Assembler - the first and only assembler for the HP-16C calculator!")
    
    print("Please enter the name or path of the .jov file you would like to assemble.")
    input_file_name = input("File name: ").strip()
    while not input_file_name.endswith(".jov"):
        print("Invalid file type. Please enter a .jov file.")
        input_file_name = input("File name: ")
    
    print("Please enter the name of the output file with the desired extension format (.pdf/.16c/.txt).")
    temp = input("Output file name: ").strip()
    # Extract file extension and file name
    output_mode = temp[-4:].lower() if len(temp) > 4 else ""
    output_file_name = temp[:-4] if len(temp) > 4 else ""
    while output_mode not in [".16c", ".pdf", ".txt"]:
        print("Invalid output file name. Please enter either a file with a '.16c','.pdf', or '.txt' extension.")
        temp = input("Output file name: ").strip()
        output_mode = temp[-4:].lower() if len(temp) > 4 else ""
        output_file_name = temp[:-4] if len(temp) > 4 else ""
    output_mode = output_mode[1:]  # trim the '.' from output mode
    logging.debug(f"Output mode determined: {output_mode}")
    logging.debug(f"Output file name: {output_file_name}")

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