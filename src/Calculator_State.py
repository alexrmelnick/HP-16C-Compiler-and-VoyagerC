import math
import sys
import logging


# Class to represent the state of the calculator

PRGM_MEMORY_AVAILABLE = 203 # Number of bytes available in memory for the program

class CalculatorState:
    # Attributes
    # Calculator state
    sign_mode = None # 0 = Unsigned, 1 = 1's complement, 2 = 2's complement, 3 = floating point
    previous_sign_mode = None # Previous sign mode (necessary for floating point numbers because int sign mode is saved)
    word_size = None # Number of bits in a word
    base = None # Base of the number being entered (2 = binary, 8 = octal, 10 = decimal, 16 = hexadecimal)
    base_numeric = None

    # Program state
    program_length = 0 # Length of the program in bytes
    registers_used = [] # Number of registers used
    available_registers = 406 # Number of registers available
    memory_partition = PRGM_MEMORY_AVAILABLE # Partition between program and data memory in bytes
    program = [] # Array of instruction objects representing the program


    # Assembler state
    input_file_name = None # Input file
    output_file_name = None # Output file
    output_mode = None # Output mode (16c or pdf)
    logger_level = logging.DEBUG

    # Methods
    def __init__(self):
        pass

    def __str__(self): # For debugging
        return f"Sign mode: {self.sign_mode}, Word size: {self.word_size}, Base: {self.base}, Program length: {self.program_length}, Registers used: {self.registers_used}, Memory partition: {self.memory_partition}"
    
    def update_base(self, new_base):
        if new_base is None:
            self.base = None
            self.base_numeric = None
            logging.debug("Base not set")
        elif new_base == 2 or new_base == "bin":
            self.base = "bin"
            self.base_numeric = 2
        elif new_base == 8 or new_base == "oct":
            self.base = "oct"
            self.base_numeric = 8
        elif new_base == 10 or new_base == "dec":
            self.base = "dec"
            self.base_numeric = 10
        elif new_base == 16 or new_base == "hex":
            self.base = "hex"
            self.base_numeric = 16
        else:
            raise ValueError("Invalid base value")

    def update_memory(self):
        if self.word_size is not None:
            self.available_registers = math.ceil((PRGM_MEMORY_AVAILABLE - self.program_length) / math.ceil((self.word_size/8)))

            self.memory_partition = PRGM_MEMORY_AVAILABLE - math.ceil(self.program_length / 7) * 7 # Round up program length to nearest multiple of 7

            if (len(self.registers_used) > self.available_registers):
                logging.critical("Error: Attempting to use more registers than available")
                sys.exit(1)
        else:
            logging.debug("Word size not set")
            self.available_registers = None

    def update_program_length(self):
        self.program_length = len(self.program)