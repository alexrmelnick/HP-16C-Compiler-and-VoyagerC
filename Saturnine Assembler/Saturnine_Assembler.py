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

input_file_name = None # Input file
input_file = None # File object for the input file

output_file_name = None # Output file
output_mode = None # Output mode (16c or pdf)

def main():
    # Determine if in CLI mode or interactive mode, then parse accordingly
    if(len(sys.argv) == 1):
        parse_interactive()
    else:
        parse_cli()

    # Open the input file, read it, then close it
    input_file = open(input_file_name, "r") # Open the file in read mode
    assembly_code = input_file.readlines() # Read all the lines of the input file into a list
    input_file.close()

    # Open the output file
    if output_mode == "16c":
        output_file_name = output_file_name + ".16c"
        output_file = open(output_file_name, "w")
        assemble_16c(assembly_code)
    else:
        output_file_name = output_file_name + ".pdf"
        output_file = open(output_file_name, "w")
        assemble_pdf(assembly_code)

    # Close the output file
    output_file.close()



def assemble_16c(assembly_code):
    # TODO: Implement the assembly process for the HP-16C simulator
    total_lines = 0
    registers_available = 203 / ()


def assemble_pdf(assembly_code):
    #TODO: Figure out how to output a printable .pdf file
    print("PDF output is not yet supported. If you know how to output a .pdf file, please let me know!")

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

def parse_cli():
    # Check if the user has entered the correct number of arguments
    if len(sys.argv) != 6:
        print("Usage: python Saturnine_Assembler.py <input filename> <output file name> <output mode (16c/pdf)> <sign mode (0/1/2)> <word size (4-64)>")
        sys.exit(1)
    
    # Parse the command line arguments
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    output_mode = sys.argv[3]
    sign_mode = int(sys.argv[4])
    word_size = int(sys.argv[5])

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






if __name__ == "__main__":
    main()