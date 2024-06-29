import sys

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
        self.calculator_state = calculator_state
        self.has_argument = False
        self.instruction_or_number = True # Always an instruction if an argument is provided
        self.instruction = self.check_for_instruction(instr)
        self.argument = arg
        
        # Check is argument is not None
        if(self.argument is None):
            if(is_number(instr)):
                self.instruction_or_number = False
                self.has_modifier = False
                self.instruction_position = instr
        else:
            self.instruction_or_number = True
            self.has_argument = True
            self.argument_position = self.get_argument_position()


        # Check if the instruction has a modifier
        if(self.check_for_modifier() is not None):
            self.has_modifier = True
            self.modifier = self.check_for_modifier()

        self.instruction_position = self.get_instruction_position()
        if(self.has_modifier):
            self.modifier_position = self.get_modifier_position()


    # Methods
    def check_for_instruction(self, mnemonic):
        if mnemonic in mnemonic_to_instr:
            return mnemonic_to_instr[mnemonic]
        else:
            raise ValueError("Invalid mnemonic")

    def check_for_modifier(self):
        if self.instruction in f_modifier_instrs:
            return 'f'
        elif self.instruction in g_modifier_instrs:
            return 'g'
        else:
            return None

    def get_instruction_position(self):
        if self.instruction in button_positions:
            return button_positions[self.instruction]
        else:
            raise ValueError("Invalid instruction")
    
    def get_argument_position(self):
        if self.argument in button_positions:
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
