from Saturnine_Assembler import *
from Calculator_State import *
from DEBUG import *
from Instructions import *
from Instructions_Data import *


# print(is_valid_float("-5.4E7",CalculatorState(2, 16, "DEC")))
# print(instr("LBL", "d", CalculatorState(2, 16, "DEC")).get_argument_position())
# print(instr("STO", "I", CalculatorState(2, 16, "DEC")).get_argument_position())
print(is_number("DEC"))
print(is_number("0xDEC"))
