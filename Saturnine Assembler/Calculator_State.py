# Class to represent the state of the calculator

PRGM_MEMORY_AVAILABLE = 203 # Number of bytes available in memory for the program

class CalculatorState:
    # Attributes
    # Calculator state
    sign_mode = 2 # 0 = Unsigned, 1 = 1's complement, 2 = 2's complement, 3 = floating point
    previous_sign_mode = 2 # Previous sign mode (necessary for floating point numbers because int sign mode is saved)
    word_size = 16 # Number of bits in a word
    base = "DEC" # Base of the number being entered (2 = binary, 8 = octal, 10 = decimal, 16 = hexadecimal)
    base_numeric = 10

    # Program state
    program_length = 0 # Length of the program in bytes
    registers_used = 0 # Number of registers used
    memory_partition = PRGM_MEMORY_AVAILABLE # Partition between program and data memory - trying to address memory over this value will throw an error
    program = [] # Array of instruction objects representing the program

    # Assembler state
    input_file_name = None # Input file
    output_file_name = None # Output file
    output_mode = None # Output mode (16c or pdf)

    # Methods
    def __init__(self): # Default constructor for the class
        pass
    def __init__(self, sign_mode, word_size, base):
        self.sign_mode = sign_mode
        self.word_size = word_size
        self.base = base

    def __str__(self): # For debugging
        return f"Sign mode: {self.sign_mode}, Word size: {self.word_size}, Base: {self.base}, Program length: {self.program_length}, Registers used: {self.registers_used}, Memory partition: {self.memory_partition}"
    
    def update_base(self):
        if self.base_numeric == 2:
            self.base = "BIN"
        elif self.base_numeric == 8:
            self.base = "OCT"
        elif self.base_numeric == 10:
            self.base = "DEC"
        elif self.base_numeric == 16:
            self.base = "HEX"
        else:
            raise ValueError("Invalid base value")