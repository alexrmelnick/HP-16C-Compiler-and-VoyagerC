import sys

from Calculator_State import CalculatorState

# Class definition for an input object
# This object will be used to store the input data
# Each line of the input file will be stored in an object of this class
# The object will have all of the necessary attributes to store the data and print it in the desired format, including pseudo-instructions
class instr:
    # Attributes
    # TODO Add more attributes to the class
    stripped_text = ""
    calculator_state = None # Calculator state
    input_line_number = 0 # Line number in the input file

    instruction_or_number = False # True if instruction, False if number
    pseudo_or_real = None # True if pseudo, False if real, None if neither
    has_argument = False

    tokens = [] # List of tokens in the line
    output_text = ""



    # Constructor
    # TODO: Write constructor
    def __init__(self, line, input_line_number, calculator_state):
        self.stripped_text = line
        self.input_line_number = input_line_number
        self.calculator_state = calculator_state

        


    # Methods
    # TODO: Write str method
    def __str__(self):
        pass

    def parse_number(self):
        # Parse the number and return the corresponding keypresses
        token_base = ""
        change_base = False
        change_mode = False
        negative = False
        negative_exponent = False
        is_float = False
        is_float_in_sci_notation = False

        acceptable_float_chars = "0123456789.e-"

        # Check if the number is negative
        if token[0] == "-":
            negative = True
            token = token[1:]

        # Check if the number is a floating point number
        if token.find(".") != -1:
            is_float = True

            # Check if we need to change the sign mode to floating point mode
            if (self.calculator_state.sign_mode == 0 or self.calculator_state.sign_mode == 1 or self.calculator_state.sign_mode == 2):
                change_mode = True
                self.calculator_state.previous_sign_mode = self.calculator_state.sign_mode
                self.calculator_state.sign_mode = 3
            
            # Check if the number is in scientific notation
            if token.find("e") != -1:
                is_float_in_sci_notation = True

            # Check if the number is valid
            if not is_valid_float(token):
                print("Invalid floating point number: " + token + "(line number )"+ input_line_number)
                sys.exit(1)

            # We have a valid floating point number
            if is_float_in_sci_notation:
                # Split the number into the mantissa and the exponent
                mantissa, exponent = token.split("e")
                if exponent[0] == "-":
                    negative_exponent = True
                    exponent = exponent[1:]
            
            # We are ready to print the keypresses

        else: # The number is an integer
            is_float = False

            # Check if we need to change the sign mode back to the previous mode
            if (self.calculator_state.sign_mode == 3):
                change_mode = True
                self.calculator_state.sign_mode = self.calculator_state.previous_sign_mode

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
                token_base = "DEC"

            if not is_valid_integer(token):
                print("Invalid integer: " + token + "(line number )"+ self.input_line_number)
                sys.exit(1)

            if token_base != self.calculator_state.base:
                change_base = True

            # We have a valid integer
            # We are ready to print the keypresses

        # Print the keypresses
        output_text = ""
        # For floats
        if (is_float and change_mode): # Switch to floating point mode
            output_text.append("f FLOAT\n")
            output_text.append(".\n")
            self.calculator_state.program_length += 2

            if(is_float_in_sci_notation): # Floating point number in scientific notation
                if(negative):
                    output_text.append(token + "\n")
                    output_text.append("CHS\n")
                    self.calculator_state.program_length += 2
                else:
                    output_text.append(token + "\n")
                    self.calculator_state.program_length += 1

                if(negative_exponent): 
                    output_text.append("f EEX\n")
                    output_text.append(exponent + "\n")
                    output_text.append("CHS\n")
                    self.calculator_state.program_length += 3
                else:
                    output_text.append("f EEX\n")
                    output_text.append(exponent + "\n")
                    self.calculator_state.program_length += 2

            else: # Floating point number
                if(negative):
                    output_text.append(token + "\n")
                    output_text.append("CHS\n")
                    self.calculator_state.program_length += 2
                else:
                    output_text.append(token + "\n")
                    self.calculator_state.program_length += 1

        elif (is_float): # Floating point number and already in floating point mode
            if(is_float_in_sci_notation): # Floating point number in scientific notation
                if(negative):
                    output_text.append(token + "\n")
                    output_text.append("CHS\n")
                    self.calculator_state.program_length += 2
                else:
                    output_text.append(token + "\n")
                    self.calculator_state.program_length += 1

                if(negative_exponent):
                    output_text.append("f EEX\n")
                    output_text.append(exponent + "\n")
                    output_text.append("CHS\n")
                    self.calculator_state.program_length += 3
                else:
                    output_text.append("f EEX\n")
                    output_text.append(exponent + "\n")
                    self.calculator_state.program_length += 2

            else: # Floating point number
                if(negative):
                    output_text.append(token + "\n")
                    output_text.append("CHS\n")
                    self.calculator_state.program_length += 2
                else:
                    output_text.append(token + "\n")
                    self.calculator_state.program_length += 1

        if(change_mode or change_base): # Switching from float to integer mode
                        #  OR already in integer mode, but changing the base
            output_text.append(self.base + "\n")
            self.calculator_state.program_length += 1

            if (negative):
                output_text.append(token + "\n")
                output_text.append("CHS\n")
                self.calculator_state.program_length += 2
            else:
                output_text.append(token + "\n")
                self.calculator_state.program_length += 1

        else: # Already in integer mode and base
            if (negative):
                output_text.append(token + "\n")
                output_text.append("CHS\n")
                self.calculator_state.program_length += 2
            else:
                output_text.append(token + "\n")
                self.calculator_state.program_length += 1

    def parse_instruction(self):
        # TODO: Write me
        pass


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