import sys

from Calculator_State import CalculatorState
from Saturnine_Assembler import is_number
from Instructions_Data import *

# Class definition for an input object
# This object will be used to store the input data
# Each line of the input file will be stored in an object of this class
# The object will have all of the necessary attributes to store the data and print it in the desired format, including pseudo-instructions
class instr:
    # Attributes
    # TODO Add more attributes to the class
    calculator_state = None # Calculator state

    instruction_or_number = False # True if instruction, False if number
    pseudo_or_real = None # True if pseudo, False if real, None if neither
    has_argument = False
    has_modifier = False

    modifier = None # Modifier for the instruction
    instruction = None # Instruction
    argument = None # Argument for the instruction

    modifier_position = None # Position of the modifier in the instruction
    instruction_position = None # Position of the instruction in the instruction
    argument_position = None # Position of the argument in the instruction



    # Constructor
    # TODO: Write constructor
    def __init__(self, instr, calculator_state):
        self.calculator_state = calculator_state
        self.has_argument = False
        
        if(is_number(instr)):
            self.instruction_or_number = False
            self.pseudo_or_real = None
            self.has_modifier = False
        elif(is_instruction(instr)):
            self.instruction_or_number = True
        else:
            raise ValueError("Invalid instruction or number")
        
        if(self.instruction_or_number): # If the token is an instruction            
            # Check if the instruction has a modifier
            if(self.check_for_modifier() is not None):
                self.has_modifier = True
                self.modifier = self.check_for_modifier()

            self.instruction = self.check_for_instruction(instr) # Shouldn't matter than this is a string
            self.instruction_position = self.get_instruction_position()

        else: # If the token is a number
            self.instruction = instr
            self.instruction_position = instr
        if(self.has_modifier):
            self.modifier_position = self.get_modifier_position()


    def __init__(self, instr, arg, calculator_state):
        self.calculator_state = calculator_state
        self.has_argument = False
        self.instruction_or_number = True # Always an instruction if an argument is provided
        self.instruction = self.check_for_instruction(instr)
        self.argument = arg
            
        # Check if the instruction has a modifier
        if(self.check_for_modifier() is not None):
            self.has_modifier = True
            self.modifier = self.check_for_modifier()

        instruction_position = self.get_instruction_position()
        argument_position = self.get_argument_position()
        if(self.has_modifier):
            self.modifier_position = self.get_modifier_position()


    # Methods
    # TODO: Write str method
    def __str__(self):
        #TODO Implement me
        return "WIP"

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


# Utility functions
def is_valid_argument(instr, arg, word_size):
    # Check if the instruction takes an argument
    # TODO: IMPLEMENT ME
    
    # Check if the argument is valid
    if(instr == 'sto' or instr == 'rcl'):
        # check if the argument is I or (i)
        if(arg == 'i' or arg == '(i)'):
            return True
        elif(arg.isdigit() and int(arg) >= 0 and int(arg) <= 31):
            return True
        else:
            return False
    elif(instr == 'sf' or instr == 'cf' or 'f?'):
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= 5):
            return True
        else:
            return False
    elif(instr == 'sb' or instr == 'cb' or 'b?'):
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= word_size):
            return True
        else:
            return False
    elif(instr == 'lbl' or instr == 'gto' or instr == 'gsb'):
        if(arg.isdigit() and int(arg) >= 0 and int(arg) < 16):
            return True
        elif(arg in 'abcdef'):
            return True
        else:
            return False
    elif(instr == 'show'):
        if(arg == 'hex' or arg == 'dec' or arg == 'oct' or arg == 'bin'):
            return True
        else:
            return False
    elif(instr == 'float'):
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= 9):
            return True
        elif(arg == '.'):
            return True
        else:
            return False
    elif(instr == 'window'):
        # This doesn't exclude all invalid arguments, but this instruction will be used so rarely that it doesn't matter
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= 7):
            return True
        else:
            return False
    elif(instr == 'clear'):
        if(arg == 'mem'):
            return True
        else:
            return False
    else:
        return False


def is_instruction(instr):
    if instr in instruction_list:
        return True
    return False


