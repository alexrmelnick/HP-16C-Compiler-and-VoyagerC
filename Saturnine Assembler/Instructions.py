import sys

from Calculator_State import CalculatorState
from Utils import is_number
from Instructions_Data import *
from DEBUG import DEBUG 

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



    # Constructor
    # def __init__(self, instr, calculator_state):
    #     self.calculator_state = calculator_state
    #     self.has_argument = False
        
    #     if(is_number(instr)):
    #         self.instruction_or_number = False
    #         self.has_modifier = False
    #     else:
    #         self.instruction_or_number = True

        
    #     if(self.instruction_or_number): # If the token is an instruction            
    #         # Check if the instruction has a modifier
    #         if(self.check_for_modifier() is not None):
    #             self.has_modifier = True
    #             self.modifier = self.check_for_modifier()

    #         self.instruction = self.check_for_instruction(instr) # Shouldn't matter than this is a string
    #         self.instruction_position = self.get_instruction_position()

    #     else: # If the token is a number
    #         self.instruction = instr
    #         self.instruction_position = instr
    #     if(self.has_modifier):
    #         self.modifier_position = self.get_modifier_position()


    def __init__(self, instr, arg, calculator_state):
        if DEBUG: print("Creating instruction object with instruction: ", instr, " and argument: ", arg)
        
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
                if DEBUG: print("Validating number: ", instr, " with no argument and getting position.")
                self.instruction_or_number = False
                self.has_modifier = False
                self.instruction_position = instr
            else: # If the token is an instruction
                if DEBUG: print("Validating instruction: ", instr, " with no argument and getting position.")
                self.instruction = self.check_for_instruction(instr)
                self.instruction_position = self.get_instruction_position()
        else: # If the token is an instruction with an argument
            if DEBUG: print("Validating instruction: ", instr, " with argument: ", arg, " and getting position.")
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

        if DEBUG: print("Instruction object created with instruction: ", self.instruction, " and argument: ", self.argument, " and modifier: ", self.modifier)


    # Methods
    def check_for_instruction(self, mnemonic):
        if mnemonic in mnemonic_to_instr:
            if DEBUG: print("Mnemonic: ", mnemonic, " is valid. Instruction: ", mnemonic_to_instr[mnemonic],".")
            return mnemonic_to_instr[mnemonic]
        else:
            print("Error: Invalid mnemonic. ", mnemonic, " is not a valid mnemonic.")
            raise ValueError("Invalid mnemonic")

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
        if DEBUG: print("Getting instruction position for: ", self.instruction)
        if self.instruction_or_number == False: # If the token is a number
            return self.instruction
        elif self.instruction in button_positions:
            return button_positions[self.instruction]
        else:
            print("Error: Invalid instruction. ", self.instruction, " is not a valid instruction.")
            raise ValueError("Invalid instruction")
    
    def get_argument_position(self):
        if is_number(self.argument):
            if self.argument in 'abcdef':
                return self.argument.upper()
            else:
                return self.argument
        elif self.argument in button_positions:
            return button_positions[self.argument]
        else:
            raise ValueError("Invalid argument")
    
    def get_modifier_position(self):
        if self.modifier == 'f':
            return 42
        elif self.modifier == 'g':
            return 43
        else:
            return ValueError("Invalid modifier")
