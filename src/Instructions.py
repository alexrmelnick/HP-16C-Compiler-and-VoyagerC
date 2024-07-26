import sys
import logging

from Calculator_State import CalculatorState
from Utils import is_number
from Instructions_Data import *

# Class definition for an input object
# This object will be used to store the input data
# Each line of the input file will be stored in an object of this class
# The object will have all of the necessary attributes to store the data and print it in the desired format, including pseudo-instructions
class instr:
    # Attributes
    calculator_state = None # Calculator state

    instruction_or_number = False # True if instruction, False if number
    has_argument = False
    has_modifier = False

    modifier = None # Modifier for the instruction
    instruction = None # Instruction
    argument = None # Argument for the instruction

    modifier_position = None # Position of the modifier in the instruction
    instruction_position = None # Position of the instruction in the instruction
    argument_position = None # Position of the argument in the instruction


    def __init__(self, instr, arg, calculator_state):
        logging.debug(f"Creating instruction object with instruction: {instr} and argument: {arg}")
        
        self.calculator_state = calculator_state
        self.has_argument = False
        self.instruction_or_number = True # Always an instruction if an argument is provided
        if arg is not None and is_number(arg):
            if arg in 'abcdef':
                self.argument = arg.upper()
            else:
                self.argument = arg       
        else:
            self.argument = arg
        # Check is argument is not None

        if(self.argument is None):
            if(is_number(instr)): # If the token is a number
                logging.debug(f"Validating number: {instr} with no argument and getting position.")
                self.instruction_or_number = False
                self.has_modifier = False
                self.instruction = instr
                self.instruction_position = instr
            else: # If the token is an instruction
                logging.debug(f"Validating instruction: {instr} with no argument and getting position.")
                self.instruction = self.check_for_instruction(instr)
                self.instruction_position = self.get_instruction_position()
        else: # If the token is an instruction with an argument
            logging.debug(f"Validating instruction: {instr} with argument: {arg} and getting position.")
            self.instruction = self.check_for_instruction(instr)
            self.instruction_position = self.get_instruction_position()
            self.instruction_or_number = True
            self.has_argument = True
            self.argument_position = self.get_argument_position()


        # Check if the instruction has a modifier
        if(self.check_for_modifier() is not None):
            self.has_modifier = True
            self.modifier = self.check_for_modifier()

        if(self.has_modifier):
            self.modifier_position = self.get_modifier_position()

        logging.debug(f"Instruction object created with instruction: {self.instruction} and argument: {self.argument} and modifier: {self.modifier}")


    # Methods
    # def __str__(self): # For printing to pdf
    #     if self.has_modifier and self.has_argument:
    #         return f"{self.modifier} {self.instruction} {self.argument}"
    #     elif self.has_modifier:
    #         return f"{self.modifier} {self.instruction}"
    #     elif self.has_argument:
    #         return f"{self.instruction} {self.argument}"
    #     else:
    #         return f"{self.instruction}"
    def __str__(self):
        if self.has_modifier and self.has_argument:
            output_line = f"{self.modifier_position},{self.instruction_position:>2}, {self.argument_position:3}| {self.modifier} {self.instruction} {self.argument}"
        elif self.has_modifier:
            output_line = f"{self.modifier_position} {self.instruction_position:7}| {self.modifier} {self.instruction}"
        elif self.has_argument:
            output_line = f"{self.instruction_position} {self.argument_position:7}| {self.instruction} {self.argument}"
        else:
            output_line = f"{self.instruction_position:10}| {self.instruction}"

        logging.debug(output_line)
        return output_line

    def check_for_instruction(self, mnemonic):
        mnemonic = mnemonic.lower()
        if mnemonic in mnemonic_to_instr:
            logging.debug(f"Mnemonic: {mnemonic} is valid. Instruction: {mnemonic_to_instr[mnemonic]}")
            return mnemonic_to_instr[mnemonic]
        else:
            logging.critical(f"Error: Invalid mnemonic. {mnemonic} is not a valid mnemonic.")
            sys.exit(1)

    def check_for_modifier(self):
        if self.instruction_or_number == False: # If the token is a number
            return None
        elif self.instruction in f_modifier_instrs:
            return 'f'
        elif self.instruction in g_modifier_instrs:
            return 'g'
        else:
            return None

    def get_instruction_position(self):
        logging.debug(f"Getting instruction position for: {self.instruction} (with argument: {self.argument})")
        if self.instruction_or_number == False: # If the token is a number
            return self.instruction
        elif self.instruction in button_positions:
            return button_positions[self.instruction]
        elif self.instruction == "SHOW":
            logging.debug(f"SHOW instruction: {self.instruction}, {self.argument}")
            if self.argument == "hex": return 23
            elif self.argument == "dec": return 24
            elif self.argument == "oct": return 25
            elif self.argument == "bin": return 26
            else:
                logging.critical("Failed to find instruction position - SHOW passed with invalid argument")
                sys.exit(1)
        elif self.instruction == "CLEAR":
            if self.argument == "reg": return 34
            else: 
                logging.critical("Failed to find instruction position - CLEAR passed with invalid argument")
                sys.exit(1)
        else:
            raise ValueError("Failed to find instruction position")
    
    def get_argument_position(self):
        logging.debug(f"Getting argument position for: {self.argument}")
        if is_number(self.argument):
            logging.debug("Argument is a number")
            if self.instruction == 'STO' or self.instruction == 'RCL':
                logging.debug(f"Returning argument position for a register: {self.argument}")
                self.convert_index()
            if self.argument in 'abcdef':
                logging.debug(f"Returning argument position for a hexadecimal digit: {self.argument.upper()}")
                return button_positions[self.argument.upper()]
            else:
                logging.debug(f"Returning argument position for digit: {self.argument}")
                return self.argument
        elif self.argument == 'hex' or self.argument == 'dec' or self.argument == 'oct' or self.argument == 'bin' or self.argument == 'reg':
            logging.debug(f"Special instruction argument: {self.instruction}, {self.argument}")
            pos = button_positions[self.argument.upper()]
            if self.instruction == 'SHOW':
                self.instruction = 'SHOW ' + self.argument.upper()
                self.instruction_position = pos
            elif self.instruction == 'CLEAR':
                self.instruction = 'CLEAR ' + self.argument.upper()
                self.instruction_position = pos
            else:
                logging.critical("Reached an invalid special instruction argument - this should not happen")
            self.argument = None
            self.has_argument = False
            return None
        elif self.argument == 'i': # Make sure that I is always uppercase
            self.argument = 'I'
            return button_positions[self.argument]
        elif self.argument in button_positions:
            logging.debug(f"Returning argument position: {button_positions[self.argument]}")
            return button_positions[self.argument]
        else:
            logging.critical("Failed to find argument position")
            sys.exit(1)
    
    def get_modifier_position(self):
        if self.modifier == 'f':
            return 42
        elif self.modifier == 'g':
            return 43
        else:
            return ValueError("Invalid modifier")
        
    def convert_index(self):
        number = int(self.argument)
        if 0 <= number <= 9:
            self.argument = str(number)
            self.argument_position = str(number)
        elif 10 <= number <= 15:
            self.argument = chr(number - 10 + ord('A'))
            self.argument_position = chr(number - 10 + ord('A'))
        elif 16 <= number <= 25:
            self.argument = '1' + str(number - 16)
            self.argument_position = '.' + str(number - 16)
        elif 26 <= number <= 31:
            self.argument = '1' + chr(number - 26 + ord('A'))
            self.argument_position = '.' + chr(number - 26 + ord('A'))
        else:
            logging.critical("Error: Invalid register index. Must be between 0 and 31")
            logging.critical(f"Line: {self.instruction, self.argument}")
            sys.exit(1)