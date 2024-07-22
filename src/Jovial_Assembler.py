'''
Welcome to the Jovial Assembler! This program takes in a .jov file of Jovial Assembly and outputs either
a .16c file for importing into the JRPN HP-16C simulator or a .pdf file for printing. 

The Jovial Assembler is a single-pass assembler featuring:
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

The Jovial Assembler is written in Python 3.12.3 and developed by Alex Melnick.
'''

#!/usr/bin/env python3

# Imports
import math
import sys

from datetime import datetime
from Calculator_State import CalculatorState
from Instructions import instr
from Instructions_Data import mnemonic_to_instr, instructions_with_arguments
from Utils import is_number
from DEBUG import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

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
    if DEBUG: print("Opening file: " + calculator_state.input_file_name + " of type " + str(type(calculator_state.input_file_name)))
    input_file = open(calculator_state.input_file_name, "r") # Open the file in read mode
    assembly_code = input_file.readlines() # Read all the lines of the input file into a list
    input_file.close()

    # Assemble the code into "bare" keypress sequences
    for input_line_number, line in enumerate(assembly_code):
        # Parse the line and get the keypresses
        if DEBUG: print("Parsing line: ", line, " (line number: ", input_line_number+1, ")")
        parse_line(line, input_line_number+1, calculator_state)

        # Update the program length and memory partition
        calculator_state.update_program_length()
        calculator_state.update_memory()

        # Check if the program is too large for the memory
        if calculator_state.program_length > PRGM_MEMORY_AVAILABLE:
            print("Error - Out of Memory: This program is too large for the memory.")
            print("Memory overflowed at line " + str(input_line_number+1) + "(the HP-16C only has 203 Bytes of memory).")
            print("Remember, the best art is made under the tightest constraints!")
            sys.exit(1)


    # Output the assembled code in the desired format
    if(calculator_state.output_mode == "16c"):
        output_16c(calculator_state)
    elif(calculator_state.output_mode == "pdf"):
        output_pdf(calculator_state)

    # Return some useful information to the user
    print(f"Assembly complete! The program has been output to {calculator_state.output_file_name}.{calculator_state.output_mode}")    
    print("Stats:".ljust(80, '.'))
    print(f"Calculator status (at end of program): {calculator_state.sign_mode} mode, {calculator_state.word_size}-bit words, {calculator_state.base} base")
    print(f"Program length: {calculator_state.program_length} Bytes")
    print(f"Registers used: {len(calculator_state.registers_used)} registers of {calculator_state.available_registers} available")
    print(f"Memory partition @ {calculator_state.memory_partition} Bytes")

    if DEBUG: 
        print("DEBUG: Registers used:")
        for reg in calculator_state.registers_used:
            print(f"DEBUG: Register {reg} used.")


def parse_interactive(calculator_state):
    print("Welcome to the Jovial Assembler - the first and only assembler for the HP-16C calculator!")
    
    print("Please enter the name or path of the .jov file you would like to assemble.")
    input_file_name = input("File name: ")
    while not input_file_name.endswith(".jov"):
        print("Invalid file type. Please enter a .jov file.")
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
    calculator_state.update_base(base)
    calculator_state.input_file_name = input_file_name
    calculator_state.output_file_name = output_file_name
    calculator_state.output_mode = output_mode


def parse_cli(argv, calculator_state):
    # Check if the user has entered the correct number of arguments
    if len(argv) != 7:
        print("Usage: python Jovial_Assembler.py <input filename> <output file name (no extension)> <output mode (16c/pdf)> <sign mode (0/1/2/3)> <word size (4-64)> <base (2/8/10/16)>")
        sys.exit(1)
    
    # Parse the command line arguments
    input_file_name = argv[1]
    output_file_name = argv[2]
    output_mode = argv[3]
    sign_mode = int(argv[4])
    word_size = int(argv[5])
    base = int(argv[6])

    # Check if arguments are valid
    if(not input_file_name.endswith(".jov")):
        print("Invalid file type. Please enter a .jov file.")
        sys.exit(1)
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
    calculator_state.update_base(base)
    calculator_state.input_file_name = input_file_name
    calculator_state.output_file_name = output_file_name
    calculator_state.output_mode = output_mode


def parse_line(line, input_line_number, calculator_state):
    # Do some basic parsing of the line
    
    # Remove leading and trailing whitespace
    line = line.strip()

    # Check for comments and remove them
    # Check for double slashes and remove anything after them
    if line.find("//") != -1:
        line = line[:line.find("//")]
    # Check for semicolons and remove anything after them
    if line.find(";") != -1:
        line = line[:line.find(";")]

    # Check for empty lines
    if len(line) == 0:
        return None

    # Make the line lowercase
    line = line.lower()

    # Separate the line into tokens
    tokens = line.split()

    # Check if the token is an instruction or a number
    if DEBUG: print("Parsing tokens: ", tokens)
    if is_valid_instruction(tokens[0]):
        parse_instruction(tokens, input_line_number, calculator_state)
    # Check if the token is a number
    elif is_number(tokens[0]):
        parse_number(tokens[0], calculator_state, input_line_number)
    else:
        print("Invalid line: ", line, "(line number )", input_line_number)
        sys.exit(1)


def parse_instruction(tokens, input_line_number, calculator_state):
    if DEBUG: print("Parsing instruction: ", tokens[0])
    has_argument = False
    if (len(tokens) == 2):
        if DEBUG: print("Token: ", tokens[0], " has an argument: ", tokens[1])
        has_argument = True
    else:
        if DEBUG: print("Token: ", tokens[0], " has no argument.")

    # Check if the token is a valid instruction with a valid argument
    if(is_valid_instruction(tokens[0])):
        if(has_argument and is_valid_argument(tokens[0], tokens[1], calculator_state)):
            if DEBUG: print("Instr: ", tokens[0], " has a valid with argument: ", tokens[1])
            
            # Perform system checks
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
                        if int(tokens[1]) not in calculator_state.registers_used:
                            if DEBUG: print("Adding register: ", tokens[1], " to the list of registers used.")
                            calculator_state.registers_used.append(int(tokens[1]))
                
                calculator_state.update_memory()

            if DEBUG: print("Adding instruction: ", tokens[0], " with argument: ", tokens[1], " to the program.")
            calculator_state.program.append(instr(tokens[0], tokens[1], calculator_state))
        elif (has_argument and not is_valid_argument(tokens[0], tokens[1], calculator_state)):
            print("Error - Invalid argument:")
            print(f"Argument: {tokens[1]} is not valid for instruction: {tokens[0]}.")
            print(f"Line: {tokens} (line number: {input_line_number})")
            sys.exit(1)
        elif (not has_argument and tokens[0] in instructions_with_arguments):
            print("Error - Missing argument:")
            print(f"Instruction: {tokens[0]} requires an argument.")
            print(f"Line: {tokens} (line number: {input_line_number})")
            sys.exit(1)
        else:
            if tokens[0] == 'hex' or tokens[0] == 'dec' or tokens[0] == 'oct' or tokens[0] == 'bin': 
                if DEBUG: print("Changing base to: ", tokens[0])
                calculator_state.update_base(tokens[0])

            if DEBUG: print("Adding instruction: ", tokens[0], " with no argument to the program.")
            calculator_state.program.append(instr(tokens[0], None, calculator_state))
    else:
        print(f"Invalid instruction: {tokens[0]} (line number {input_line_number})")
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
    multiple_digits = False
    multiple_digits_exponent = False

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

        # Does the mantissa contain multiple digits?
        if len(mantissa) > 1:
            multiple_digits = True
        
        # Does the exponent contain multiple digits?
        if len(exponent) > 1:
            multiple_digits_exponent = True
        
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
            token_base = calculator_state.base

        if not is_valid_integer(token, calculator_state):
            print(f"Invalid integer: {token} (line number {input_line_number})")
            sys.exit(1)

        if token_base.lower() != calculator_state.base.lower():
            change_base = True

        token = token.upper()

        # Does the number contain multiple digits?
        if len(token) > 1:
            multiple_digits = True

        # We have a valid integer
        # We are ready to print the keypresses

    # For floats
    if (is_float and change_mode): # Switch to floating point mode
        calculator_state.program.append(instr("FLOAT", None, calculator_state))
        calculator_state.program.append(instr(".", None, calculator_state))
        calculator_state.program_length += 2

        if(is_float_in_sci_notation): # Floating point number in scientific notation
            if(negative):
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program.append(instr("CHS", None, calculator_state))
                calculator_state.program_length += 1
            else:
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1

            if(negative_exponent): 
                calculator_state.program.append(instr("EEX", None, calculator_state))
                for digit in exponent:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program.append(instr("CHS", None, calculator_state))
                calculator_state.program_length += 2
            else:
                calculator_state.program.append(instr("EEX", None, calculator_state))
                for digit in exponent:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program_length += 1

        else: # Floating point number
            if(negative):
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program.append(instr("CHS", None, calculator_state))
                calculator_state.program_length += 1
            else:
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1

    elif (is_float): # Floating point number and already in floating point mode
        if(is_float_in_sci_notation): # Floating point number in scientific notation
            if(negative):
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program.append(instr("CHS", None, calculator_state))
                calculator_state.program_length += 1
            else:
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1

            if(negative_exponent):
                calculator_state.program.append(instr("EEX", None, calculator_state))
                for digit in exponent:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program.append(instr("CHS", None, calculator_state))
                calculator_state.program_length += 2
            else:
                calculator_state.program.append(instr("EEX", None, calculator_state))
                for digit in exponent:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program_length += 1

        else: # Floating point number
            if(negative):
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program.append(instr("CHS", None, calculator_state))
                calculator_state.program_length += 1

            else:
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1

    if(change_mode or change_base): # Switching from float to integer mode
                    #  OR already in integer mode, but changing the base
        if DEBUG: print("Changing mode to: ", token_base)
        calculator_state.program.append(instr(token_base.upper(), None, calculator_state))
        calculator_state.program_length += 1

        if (negative):
            for digit in token:
                calculator_state.program.append(instr(digit, None, calculator_state))
                calculator_state.program_length += 1
            calculator_state.program.append(instr("CHS", None, calculator_state))
            calculator_state.program_length += 1
        else:
            for digit in token:
                calculator_state.program.append(instr(digit, None, calculator_state))
                calculator_state.program_length += 1

    else: # Already in integer mode and base
        if (negative):
            for digit in token:
                calculator_state.program.append(instr(digit, None, calculator_state))
                calculator_state.program_length += 1
            calculator_state.program.append(instr("CHS", None, calculator_state))
            calculator_state.program_length += 1
        else:
            for digit in token:
                calculator_state.program.append(instr(digit, None, calculator_state))
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
    if DEBUG: print("Token: ", token, " Base: ", calculator_state.base_numeric)
    try:
        num = int(token, calculator_state.base_numeric)
    except ValueError:
        # Handle the error, for example, by setting num to None or logging an error message
        num = None
        print(f"Error: '{token}' is not a valid number in base {calculator_state.base_numeric}")
        return False
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
    token = token.lower()

    for char in token:
        if char == "e":
            contains_e = True
        if char not in acceptable_float_chars:
            if is_valid_float_DEBUG: print("Invalid character: ", char)
            return False


    # Is the number within the range of a float?
    if contains_e:
        # The number is in scientific notation
        # Split the number into the mantissa and the exponent
        mantissa, exponent = token.split("e")
        if mantissa[0] == "-":
            mantissa = mantissa[1:]
        if exponent[0] == "-":
            exponent = exponent[1:]
        # if not is_valid_integer(mantissa, calculator_state):
        #     if is_valid_float_DEBUG: print("Invalid mantissa: ", mantissa)
        #     return False
        if DEBUG: print("Checking if exponent: ", exponent, " is valid.")
        if not is_valid_integer(exponent, calculator_state):
            if is_valid_float_DEBUG: print("Invalid exponent: ", exponent)
            return False
    num = float(mantissa) ** float(exponent)
    if num > 9.999999999 * 10**99 or num < -9.999999999 * 10**99:
        if is_valid_float_DEBUG: print("Number out of range: ", num)
        return False
    
    if is_valid_float_DEBUG: print("Valid floating point number: ", token)
    return True


def is_valid_instruction(instr):
    # Check if the instruction is valid
    if instr in mnemonic_to_instr:
        return True
    else:
        return False


def is_valid_argument(instr, arg, calculator_state):
    if DEBUG: print("Checking if argument: ", arg, " is valid for instruction: ", instr)
    
    # Check if the instruction takes an argument
    if instr not in instructions_with_arguments:
        if is_valid_argument_DEBUG: print("Instruction: ", instr, " does not take an argument.")
        return False
    if is_valid_argument_DEBUG: print("Instruction: ", instr, " takes an argument.")

    # Check if the argument is valid
    if(instr == 'sto' or instr == 'rcl'):
        if is_valid_argument_DEBUG: print("Checking if argument: ", arg, " is valid for a STO or RCL instruction.")
        
        # check if the argument is I or (i)
        if(arg == 'i' or arg == '(i)'):
            return True
        elif(arg.isdigit() and int(arg) >= 0 and int(arg) <= 31):
            return True
        else:
            return False
    elif(instr == 'sf' or instr == 'cf' or instr == 'f?'):
        if is_valid_argument_DEBUG: print("Checking if argument: ", arg, " is valid for a SF, CF, or F? instruction.")
        
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= 5):
            return True
        else:
            return False
    elif(instr == 'sb' or instr == 'cb' or instr == 'b?'):
        print("ERROR: Setting/Clearing/Testing a bit does not take an argument")
        sys.exit(1)
    elif(instr == 'lbl' or instr == 'gto' or instr == 'gsb'):
        if is_valid_argument_DEBUG: print("Checking if argument: ", arg, " is valid for a LBL, GTO, or GSB instruction.")
        
        if(arg.isdigit() and int(arg) >= 0 and int(arg) < 16):
            return True
        elif(arg in 'abcdef'):
            return True
        elif(arg == 'i' or arg == '(i)'):
            return True
        else:
            return False
    elif(instr == 'show'):
        if is_valid_argument_DEBUG: print("Checking if argument: ", arg, " is valid for a SHOW instruction.")
        
        if(arg == 'hex' or arg == 'dec' or arg == 'oct' or arg == 'bin'):
            return True
        else:
            return False
    elif(instr == 'float'):
        if is_valid_argument_DEBUG: print("Checking if argument: ", arg, " is valid for a FLOAT instruction.")
        
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= 9):
            return True
        elif(arg == '.'):
            return True
        else:
            return False
    elif(instr == 'window'):
        if is_valid_argument_DEBUG: print("Checking if argument: ", arg, " is valid for a WINDOW instruction.")
        
        # This doesn't exclude all invalid arguments, but this instruction will be used so rarely that it doesn't matter
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= 7):
            return True
        else:
            return False
    elif(instr == 'clear'):
        if is_valid_argument_DEBUG: print("Checking if argument: ", arg, " is valid for a CLEAR instruction.")
        
        if(arg == 'reg'):
            return True
        else:
            return False
    else:
        if is_valid_argument_DEBUG: print("Did not find a valid argument for instruction: ", instr)
        
        return False


def output_16c(calculator_state):
    # Update the state of the calculator
    calculator_state.update_memory()
    calculator_state.update_program_length()
    
    # Output the assembled code in the .16c format
    output_file = open(calculator_state.output_file_name + ".16c", "w") # Open the file in write mode

    # Write the header to the output file
    output_file.write("#  Program produced by Alex Melnick's Jovial Assembler.\n")
    output_file.write("#  Character encoding: UTF-8\n")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_file.write(f"#  Generated {current_time}\n")  # Corrected line
    output_file.write(f"#  Program occupies {calculator_state.program_length} bytes.\n\n")  # Corrected line

    # Write the first line of the output file (always the same)
    output_file.write("   000 {          } \n") # 10 spaces between the curly braces

    # Write the keypresses to the output file
    for line_number, line in enumerate(calculator_state.program):
        line_number_str = str(line_number + 1).zfill(3)
        if line.has_modifier and line.has_argument:
            output_line = f"   {line_number_str} {{ {line.modifier_position} {line.instruction_position} {line.argument_position} }} {line.modifier} {line.instruction} {line.argument}\n"
        elif line.has_modifier:
            output_line = f"   {line_number_str} {{    {line.modifier_position} {line.instruction_position} }} {line.modifier} {line.instruction}\n"
        elif line.has_argument:
            output_line = f"   {line_number_str} {{    {line.instruction_position} {line.argument_position} }} {line.instruction} {line.argument}\n"
        else:
            output_line = f"   {line_number_str} {{       {line.instruction_position} }} {line.instruction}\n"
        
        if DEBUG: print("Writing line: ", output_line)
        
        output_file.write(output_line)
    
    output_file.write("\n# End.\n")  # Write end statement to the output file

    # Close the output file
    output_file.close()


def output_pdf(calculator_state):
    # Parameters for the PDF
    font_name = "Dot Matrix" # Using a custom font for the program listing for a retro look
    font_path = "fonts/Dot-Matrix-Typeface-master/Dot Matrix Regular.TTF" # Thank you Daniel Hark for the font!
    line_spacing = 20  # Line spacing for the program listing

    c = canvas.Canvas(calculator_state.output_file_name + ".pdf", pagesize=LETTER)
    pdfmetrics.registerFont(TTFont(font_name, font_path))
    c.setFont(font_name, 12)  # Using Times-Roman font with size 12 because this is meant to be printed
    heading_y_position = 792 - 72  # 72 points (1 inch) from the top

    # Heading and Stats
    header = [
        f"Program Listing for {calculator_state.input_file_name} for the HP-16C Calculator",
        f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} with the Jovial Assembler by Alex Melnick",
        f"Calculator status (at end of program): {calculator_state.sign_mode} mode, {calculator_state.word_size}-bit words, {calculator_state.base} base",
        f"Program length: {calculator_state.program_length} Bytes",
        f"Registers used: {len(calculator_state.registers_used)} of {calculator_state.available_registers} available",
        f"Memory partition @ {calculator_state.memory_partition} Bytes"
    ]

    # Draw Heading and Stats
    for line in header:
        c.drawString(72, heading_y_position, line)
        heading_y_position -= line_spacing

    # Set the dash pattern for the line: 1 unit on, 3 units off
    c.setDash(1, 3)
    # Draw a line under the heading
    c.line(72, heading_y_position, 522, heading_y_position)
    heading_y_position -= line_spacing  # Move down for the next line

    # Column layout settings
    columns = [(72, heading_y_position), (228, heading_y_position), (384, heading_y_position)]  # Adjusted y position for columns start
    column_width = 200  # Not used in this example, but useful for text wrapping
    current_column = 0  # Start with the first column


    # Iterate over the program lines and add them to the PDF
    for line_number, line in enumerate(calculator_state.program, start=1):
        x_position, y_position = columns[current_column]
        line_content = f"{line_number-1:03}: {line}"  # Format line content
        c.drawString(x_position, y_position, line_content)
        y_position -= line_spacing  # Move down for the next line
        columns[current_column] = (x_position, y_position)  # Update the y position in the columns array

        # Check if we need to switch columns or pages
        if y_position < 72:  # Near the bottom of the page
            current_column += 1  # Move to the next column
            if current_column > 2:  # If beyond the third column, create a new page
                c.showPage()
                c.setFont(font_name, 12)
                current_column = 0  # Reset to the first column
                # Reset y position for the new column or page
                heading_y_position = 792 - 72  # 72 points (1 inch) from the top
                columns = [(72, heading_y_position), (228, heading_y_position), (384, heading_y_position)]  # Adjusted y position for columns start

    c.save()  # Save the PDF

if __name__ == "__main__":
    main()