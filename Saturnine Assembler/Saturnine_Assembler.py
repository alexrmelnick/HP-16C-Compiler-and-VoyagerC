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
sign_mode = 2 # 0 = Unsigned, 1 = 1's complement, 2 = 2's complement
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
    for line in assembly_code:
        bare_line = parse_line(line)
        if(bare_line != None):
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
        print("Usage: python Saturnine_Assembler.py <input filename> <output file name> <output mode (16c/pdf)> <sign mode (0/1/2)> <word size (4-64)> <base (2/8/10/16)>")
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
    if(sign_mode < 0 or sign_mode > 2):
        print("Invalid sign mode. Please use the sign mode (0 = Unsigned, 1 = 1's complement, 2 = 2's complement).")
        sys.exit(1)
    if(word_size < 4 or word_size > 64):
        print("Invalid word size. Please use a word size between 4 and 64 bits.")
        sys.exit(1)
    if(base != 2 and base != 8 and base != 10 and base != 16):
        print("Invalid base. Please use the base of the number being entered (2 = binary, 8 = octal, 10 = decimal, 16 = hexadecimal).")
        sys.exit(1)

def parse_line(line):
    # Remove leading and trailing whitespace
    line = line.strip()

    # Check for comments and remove them
    if line.find("//") != -1:
        line = line[:line.find("//")]

    # Check for empty lines
    if len(line) == 0:
        return None

    # Separate the line into tokens
    tokens = line.split()





if __name__ == "__main__":
    main()