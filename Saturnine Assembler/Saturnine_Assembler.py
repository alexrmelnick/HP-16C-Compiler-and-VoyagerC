'''
Welcome to the Saturnine Assembler! This program takes in a .sat file of Saturnine Assembly and outputs either
a .16c file for importing into the JRPN HP-16C simulator or a .pdf file for printing. 

The Saturnine Assembler is a single-pass assembler featuring:
- A simple and intuitive syntax based on the sample programs in the HP-16C manual.
- A comprehensive instruction set that covers all of the operations available on the HP-16C calculator.
- Support for comments using a `//` prefix.
- Support for automatic assembly of the `f` and `g` modifier keys.
- Ability to specify the base of the number being entered (binary, octal, decimal, or hexadecimal).
- Ability to use negative numbers as an immediate.
- Ability to enter floating point numbers in scientific notation.
- Support for optionally specifying the initial mode settings for the calculator.
- Warnings for carry and out-of-range errors and other issues if the initial mode settings are supplied. 
- Support for throwing errors if the program is too large for the memory.
- Support for throwing errors if addresses are out of range.
- Support for directly addressing the first 32 storage registers in decimal.
- Support for detecting if subroutines are nested more than 4 levels deep.
- Support for pseudo-instructions to simplify certain operations.

The Saturnine Assembler is written in Python 3.12.3 and developed by Alex Melnick.
'''

# Imports
import math
import sys

from datetime import datetime
from Calculator_State import CalculatorState
from Instructions import instr
from Instructions_Data import *
from Utils import is_number

# CONSTANTS
PRGM_MEMORY_AVAILABLE = 203 # Number of bytes available in memory for the program

def main():
    input_file = None # File object for the input file
    calculator_state = CalculatorState(2, 16, 10) # Create a new instance of the CalculatorState class with default values

    # Determine if in CLI mode or interactive mode, then parse accordingly
    if(len(sys.argv) == 1):
        parse_interactive(calculator_state)
    else:
        parse_cli(sys.argv, calculator_state)

    # Open the input file, read it, then close it
    input_file = open(CalculatorState.input_file_name, "r") # Open the file in read mode
    assembly_code = input_file.readlines() # Read all the lines of the input file into a list
    input_file.close()

    # Assemble the code into "bare" keypress sequences
    for input_line_number, line in enumerate(assembly_code):
        # Parse the line and get the keypresses
        parse_line(line, input_line_number, calculator_state)

        # Check if the program is too large for the memory
        if calculator_state.program_length > PRGM_MEMORY_AVAILABLE:
            print("Error - Out of Memory: This program is too large for the memory.")
            print("Memory overflowed at line " + str(input_line_number) + "(the HP-16C only has 203 Bytes of memory).")
            print("Remember, the best art is made under the tightest constraints!")
            sys.exit(1)


    # Output the assembled code in the desired format
    if(calculator_state.output_mode == "16c"):
        output_16c(calculator_state)
    elif(calculator_state.output_mode == "pdf"):
        output_pdf(calculator_state)

    # Return some useful information to the user
    print("Assembly complete! The program has been output to " + calculator_state.output_file_name + "." + calculator_state.output_mode)
    print("Stats:")
    print("Calculator status: " + calculator_state.sign_mode + " mode, " + calculator_state.word_size + " bit words, " + calculator_state.base + " base")
    print("Program length: " + calculator_state.program_length + " bytes")
    print("Registers used: " + calculator_state.registers_used.length + " registers of " + calculator_state.available_registers + " available")
    print("Memory partition: " + calculator_state.memory_partition + " bytes")


def parse_interactive(calculator_state):
    print("Welcome to the Saturnine Assembler - the first and only assembler for the HP-16C calculator!")
    
    print("Please enter the name or path of the .sat file you would like to assemble.")
    input_file_name = input("File name: ")
    while not input_file_name.endswith(".sat"):
        print("Invalid file type. Please enter a .sat file.")
        input_file_name = input("File name: ")
    
    print("Please enter the name of the output file you would like to create.")
    output_file_name = input("Output file name: ")
    
    print("Would you like to output a .16c file for the HP-16C simulator or a printable .pdf?")
    output_mode = input("Output mode (16c/pdf): ")
    while(output_mode != "16c" and output_mode != "pdf"):
        print("Invalid output mode. Please enter either '16c' or 'pdf'.")
        output_mode = input("Output mode (16c/pdf): ")

    print("Please enter the initial settings for the calculator.")

    print("Enter the sign mode (0 = Unsigned, 1 = 1's complement, 2 = 2's complement).")
    print("If you are unsure, enter 0 for unsigned mode or 2 if you want to use signed numbers.")
    # Checking if sign_mode input is a number
    while True:
        try:
            sign_mode = int(input("Sign mode (0 = Unsigned, 1 = 1's complement, 2 = 2's complement): "))
            if 0 <= sign_mode <= 2:
                break  # Exit loop if input is a valid number within range
            else:
                print("Invalid sign mode. Please enter a valid number (0, 1, or 2).")
        except ValueError:
            print("Please enter a number.")

    print("Enter the word size (number of bits in a word) between 4 bits and 64 bits.")
    print("If you are unsure, enter 16 for the standard word size. It has a good balance of register size and memory usage.")
    while True:
        try:
            word_size = int(input("Word size (between 4 bits and 64 bits): "))
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
    calculator_state.base_numeric = base
    calculator_state.update_base()
    calculator_state.input_file_name = input_file_name
    calculator_state.output_file_name = output_file_name
    calculator_state.output_mode = output_mode


def parse_cli(argv, calculator_state):
    # Check if the user has entered the correct number of arguments
    if len(argv) != 6:
        print("Usage: python Saturnine_Assembler.py <input filename> <output file name> <output mode (16c/pdf)> <sign mode (0/1/2/3)> <word size (4-64)> <base (2/8/10/16)>")
        sys.exit(1)
    
    # Parse the command line arguments
    input_file_name = argv[1]
    output_file_name = argv[2]
    output_mode = argv[3]
    sign_mode = int(argv[4])
    word_size = int(argv[5])
    base = int(argv[6])

    # Check if arguments are valid
    if(output_mode != "16c" and output_mode != "pdf"):
        print("Invalid output mode. Please use either '16c' or 'pdf'.")
        sys.exit(1)
    if(sign_mode < 0 or sign_mode > 3):
        print("Invalid sign mode. Please use the sign mode (0 = Unsigned, 1 = 1's complement, 2 = 2's complement, 3 = floating point).")
        sys.exit(1)
    if(sign_mode == 3 and word_size != 56):
        print("Invalid word size. Floating point numbers must be 56 bits.")
        sys.exit(1)
    if(word_size < 4 or word_size > 64):
        print("Invalid word size. Please use a word size between 4 and 64 bits.")
        sys.exit(1)
    if(base != 2 and base != 8 and base != 10 and base != 16):
        print("Invalid base. Please use the base of the number being entered (2 = binary, 8 = octal, 10 = decimal, 16 = hexadecimal).")
        sys.exit(1)

    # Set the calculator state to the command line arguments
    calculator_state.sign_mode = sign_mode
    calculator_state.word_size = word_size
    calculator_state.base_numeric = base
    calculator_state.update_base()
    calculator_state.input_file_name = input_file_name
    calculator_state.output_file_name = output_file_name
    calculator_state.output_mode = output_mode


def parse_line(line, input_line_number, calculator_state):
    # Do some basic parsing of the line
    
    # Remove leading and trailing whitespace
    line = line.strip()

    # Check for comments and remove them
    if line.find("//") != -1:
        line = line[:line.find("//")]

    # Check for empty lines
    if len(line) == 0:
        return None

    # Make the line lowercase
    line = line.lower()

    # Separate the line into tokens
    tokens = line.split()

    # Check if the token is an instruction or a number
    if is_valid_instruction(tokens[0]):
        parse_instruction(tokens, input_line_number, calculator_state)
    # Check if the token is a number
    elif is_number(tokens[0]):
        parse_number(tokens[0], calculator_state, input_line_number)
    else:
        print("Invalid line: " + line + "(line number )"+ input_line_number)
        sys.exit(1)


def parse_instruction(tokens, input_line_number, calculator_state):
    has_argument = False
    if (len(tokens) == 2):
        has_argument = True

    # Check if the token is a valid instruction with a valid argument
    if(is_valid_instruction(tokens[0])):
        if(has_argument and is_valid_argument(tokens[0], tokens[1], calculator_state)):
            # Perform memory checks
            if tokens[0] == 'sto' or tokens[0] == 'rcl':
                if tokens[1] != 'i' and tokens[1] != '(i)':
                    if int(tokens[1]) > 31:
                        print("Error - Out of direct memory range:")
                        print("Addresses must be between 0 and 31 for direct addressing.")
                        print("Line: " + tokens + " (line number: " + input_line_number + " )")
                        sys.exit(1)
                    elif(int(tokens[1])*calculator_state.word_size/8 >= calculator_state.memory_partition):
                        print("Error - Out of memory range:")
                        print("Addresses must be within the memory partition.")
                        print("Line: " + tokens + " (line number: " + input_line_number + " )")
                        sys.exit(1)
                    else:
                        if tokens[1] not in calculator_state.registers_used:
                            calculator_state.registers_used.append(int(tokens[1]))
                
                calculator_state.update_memory()

            calculator_state.program.append(instr(tokens[0], tokens[1], calculator_state))
        else:
            calculator_state.program.append(instr(tokens[0], calculator_state))
    else:
        print("Invalid instruction: " + tokens[0] + "(line number )"+ input_line_number)
        sys.exit(1)


def parse_number(token, calculator_state, input_line_number):
    # Parse the number and return the corresponding keypresses
    token_base = ""
    change_base = False
    change_mode = False
    negative = False
    negative_exponent = False
    is_float = False
    is_float_in_sci_notation = False

    # Check if the number is negative
    if token[0] == "-":
        negative = True
        token = token[1:]

    # Check if the number is a floating point number
    if token.find(".") != -1:
        is_float = True

        # Check if we need to change the sign mode to floating point mode
        if (calculator_state.sign_mode == 0 or calculator_state.sign_mode == 1 or calculator_state.sign_mode == 2):
            change_mode = True
            calculator_state.previous_sign_mode = calculator_state.sign_mode
            calculator_state.sign_mode = 3
        
        # Check if the number is in scientific notation
        if token.find("e") != -1:
            is_float_in_sci_notation = True

        # Check if the number is valid
        if not is_valid_float(token, calculator_state):
            print("Invalid floating point number: " + token + "(line number )"+ calculator_state.input_line_number)
            sys.exit(1)

        # We have a valid floating point number
        if is_float_in_sci_notation:
            # Split the number into the mantissa and the exponent
            mantissa, exponent = token.split("e")
            if exponent[0] == "-":
                negative_exponent = True
                exponent = exponent[1:]
        
        # We are ready to print the keypresses

    else: # The number is an integer
        is_float = False

        # Check if we need to change the sign mode back to the previous mode
        if (calculator_state.sign_mode == 3):
            change_mode = True
            calculator_state.sign_mode = calculator_state.previous_sign_mode

        # Determine the base of the number
        if token.find("0x") != -1:
            token_base = "HEX"
            token = token[2:] # Remove the "0x" prefix
        elif token.find("0b") != -1:
            token_base = "BIN"
            token = token[2:] # Remove the "0b" prefix
        elif token.find("0o") != -1:
            token_base = "OCT"
            token = token[2:] # Remove the "0o" prefix
        elif token.find("0d") != -1:
            token_base = "DEC"
            token = token[2:] # Remove the "0d" prefix
        else:
            token_base = "DEC"

        if not is_valid_integer(token, calculator_state):
            print("Invalid integer: " + token + "(line number )"+ input_line_number)
            sys.exit(1)

        if token_base != calculator_state.base:
            change_base = True

        # We have a valid integer
        # We are ready to print the keypresses

    # For floats
    if (is_float and change_mode): # Switch to floating point mode
        calculator_state.program.append(instr("FLOAT", calculator_state))
        calculator_state.program.append(instr(".", calculator_state))
        calculator_state.program_length += 2

        if(is_float_in_sci_notation): # Floating point number in scientific notation
            if(negative):
                calculator_state.program.append(instr(token, calculator_state))
                calculator_state.program.append(instr("CHS", calculator_state))
                calculator_state.program_length += 2
            else:
                calculator_state.program.append(instr(token, calculator_state))
                calculator_state.program_length += 1

            if(negative_exponent): 
                calculator_state.program.append(instr("EEX", calculator_state))
                calculator_state.program.append(instr(exponent, calculator_state))
                calculator_state.program.append(instr("CHS", calculator_state))
                calculator_state.program_length += 3
            else:
                calculator_state.program.append(instr("EEX", calculator_state))
                calculator_state.program.append(instr(exponent, calculator_state))
                calculator_state.program_length += 2

        else: # Floating point number
            if(negative):
                calculator_state.program.append(instr(token, calculator_state))
                calculator_state.program.append(instr("CHS", calculator_state))
                calculator_state.program_length += 2
            else:
                calculator_state.program.append(instr(token, calculator_state))
                calculator_state.program_length += 1

    elif (is_float): # Floating point number and already in floating point mode
        if(is_float_in_sci_notation): # Floating point number in scientific notation
            if(negative):
                calculator_state.program.append(instr(token, calculator_state))
                calculator_state.program.append(instr("CHS", calculator_state))
                calculator_state.program_length += 2
            else:
                calculator_state.program.append(instr(token, calculator_state))
                calculator_state.program_length += 1

            if(negative_exponent):
                calculator_state.program.append(instr("EEX", calculator_state))
                calculator_state.program.append(instr(exponent, calculator_state))
                calculator_state.program.append(instr("CHS", calculator_state))
                calculator_state.program_length += 3
            else:
                calculator_state.program.append(instr("EEX", calculator_state))
                calculator_state.program.append(instr(exponent, calculator_state))
                calculator_state.program_length += 2

        else: # Floating point number
            if(negative):
                calculator_state.program.append(instr(token, calculator_state))
                calculator_state.program.append(instr("CHS", calculator_state))
                calculator_state.program_length += 2

            else:
                calculator_state.program.append(instr(token, calculator_state))
                calculator_state.program_length += 1

    if(change_mode or change_base): # Switching from float to integer mode
                    #  OR already in integer mode, but changing the base
        calculator_state.program.append(instr(calculator_state.base, calculator_state))
        calculator_state.program_length += 1

        if (negative):
            calculator_state.program.append(instr(token, calculator_state))
            calculator_state.program.append(instr("CHS", calculator_state))
            calculator_state.program_length += 2
        else:
            calculator_state.program.append(instr(token, calculator_state))
            calculator_state.program_length += 1

    else: # Already in integer mode and base
        if (negative):
            calculator_state.program.append(instr(token, calculator_state))
            calculator_state.program.append(instr("CHS", calculator_state))
            calculator_state.program_length += 2
        else:
            calculator_state.program.append(instr(token, calculator_state))
            calculator_state.program_length += 1


def is_valid_integer(token, calculator_state):
    # Check if the number is valid
    # Does the token contain the correct characters for the base?
    acceptable_hex_chars = "0123456789abcdef"
    acceptable_dec_chars = "0123456789"
    acceptable_oct_chars = "01234567"
    acceptable_bin_chars = "01"

    if calculator_state.base == 16:
        for char in token:
            if char not in acceptable_hex_chars:
                return False
    elif calculator_state.base == 10:
        for char in token:
            if char not in acceptable_dec_chars:
                return False
    elif calculator_state.base == 8:
        for char in token:
            if char not in acceptable_oct_chars:
                return False
    elif calculator_state.base == 2:
        for char in token:
            if char not in acceptable_bin_chars:
                return False

    # Is the number within the range of the word size?
    num = int(num, calculator_state.base_numeric)
    if num < 0:
        return False
    if num >= 2 ** calculator_state.word_size:
        return False
    
    return True


def is_valid_float(token, calculator_state):
    # Check if the number is valid
    # Does the token contain the correct characters for a floating point number?
    acceptable_float_chars = "0123456789.e-"
    contains_e = False

    for char in token:
        if char == "e":
            contains_e = True
        if char not in acceptable_float_chars:
            return False


    # Is the number within the range of a float?
    if contains_e:
        # The number is in scientific notation
        # Split the number into the mantissa and the exponent
        mantissa, exponent = token.split("e")
        if not is_valid_integer(mantissa, calculator_state):
            return False
        if not is_valid_integer(exponent, calculator_state):
            return False
    num = mantissa ^ exponent
    if num > 9.999999999 * 10^99 or num < -9.999999999 * 10^99:
        return False
    
    return True


def is_valid_instruction(instr):
    # Check if the instruction is valid
    if instr in mnemonic_to_instr:
        return True
    else:
        return False


def is_valid_argument(instr, arg, calculator_state):
    # Check if the instruction takes an argument
    if instr not in instructions_with_arguments:
        return False
    
    # Check if the argument is valid
    if(instr == 'sto' or instr == 'rcl'):
        # check if the argument is I or (i)
        if(arg == 'i' or arg == '(i)'):
            return True
        elif(arg.isdigit() and int(arg) >= 0 and int(arg) <= 31):
            return True
        else:
            return False
    elif(instr == 'sf' or instr == 'cf' or 'f?'):
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= 5):
            return True
        else:
            return False
    elif(instr == 'sb' or instr == 'cb' or 'b?'):
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= calculator_state.word_size):
            return True
        else:
            return False
    elif(instr == 'lbl' or instr == 'gto' or instr == 'gsb'):
        if(arg.isdigit() and int(arg) >= 0 and int(arg) < 16):
            return True
        elif(arg in 'abcdef'):
            return True
        else:
            return False
    elif(instr == 'show'):
        if(arg == 'hex' or arg == 'dec' or arg == 'oct' or arg == 'bin'):
            return True
        else:
            return False
    elif(instr == 'float'):
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= 9):
            return True
        elif(arg == '.'):
            return True
        else:
            return False
    elif(instr == 'window'):
        # This doesn't exclude all invalid arguments, but this instruction will be used so rarely that it doesn't matter
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= 7):
            return True
        else:
            return False
    elif(instr == 'clear'):
        if(arg == 'mem'):
            return True
        else:
            return False
    else:
        return False


def output_16c(calculator_state):
    # Output the assembled code in the .16c format
    output_file = open(calculator_state.output_file_name + ".16c", "w") # Open the file in write mode

    # Write the header to the output file
    output_file.write("#  Program produced by Alex Melnick's Saturnine Assembler.\n")
    output_file.write("#  Character encoding: UTF-8\n")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_file.write("#  Generated "+current_time+"\n") # Write the current date and time to the output file
    output_file.write("# Program occupies " + calculator_state.program_length + " bytes.\n\n")

    # Write the first line of the output file (always the same)
    output_file.write("   000 {          } \n") # 10 spaces between the curly braces

    # Write the keypresses to the output file
    for line_number, line in enumerate(calculator_state.program):
        output_file.write("   "+str(line_number+1).zfill(3)+" { ")

        if line.has_modifier and line.has_argument:
            output_file.write(line.modifier_position + " " + line.instruction_position + " " + line.argument_position + " } " + line.modifier + " " + line.instruction + " " + line.argument + "\n")
        elif line.has_modifier:
            output_file.write("   " + line.modifier_position + " " + line.instruction_position + " } " + line.modifier + " " + line.instruction + "\n")
        elif line.has_argument:
            output_file.write("   " + line.instruction_position + " " + line.argument_position + " } " + line.instruction + " " + line.argument + "\n")
        else:
            output_file.write("      " + line.instruction_position + " } " + line.instruction + "\n")

    output_file.write("\n# End.\n") # Write end statement to the output file

    # Close the output file
    output_file.close()


def output_pdf(calculator_state):
    # TODO: Learn how to output as a pdf
    # TODO: Write this function
    pass

if __name__ == "__main__":
    main()