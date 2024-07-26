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

# Imports
import sys
import logging

from Calculator_State import CalculatorState
from Output import *
from Parse_Command import *
from Parser import *

# CONSTANTS
PRGM_MEMORY_AVAILABLE = 203 # Number of bytes available in memory for the program

def main():
    # Set up logging configuration
    myLevel = logging.DEBUG
    myFormat = logging.Formatter('%(levelname)s - %(filename)s - %(funcName)s - %(message)s')
    
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(myLevel)
    console_handler.setFormatter(myFormat)
    
    # Get the root logger and set its level and handler
    logger = logging.getLogger()
    logger.setLevel(myLevel)
    logger.addHandler(console_handler)

    input_file = None # File object for the input file
    calculator_state = CalculatorState(2, 16, 10) # Create a new instance of the CalculatorState class with default values

    # Determine if in CLI mode or interactive mode, then parse accordingly
    if(len(sys.argv) == 1):
        parse_interactive(calculator_state)
    else:
        parse_cli(sys.argv, calculator_state)

    # Open the input file, read it, then close it
    logging.info(f"Opening file: {calculator_state.input_file_name} of type {str(type(calculator_state.input_file_name))}")
    input_file = open(calculator_state.input_file_name, "r") # Open the file in read mode
    assembly_code = input_file.readlines() # Read all the lines of the input file into a list
    input_file.close()

    # Assemble the code into "bare" keypress sequences
    for input_line_number, line in enumerate(assembly_code):
        # Parse the line and get the keypresses
        adjusted_line_no = input_line_number+1
        logging.info(f"Parsing line: {line} (line number: {adjusted_line_no}")
        parse_line(line, input_line_number+1, calculator_state)

        # Update the program length and memory partition
        calculator_state.update_program_length()
        calculator_state.update_memory()

        # Check if the program is too large for the memory
        if calculator_state.program_length > PRGM_MEMORY_AVAILABLE:
            logging.critical("Error - Out of Memory: This program is too large for the memory.")
            logging.critical(f"Memory overflowed at line {adjusted_line_no} (the HP-16C only has 203 Bytes of memory).")
            logging.critical("Remember, the best art is made under the tightest constraints!")
            sys.exit(1)


    # Output the assembled code in the desired format
    if(calculator_state.output_mode == "16c"):
        output_16c(calculator_state)
    elif(calculator_state.output_mode == "txt"):
        output_txt(calculator_state)
    elif(calculator_state.output_mode == "pdf"):
        output_pdf(calculator_state)

    # Return some useful information to the user
    print(f"Assembly complete! The program has been output to {calculator_state.output_file_name}.{calculator_state.output_mode}")    
    print("Stats:".ljust(80, '.'))
    print(f"Calculator status (at end of program): {calculator_state.sign_mode} mode, {calculator_state.word_size}-bit words, {calculator_state.base} base")
    print(f"Program length: {calculator_state.program_length} Bytes")
    print(f"Registers used: {len(calculator_state.registers_used)} registers of {calculator_state.available_registers} available")
    print(f"Memory partition @ {calculator_state.memory_partition} Bytes")

    logging.debug("Registers used:")
    for reg in calculator_state.registers_used:
        logging.debug(f"DEBUG: Register {reg} used.")

if __name__ == "__main__":
    main()