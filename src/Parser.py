import logging
import sys

from Instructions import instr
from Instructions_Data import mnemonic_to_instr, instructions_with_arguments
from Utils import is_number

# FIXME: Fix a bug that causes this to switch to decimal mode

def parse_line(line, input_line_number, calculator_state):
    # Do some basic parsing of the line
    
    # Remove leading and trailing whitespace
    line = line.strip()

    # Check for comments and remove them
    # Check for double slashes and remove anything after them
    if line.find("//") != -1:
        line = line[:line.find("//")]
    # Check for semicolons and remove anything after them
    if line.find(";") != -1:
        line = line[:line.find(";")]

    # Check for empty lines
    if len(line) == 0:
        return None

    # Make the line lowercase
    line = line.lower()

    # Separate the line into tokens
    tokens = line.split()

    # Check if the token is an instruction or a number
    logging.debug(f"Parsing tokens: {tokens}")
    if is_valid_instruction(tokens[0]):
        parse_instruction(tokens, input_line_number, calculator_state)
    # Check if the token is a number
    elif is_number(tokens[0]):
        parse_number(tokens[0], calculator_state, input_line_number)
    else:
        logging.critical(f"Invalid line: {line} (line number {input_line_number})")
        sys.exit(1)


def parse_instruction(tokens, input_line_number, calculator_state):
    logging.debug(f"Parsing instruction: {tokens[0]}")
    has_argument = False
    if (len(tokens) == 2):
        logging.debug(f"Token: {tokens[0]} has an argument: {tokens[1]}")
        has_argument = True
    else:
        logging.debug(f"Token: {tokens[0]} has no argument.")

    # Check if the token is a valid instruction with a valid argument
    if(is_valid_instruction(tokens[0])):
        if(has_argument and is_valid_argument(tokens[0], tokens[1])):
            logging.debug(f"Instr: {tokens[0]} has a valid with argument: {tokens[1]}")
            
            # Perform system checks
            if tokens[0] == 'sto' or tokens[0] == 'rcl':
                if tokens[1] != 'i' and tokens[1] != '(i)':
                    if int(tokens[1]) > 31:
                        logging.critical("Error - Out of direct memory range:")
                        logging.critical("Addresses must be between 0 and 31 for direct addressing.")
                        logging.critical(f"Line: {tokens} (line number: {input_line_number})")
                        sys.exit(1)
                    elif(int(tokens[1])*calculator_state.word_size/8 >= calculator_state.memory_partition):
                        logging.critical("Error - Out of memory range:")
                        logging.critical("Addresses must be within the memory partition.")
                        logging.critical(f"Line: {tokens} (line number: {input_line_number})")
                        sys.exit(1)
                    else:
                        if int(tokens[1]) not in calculator_state.registers_used:
                            logging.debug(f"Adding register: {tokens[1]} to the list of registers used.")
                            calculator_state.registers_used.append(int(tokens[1]))
                
                calculator_state.update_memory()

            logging.info(f"Adding instruction: {tokens[0]} with argument: {tokens[1]} to the program.")
            calculator_state.program.append(instr(tokens[0], tokens[1], calculator_state))
        elif (has_argument and not is_valid_argument(tokens[0], tokens[1])):
            logging.critical("Error - Invalid argument:")
            logging.critical(f"Argument: {tokens[1]} is not valid for instruction: {tokens[0]}.")
            logging.critical(f"Line: {tokens} (line number: {input_line_number})")
            sys.exit(1)
        elif (not has_argument and tokens[0] in instructions_with_arguments):
            logging.critical("Error - Missing argument:")
            logging.critical(f"Instruction: {tokens[0]} requires an argument.")
            logging.critical(f"Line: {tokens} (line number: {input_line_number})")
            sys.exit(1)
        else:
            if tokens[0] == 'hex' or tokens[0] == 'dec' or tokens[0] == 'oct' or tokens[0] == 'bin': 
                logging.debug(f"Changing base to: {tokens[0]}")
                calculator_state.update_base(tokens[0])

            logging.info(f"Adding instruction: {tokens[0]} with no argument to the program.")
            calculator_state.program.append(instr(tokens[0], None, calculator_state))
    else:
        logging.critical(f"Invalid instruction: {tokens[0]} (line number {input_line_number})")
        sys.exit(1)


def parse_number(token, calculator_state, input_line_number):
    # Parse the number and return the corresponding keypresses
    token_base = ""
    change_base = False
    change_mode = False
    negative = False
    negative_exponent = False
    is_float = False
    is_float_in_sci_notation = False
    multiple_digits = False
    multiple_digits_exponent = False

    # Check if the number is negative
    if token[0] == "-":
        negative = True
        token = token[1:]

    # Check if the number is a floating point number
    if token.find(".") != -1 or calculator_state.sign_mode == 3:
        is_float = True

        # Check if we need to change the sign mode to floating point mode
        if (calculator_state.sign_mode == 0 or calculator_state.sign_mode == 1 or calculator_state.sign_mode == 2):
            change_mode = True
            calculator_state.previous_sign_mode = calculator_state.sign_mode
            calculator_state.sign_mode = 3
        
        # Check if the number is in scientific notation
        if token.find("e") != -1:
            is_float_in_sci_notation = True

        # Check if the number is valid
        if not is_valid_float(token, calculator_state):
            logging.critical("Invalid floating point number: " + token + "(line number )"+ calculator_state.input_line_number)
            sys.exit(1)

        # We have a valid floating point number
        if is_float_in_sci_notation:
            # Split the number into the mantissa and the exponent
            mantissa, exponent = token.split("e")
            if exponent[0] == "-":
                negative_exponent = True
                exponent = exponent[1:]

            # Does the mantissa contain multiple digits?
            if len(mantissa) > 1:
                multiple_digits = True
            
            # Does the exponent contain multiple digits?
            if len(exponent) > 1:
                multiple_digits_exponent = True
            
        # We are ready to print the keypresses

    else: # The number is an integer
        is_float = False

        # Check if we need to change the sign mode back to the previous mode
        if (calculator_state.sign_mode == 3):
            change_mode = True
            calculator_state.sign_mode = calculator_state.previous_sign_mode

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
            token_base = calculator_state.base

        if not is_valid_integer(token, calculator_state):
            logging.critical(f"Invalid integer: {token} (line number {input_line_number})")
            sys.exit(1)

        if token_base.lower() != calculator_state.base.lower():
            change_base = True

        token = token.upper()

        # Does the number contain multiple digits?
        if len(token) > 1:
            multiple_digits = True

        # We have a valid integer
        # We are ready to print the keypresses

    # For floats
    if (is_float and change_mode): # Switch to floating point mode
        calculator_state.program.append(instr("FLOAT", None, calculator_state))
        calculator_state.program.append(instr(".", None, calculator_state))
        calculator_state.program_length += 2

        if(is_float_in_sci_notation): # Floating point number in scientific notation
            if(negative):
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program.append(instr("CHS", None, calculator_state))
                calculator_state.program_length += 1
            else:
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1

            if(negative_exponent): 
                calculator_state.program.append(instr("EEX", None, calculator_state))
                for digit in exponent:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program.append(instr("CHS", None, calculator_state))
                calculator_state.program_length += 2
            else:
                calculator_state.program.append(instr("EEX", None, calculator_state))
                for digit in exponent:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program_length += 1

        else: # Floating point number
            if(negative):
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program.append(instr("CHS", None, calculator_state))
                calculator_state.program_length += 1
            else:
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1

    elif (is_float): # Floating point number and already in floating point mode
        if(is_float_in_sci_notation): # Floating point number in scientific notation
            if(negative):
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program.append(instr("CHS", None, calculator_state))
                calculator_state.program_length += 1
            else:
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1

            if(negative_exponent):
                calculator_state.program.append(instr("EEX", None, calculator_state))
                for digit in exponent:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program.append(instr("CHS", None, calculator_state))
                calculator_state.program_length += 2
            else:
                calculator_state.program.append(instr("EEX", None, calculator_state))
                for digit in exponent:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program_length += 1

        else: # Floating point number
            if(negative):
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1
                calculator_state.program.append(instr("CHS", None, calculator_state))
                calculator_state.program_length += 1

            else:
                for digit in token:
                    calculator_state.program.append(instr(digit, None, calculator_state))
                    calculator_state.program_length += 1

    elif(change_mode or change_base): # Switching from float to integer mode
                    #  OR already in integer mode, but changing the base
        logging.debug(f"Changing mode to: {token_base}")
        calculator_state.program.append(instr(token_base.upper(), None, calculator_state))
        calculator_state.program_length += 1

        if (negative):
            for digit in token:
                calculator_state.program.append(instr(digit, None, calculator_state))
                calculator_state.program_length += 1
            calculator_state.program.append(instr("CHS", None, calculator_state))
            calculator_state.program_length += 1
        else:
            for digit in token:
                calculator_state.program.append(instr(digit, None, calculator_state))
                calculator_state.program_length += 1

    else: # Already in integer mode and base
        if (negative):
            for digit in token:
                calculator_state.program.append(instr(digit, None, calculator_state))
                calculator_state.program_length += 1
            calculator_state.program.append(instr("CHS", None, calculator_state))
            calculator_state.program_length += 1
        else:
            for digit in token:
                calculator_state.program.append(instr(digit, None, calculator_state))
                calculator_state.program_length += 1

def is_valid_integer(token, calculator_state):
    # Check if the number is valid
    # Does the token contain the correct characters for the base?
    acceptable_hex_chars = "0123456789abcdef"
    acceptable_dec_chars = "0123456789"
    acceptable_oct_chars = "01234567"
    acceptable_bin_chars = "01"

    if calculator_state.base == 16:
        for char in token:
            if char not in acceptable_hex_chars:
                return False
    elif calculator_state.base == 10:
        for char in token:
            if char not in acceptable_dec_chars:
                return False
    elif calculator_state.base == 8:
        for char in token:
            if char not in acceptable_oct_chars:
                return False
    elif calculator_state.base == 2:
        for char in token:
            if char not in acceptable_bin_chars:
                return False

    # Is the number within the range of the word size?
    logging.debug(f"Token: {token} Base: {calculator_state.base_numeric}")
    try:
        num = int(token, calculator_state.base_numeric)
    except ValueError:
        # Handle the error, for example, by setting num to None or logging an error message
        num = None
        logging.critical(f"Error: {token} is not a valid number in base {calculator_state.base_numeric}")
        return False
    if num < 0:
        return False
    if num >= 2 ** calculator_state.word_size:
        return False
    
    return True


def is_valid_float(token, calculator_state):
    # Check if the number is valid
    # Does the token contain the correct characters for a floating point number?
    acceptable_float_chars = "0123456789.e-"
    contains_e = False
    token = token.lower()

    for char in token:
        if char == "e":
            contains_e = True
        if char not in acceptable_float_chars:
            logging.debug("Invalid character: {char}")
            return False


    # Is the number within the range of a float?
    if contains_e:
        # The number is in scientific notation
        # Split the number into the mantissa and the exponent
        mantissa, exponent = token.split("e")
        if mantissa[0] == "-":
            mantissa = mantissa[1:]
        if exponent[0] == "-":
            exponent = exponent[1:]

        logging.debug("Checking if exponent: {exponent} is valid.")
        if not is_valid_integer(exponent, calculator_state):
            logging.debug("Invalid exponent: {exponent}")
            return False
        num = float(mantissa) ** float(exponent)
    else:
        num = float(token)

    if num > 9.999999999 * 10**99 or num < -9.999999999 * 10**99:
        logging.debug("Number out of range: {num}")
        return False
    
    logging.debug("Valid floating point number: {token}")
    return True


def is_valid_instruction(instr):
    # Check if the instruction is valid
    if instr in mnemonic_to_instr:
        return True
    else:
        return False


def is_valid_argument(instr, arg):
    logging.info("Checking if argument: {arg} is valid for instruction: {instr}")
    
    # Check if the instruction takes an argument
    if instr not in instructions_with_arguments:
        logging.debug("Instruction: {instr} does not take an argument.")
        return False
    logging.debug("Instruction: {instr} takes an argument.")

    # Check if the argument is valid
    if(instr == 'sto' or instr == 'rcl'):
        logging.debug("Checking if argument: {arg} is valid for a STO or RCL instruction.")
        
        # check if the argument is I or (i)
        if(arg == 'i' or arg == '(i)'):
            return True
        elif(arg.isdigit() and int(arg) >= 0 and int(arg) <= 31):
            return True
        else:
            return False
    elif(instr == 'sf' or instr == 'cf' or instr == 'f?'):
        logging.debug("Checking if argument: {arg} is valid for a SF, CF, or F? instruction.")
        
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= 5):
            return True
        else:
            return False
    elif(instr == 'sb' or instr == 'cb' or instr == 'b?'):
        logging.critical("ERROR: Setting/Clearing/Testing a bit does not take an argument")
        sys.exit(1)
    elif(instr == 'lbl' or instr == 'gto' or instr == 'gsb'):
        logging.debug("Checking if argument: {arg} is valid for a LBL, GTO, or GSB instruction.")
        
        if(arg.isdigit() and int(arg) >= 0 and int(arg) < 16):
            return True
        elif(arg in 'abcdef'):
            return True
        elif(arg == 'i' or arg == '(i)'):
            return True
        else:
            return False
    elif(instr == 'show'):
        logging.debug("Checking if argument: {arg} is valid for a SHOW instruction.")
        
        if(arg == 'hex' or arg == 'dec' or arg == 'oct' or arg == 'bin'):
            return True
        else:
            return False
    elif(instr == 'float'):
        logging.debug("Checking if argument: {arg} is valid for a FLOAT instruction.")
        
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= 9):
            return True
        elif(arg == '.'):
            return True
        else:
            return False
    elif(instr == 'window'):
        logging.debug("Checking if argument: {arg} is valid for a WINDOW instruction.")
        
        # This doesn't exclude all invalid arguments, but this instruction will be used so rarely that it doesn't matter
        if(arg.isdigit() and int(arg) >= 0 and int(arg) <= 7):
            return True
        else:
            return False
    elif(instr == 'clear'):
        logging.debug("Checking if argument: {arg} is valid for a CLEAR instruction.")
        
        if(arg == 'reg'):
            return True
        else:
            return False
    else:
        logging.debug("Did not find a valid argument for instruction: {instr}")
        
        return False