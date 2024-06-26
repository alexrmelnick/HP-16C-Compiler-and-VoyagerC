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

# Global variables and their default values
sign_mode = 2 # 0 = Unsigned, 1 = 1's complement, 2 = 2's complement, 3 = floating point
previous_sign_mode = 2 # Previous sign mode (necessary for floating point numbers because int sign mode is saved)
word_size = 16 # Number of bits in a word
base = 16 # Base of the number being entered (2 = binary, 8 = octal, 10 = decimal, 16 = hexadecimal)

input_file_name = None # Input file
input_file = None # File object for the input file

output_file_name = None # Output file
output_mode = None # Output mode (16c or pdf)

bare_keypresses = [] # List of keypress lines

program_length = 0 # Length of the program in bytes
registers_used = 0 # Number of registers used
memory_available = 203 # Number of bytes available in memory

def main():
    # Determine if in CLI mode or interactive mode, then parse accordingly
    if(len(sys.argv) == 1):
        parse_interactive()
    else:
        parse_cli(sys.argv)

    # Open the input file, read it, then close it
    input_file = open(input_file_name, "r") # Open the file in read mode
    assembly_code = input_file.readlines() # Read all the lines of the input file into a list
    input_file.close()

    # Assemble the code into "bare" keypress sequences
    for input_line_number, line in enumerate(assembly_code):
        bare_line = parse_line(line, input_line_number)
        if bare_line != None:
            bare_keypresses.append(bare_line)

    # Output the assembled code in the desired format
    #TODO

    # Return some useful information to the user
    #TODO

def parse_interactive():
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
    sign_mode = int(input("Sign mode (0, 1, or 2): "))
    while(sign_mode < 0 or sign_mode > 2):
        print("Invalid sign mode. Please enter the sign mode (0 = Unsigned, 1 = 1's complement, 2 = 2's complement).")
        sign_mode = int(input("Sign mode: "))

    print("Enter the word size (number of bits in a word) between 4 bits and 64 bits.")
    print("If you are unsure, enter 16 for the standard word size. It has a good balance of register size and memory usage.")
    word_size = int(input("Word size: "))
    while(word_size < 4 or word_size > 64):
        print("Invalid word size. Please enter a word size between 4 and 64 bits.")
        word_size = int(input("Word size: "))

    print("Enter the starting base of the number being entered (2 = binary, 8 = octal, 10 = decimal, 16 = hexadecimal).")
    print("If you are unsure, enter 10 for decimal. It is the most common base for entering numbers.")
    base = int(input("Base: "))
    while(base != 2 and base != 8 and base != 10 and base != 16):
        print("Invalid base. Please enter the base of the number being entered (2 = binary, 8 = octal, 10 = decimal, 16 = hexadecimal).")
        base = int(input("Base: "))

def parse_cli(argv):
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

def parse_line(line, input_line_number):
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

    # Determine the format of the line
    # Should be 3 options:
        # 1. An instruction with an argument
        # 2. An instruction with no argument
        # 3. A number
    if len(tokens) == 1:
        # Check if the token is an instruction (easier to check for instructions first because they are predefined)
        if is_instruction(tokens[0]):
            return parse_instruction(tokens[0])
        # Check if the token is a number
        if is_number(tokens[0]):
            return parse_number(tokens[0], input_line_number)
        else:
            print("Invalid line: " + line + "(line number )"+ input_line_number)
            return None
    elif len(tokens) == 2:
        # Check if the first token is an instruction
        if is_instruction(tokens[0]):
            # Check if the second token is a valid argument
            if is_argument(tokens[1]):
                return parse_instruction(tokens[0], tokens[1])
            else:
                print("Invalid line: " + line + "(line number )"+ input_line_number)
                return None
        else:
            print("Invalid line: " + line + "(line number )"+ input_line_number)
            return None
    else:
        print("Invalid line: " + line + "(line number )"+ input_line_number)
        return None
    
def is_number(token):
    # Check if the token is a number

    # Does token contain any characters other than -,.,0-9,A-F,a-f,b,o,x?
    acceptable_chars = "0123456789abcdefbox-."

    for char in token:
        if(char not in acceptable_chars):
            return False

    # Does token contain more than one decimal point?
    if token.count(".") > 1:
        return False
    
    # Does token contain more than two negative signs?
    if token.count("-") > 2:
        return False
    
    # Does token contain more than one binary, octal, or hexadecimal prefix?
    if token.count("0b") > 1 or token.count("0o") > 1 or token.count("0x") > 1:
        return False
    
    # Does token contain more than one base prefix?
    if token.count("b") > 1 or token.count("o") > 1 or token.count("x") > 1:
        return False
    
    # Does token contain a prefix and a decimal point (floats are always base 10)?
    if (token.find("0b") != -1 and token.find(".")) or (token.find("0b") != -1 and token.find(".")) or (token.find("0x") != -1 and token.find(".")) or (token.find("0d") != -1 and token.find(".")):
        return False

    return True

def is_number_test():
    print("Testing is_number() function...")
    print("1234:", is_number("1234"))
    print("0x1234:", is_number("0x1234"))
    print("0b1010:", is_number("0b1010"))
    print("0o1234:", is_number("0o1234"))
    print("1234.0:", is_number("1234.0"))
    print("1234.5:", is_number("1234.5"))
    print("1234.5.6:", is_number("1234.5.6"))
    print("0x1234.5:", is_number("0x1234.5"))
    print("0b1010.1:", is_number("0b1010.1"))
    print("0o1234.2:", is_number("0o1234.2"))
    print("0x1234.5.6:", is_number("0x1234.5.6"))
    print("-1234:", is_number("-1234"))
    print("-0x1234:", is_number("-0x1234"))
    print("-0b1010:", is_number("-0b1010"))
    print("-0o1234:", is_number("-0o1234"))
    print("-1234.0:", is_number("-1234.0"))
    print("-1234.5:", is_number("-1234.5"))
    print("-1234.5.6:", is_number("-1234.5.6"))
    print("-0x1234.5:", is_number("-0x1234.5"))
    print("-0b1010.1:", is_number("-0b1010.1"))
    print("-0o1234.2:", is_number("-0o1234.2"))
    print("-0x1234.5.6:", is_number("-0x1234.5.6"))

def parse_number(token, input_line_number):
    # Parse the number and return the corresponding keypresses
    token_base = 0
    change_base = False
    change_mode = False
    negative = False
    negative_exponent = False
    is_float = False
    is_float_in_sci_notation = False

    acceptable_float_chars = "0123456789.e-"

    # Check if the number is negative
    if token[0] == "-":
        negative = True
        token = token[1:]

    # Check if the number is a floating point number
    if token.find(".") != -1:
        is_float = True

        # Check if we need to change the sign mode to floating point mode
        if (sign_mode == 0 or sign_mode == 1 or sign_mode == 2):
            change_mode = True
            previous_sign_mode = sign_mode
            sign_mode = 3
        
        # Check if the number is in scientific notation
        if token.find("e") != -1:
            is_float_in_sci_notation = True

        # Check if the number is valid
        if not is_valid_float(token):
            print("Invalid floating point number: " + token + "(line number )"+ input_line_number)
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
        if (sign_mode == 3):
            change_mode = True
            sign_mode = previous_sign_mode

        # Determine the base of the number
        if token.find("0x") != -1:
            token_base = 16
            token = token[2:] # Remove the "0x" prefix
        elif token.find("0b") != -1:
            token_base = 2
            token = token[2:] # Remove the "0b" prefix
        elif token.find("0o") != -1:
            token_base = 8
            token = token[2:] # Remove the "0o" prefix
        elif token.find("0d") != -1:
            token_base = 10
            token = token[2:] # Remove the "0d" prefix
        else:
            token_base = 10

        if not is_valid_integer(token):
            print("Invalid integer: " + token + "(line number )"+ input_line_number)
            sys.exit(1)

        if token_base != base:
            change_base = True

        # We have a valid integer
        # We are ready to print the keypresses

    # Print the keypresses
    # For floats
    if (is_float and change_mode): # Switch to floating point mode
        bare_keypresses.append("f FLOAT\n")
        bare_keypresses.append(".\n")
        program_length += 2

        if(is_float_in_sci_notation): # Floating point number in scientific notation
            if(negative):
                bare_keypresses.append(token + "\n")
                bare_keypresses.append("CHS\n")
                program_length += 2
            else:
                bare_keypresses.append(token + "\n")
                program_length += 1

            if(negative_exponent): 
                bare_keypresses.append("f EEX\n")
                bare_keypresses.append(exponent + "\n")
                bare_keypresses.append("CHS\n")
                program_length += 3
            else:
                bare_keypresses.append("f EEX\n")
                bare_keypresses.append(exponent + "\n")
                program_length += 2

        else: # Floating point number
            if(negative):
                bare_keypresses.append(token + "\n")
                bare_keypresses.append("CHS\n")
                program_length += 2
            else:
                bare_keypresses.append(token + "\n")
                program_length += 1

    elif (is_float): # Floating point number and already in floating point mode
        if(is_float_in_sci_notation): # Floating point number in scientific notation
            if(negative):
                bare_keypresses.append(token + "\n")
                bare_keypresses.append("CHS\n")
                program_length += 2
            else:
                bare_keypresses.append(token + "\n")
                program_length += 1

            if(negative_exponent):
                bare_keypresses.append("f EEX\n")
                bare_keypresses.append(exponent + "\n")
                bare_keypresses.append("CHS\n")
                program_length += 3
            else:
                bare_keypresses.append("f EEX\n")
                bare_keypresses.append(exponent + "\n")
                program_length += 2

        else: # Floating point number
            if(negative):
                bare_keypresses.append(token + "\n")
                bare_keypresses.append("CHS\n")
                program_length += 2
            else:
                bare_keypresses.append(token + "\n")
                program_length += 1

    if(change_mode or change_base): # Switching from float to integer mode
                    #  OR already in integer mode, but changing the base
        bare_keypresses.append(base + "\n")
        program_length += 1

        if (negative):
            bare_keypresses.append(token + "\n")
            bare_keypresses.append("CHS\n")
            program_length += 2
        else:
            bare_keypresses.append(token + "\n")
            program_length += 1

    else: # Already in integer mode and base
        if (negative):
            bare_keypresses.append(token + "\n")
            bare_keypresses.append("CHS\n")
            program_length += 2
        else:
            bare_keypresses.append(token + "\n")
            program_length += 1

def is_valid_integer(token):
    # Check if the number is valid
    # Does the token contain the correct characters for the base?
    acceptable_hex_chars = "0123456789abcdef"
    acceptable_dec_chars = "0123456789"
    acceptable_oct_chars = "01234567"
    acceptable_bin_chars = "01"

    if base == 16:
        for char in token:
            if char not in acceptable_hex_chars:
                return False
    elif base == 10:
        for char in token:
            if char not in acceptable_dec_chars:
                return False
    elif base == 8:
        for char in token:
            if char not in acceptable_oct_chars:
                return False
    elif base == 2:
        for char in token:
            if char not in acceptable_bin_chars:
                return False

    # Is the number within the range of the word size?
    num = int(num,base)
    if num < 0:
        return False
    if num >= 2 ** word_size:
        return False
    
    return True

def is_valid_float(token):
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
        if not is_valid_integer(mantissa):
            return False
        if not is_valid_integer(exponent):
            return False
    num = mantissa ^ exponent
    if num > 9.999999999 * 10^99 or num < -9.999999999 * 10^99:
        return False
    
    return True

if __name__ == "__main__":
    main()