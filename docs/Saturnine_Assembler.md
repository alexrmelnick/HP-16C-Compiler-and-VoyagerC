# Welcome to the official documentation for the Saturnine Assembler
This documentation will provide an overview of the Saturnine Assembler, including the features it provides, the syntax it uses, and how to use it to write programs for the HP-16C Simulator and the JRPN HP-16C Simulator.

Please note that this documentation is a work in progress and will be updated as the SRPN Assembler project progresses. If you have any questions or suggestions for the documentation (or the project in general), please feel free to reach out.


## Table of Contents
1. [Introduction](##introduction)
2. [System Architecture](##system-architecture)
    a. [Registers](###registers)
    b. [Numerical Representation Modes](###numerical-representation-modes)
        i. [Integer Mode](####integer-mode)
        ii. [Floating Point Mode](####floating-point-mode)
    c. [Memory](###memory)
    d. [Flags](###flags)
        i. [Status](###status)
3. [Instruction Set](##instruction-set)
    a. [Numeric Input](###numeric-input)
    b. [Arithmetic Operations](###arithmetic-operations)
    c. [Logical Operations](###logical-operations)
    d. [Shifting and Rotating Operations](###shifting-and-rotating-operations)
4. [Syntax](##syntax)
5. [Usage](##usage)


## Introduction
Saturnine is a custom assembly language designed specifically for the HP-16C calculator. It is intended to be used with the JRPN HP-16C Simulator to write programs that can be run on the simulator. It is modeled on the HP-16C keystroke programming language provided in the HP-16C manual with some small simplifications for ease of programming. The Saturnine Assembler is designed to be easy to use and to provide a familiar programming environment for those who are already familiar with the HP-16C calculator.

The Saturnine Assembler gets its name from the JRPN HP-16C Simulator. JRPN stands for Jovial Reverse Polish Notation. One meaning of "Jovial" is "of Jupiter". The next planet after Jupiter is Saturn, so the name "Saturnine" was chosen. The word "Saturnine" has a few meanings, one of which is "gloomy or sullen in temperament". This is a appropriate given the HP-16C's challenge to program.

This guide will repeat lots of information from the HP-16C manual. Half of the reason for its existence is to serve as my notes while learning the HP-16C keystroke programming language. I hope it will be useful to others as well.


## System Architecture
This will be my attempt to summarize how the system architecture works on the HP-16C. This is a work in progress and will be updated as I learn more. You may find comparisons to MIPS, the only other assembly language I have experience with. However, the two are quite different. I struggled on how exactly to order the categories in this section. I decided to simply copy the order of the HP-16C manual, however knowledge of some categories is required to understand others. I will try to make it clear when this is the case.

### Registers
The HP-16C has 6 registers. It has a 4 register stack that can be used to store intermediate values, a Last X register which retains a copy of the X register, and an I register for indexing. 
The stack registers, in *reverse* order, are as follows:
- X: The main register. It is the closest thing the HP-16C has to a general purpose register. Most operations are performed using the X register. It's contents are what is generally displayed on the screen and it is the only register that can be directly accessed.
- Y: The second register. It is used for calculations that require 2 operands and to store intermediate values during calculations.
- Z: The third register. It is used to store intermediate values during calculations.
- T: The fourth register. It is used to store intermediate values during calculations. It is lost when a new value is entered into the X register.

The stack registers can rotate depending on the operation. There are 3 types of operations: Stack Lift, Stack Drop, No Stack Change. These most easily understood by looking at the stack as a vertical list of registers. Stack Lift operations move the registers up, Stack Drop operations move the registers down, and No Stack Change operations leave the registers in place. Here is a diagram showing these operations:
![Stack Lift and Drop Diagram](Images/Stack_Lifts_and_Drops_Diagram.png)
Most notably, entering numbers and `ENTER` are Stack Lift operations, and arithmetic and logical operations are Stack Drop operations. 

The values stored in the stack can be rotated into and out of the X register using the `R^` and `Rv` instructions. The values of the X and Y registers can also be swapped with `X<>Y`. These allow the Y, Z, and T registers to be used more like general purpose registers. 

Additionally, there are 2 more registers, however they are not part of the stack:
- Last X: This register stores the value of the X register before the last operation was performed. It is useful for recalling the previous value of the X register. Example: 

    | Keypress Sequence | Registers       |
    |-------------------|-----------------|
    | `1`, `ENTER`      | X <- 1          |
    | `2`               | X <- 2, Y <- 1  |
    | `+`               | X <- 3, Last X <- 2, Y == 1 |
    | `LST-X`           | X <- 2, Last X == 2, Y == 1 |
- I: This register is used to store the index of the current memory register. It is used in conjunction with the memory operations to allow for indirect memory access. This allows for more flexible memory operations. It can also be used with special functions to simplify for-loop control. 

### Numerical Representation Modes
The HP-16C has 2 main modes: integer, and floating point. The vast majority of calculations are done in integer mode since it is far more fully featured. The two modes are mostly incompatible with each other - the numbers in each do not have the necessarily same cardinality (i.e., numerical value) in each format. Converting between the two is possible, but not always straightforward. See the [Floating Point Mode](####Floating-Point-Mode) section for more information. 
#### Integer Mode
In integer mode, the HP-16C can store numbers in 4 different bases: `binary`, `octal`, `decimal`, and `hexadecimal`. For the Saturnine Assembler, to specify the base of the number, use `0b###` for `binary`, `0o###` for `octal`, `0d###` for `decimal`, and `0x###` for `hexadecimal`. If no base is specified, the number is assumed to be in `decimal`.

The HP-16C can store integers in 180 different combinations of encodings. The original purpose of this is so you can set your HP-16C to whatever encoding your computer uses. The HP-16C was primarily a debugging tool for computer engineers working in assembly, so this feature was useful, but not so relevant for the Saturnine Assembler. 

The HP-16C stores integers in 1 of 3 different encodings: `unsigned`, `1's complement`, and `2's complement`. The encoding set in Saturnine by using the `UNSIGNED`, `1's`, `2's` instructions, respectively. The default is `2's complement`. For most purposes, you should set the HP-16C to `2's complement` encoding for signed integers, or `unsigned` for unsigned integers. `1's complement` mode arithmetic is weird and is effected by the carry flag and has -0. While you might find it useful for debugging a UNIVAC, I will not be discussing it further as it is not useful for programming.  

The HP-16C can store integers in any word size between `4-` and `64-bits`. This means it is still actually useful for modern 64-bit computers. By default, the HP-16C is set to `16-bit` word size. The word size can be set using the `WORD` instruction. For most purposes, you should set the HP-16C to either `4-bit`, `8-bit`, `16-bit`, `32-bit`, or `64-bit` word size, depending on the size of the integers you are working with. I am unaware of any reason to use the other word sizes for integers. Maybe if you wanted to store `7-bit` integers for ASCII characters, but that seems like a stretch. Numbers that are too large to fit in the word size cannot be entered. Results of calculations with values larger than 2^[WORD SIZE] will cause an out-of-range error (flag 5 / `G` annunciator). The X register's value will be the result of the operation modulo 2^[WORD SIZE].

The word size not only affects when the maximum storable value in a register, but also how many much memory is available. The HP-16C has 203 Bytes of memory. This is divided by the word size to get the number of storage addresses. This will be discussed in more detail in the [Memory](###Memory) section.

#### Floating Point Mode
In floating point mode, the HP-16C can do calculations with decimals. The HP-16C does not use the IEEE 754 Standard for Floating Point Arithmetic. The standard not published until 1985, 4 years after the HP-16C was released. In 1982 at release, the proposal was only a draft. Notably, HP did include a program in the manual to convert between the two formats, but does not use the IEEE 754 standard internally. This limits the usefulness of the HP-16C for modern floating point applications. 

To enter floating point mode, use the `FLOAT #` instruction, where `#` is the number of decimal places to use. If a `.` is entered instead of a number, the 16C will display the floating point number in scientific/engineering notion with 6 decimal place. The last 2 digits on the display (i.e., those to the right of the gap) are the exponent.
- Example: `FLOAT 2`; `3`: DISPLAY == 3.00
- Example: `FLOAT .`; `300`: DISPLAY == 3.000000 02 (== 3.000000 * 10^2)

Numbers can be entered in scientific notion using the `EEX` button to set the exponent. 
- Example: `FLOAT 2`; `3`; `EEX`; `2`: DISPLAY == 300.00
- Example: `FLOAT .`; `3`; `EEX`; `2`: DISPLAY == 3.000000 02 (== 3.000000 * 10^2)

Internally, the HP-16C stores floating point numbers with a 10 digit mantissa and a 2 digit exponent (#.### ### ### * 2 ^##). This means that the HP-16C can store floats between +/- 9.999999999 * 10^99. Results of calculations with values larger or smaller than these limits will cause an out-of-range error (flag 5 / `G` annunciator) with X <- +/- +/- 9.999999999 * 10^99. The smallest value that can be stored is 1.000000000 * 10^-99. Any values smaller than this will be rounded to 0.

The value in the initial display will be Y*2^X, where Y and X are the integer values stored in the Y and X registers. This means that integers can be converted to floating point numbers by setting the X register to 0. Returning to integer mode will not convert the floating point number back to an integer. The X and Y registers will be set to values such that X * 2^Y == the floating point number previously displayed. 
- Example: `3`; `ENTER`; `2`; `FLOAT 2`: X == 2, Y == 3, Display 12.00 (== 3 * 2^2 == 3 * 4 == 12)

On converting to floating point mode, the stack and the LAST X registers are cleared. The I register and the storage registers are not affected. The complement mode is maintained, but not in use. On returning to integer mode, the registers are not cleared (note that they will not be converted to integers either). However, the X and Y registers will be altered as described above.

Floating point mode has a word size of `56-bit`. This means an absolute maximum of 29 floating point values can be stored in memory, assuming no program is loaded. Returning to integer mode maintains this word `56-bit` size. 

### Memory
**WIP**
From above for future use:
In `16-bit` mode, there are 101 storage registers. In `64-bit` mode, there are 25 storage registers. Interestingly, in `4-bit` mode, there are 406 storage registers.

### Flags
**WIP**

#### Status
This largely does not apply to the Saturnine Assembler, but is useful to know. When in `STATUS` mode, the HP-16C will display the status of the calculator. This includes, in order, the complement mode, the word size, and the current status of the `flags 3, 2, 1, and 0`. Note that `flags 4 (carry)` and `5 (out-of-range)` are always displayed by the `C` and `G` annunciators respectively. See the diagram below for the layout of the status display:
![Status Display Diagram](Images/Status_Diagram.png)

## Instruction Set
Each instruction in the Saturnine Assembly Language corresponds to a key press on the HP-16C calculator. Instructions are all based on the keys of 16C, but with some changes to make them typeable from a standard QWERTY keyboard. **Instructions are not case sensitive.** The documentation below will list them as they are on the HP-16C keys, but you may see them in all lowercase in the other files. 

The following is a list of the instructions available in the Saturnine Assembly Language:
### Numeric Input
- `0` through `9`: Enter the corresponding digit in base 10.
- `.`: Enter the decimal point in floating-point mode.
- `A` through `F`: Enter the corresponding digit in base 16.
- `CHS`: Set the sign of the number to negative in 1's or 2's complement mode.
- To specify the base of the number, use 0b### for binary, 0o### for octal, 0d### for decimal, and 0x### for hexadecimal. If no base is specified, the number is assumed to be in decimal.
- Note that entering a number is its own operation and requires a separate instruction to do an operation with it.
- `HEX`, `DEC`, `OCT`, `BIN`: Set the base of the number to hexadecimal, decimal, octal, or binary, respectively.
- Examples (in 2's complement mode with an 8-bit word size):
    - `3`: X <- 3
    - `0b1010`: X <- 0d10
    - `0xA`; `CHS`; `DEC`: X <- 0xA; X <- 0xF6; X <- -10

### Arithmetic Operations
- `+`: X <- X + Y
    - Add the number in the X register to the number in the Y register and store the result in the X register.
- `-`: X <- Y - X
    - Subtract the number in the X register from the number in the Y register and store the result in the X register.
    - Example:
        - `5`; `3`; `-`: X == 2
        - X <- 5; X <- 3, Y <- 5; X <- (5 - 3) == 2
- `*`: X <- X * Y
    - Multiply the number in the X register by the number in the Y register and store the result in the X register.
- `/`: X <- Y / X
    - Divide the number in the Y register by the number in the X register and store the result in the X register.
    - Example:
        - `10`; `2`; `/`: X == 5
        - X <- 10; X <- 2, Y <- 10; X <- (10 / 2) == 5
- `RMD`: X <- Y % |X|
    - Calculate the remainder of the division of the number in the Y register by the absolute value of the number in the X register and store the result in the X register.
- `SQRT`: X <- sqrt(X)
    - Calculate the square root of the number in the X register and store the result in the X register.
- If in integer mode, the result of division and square roots are truncated to the nearest integer (i.e., rounded down).
- `1/X`: X <- (1 / X)
    - Calculate the reciprocal of the number in the X register and store the result in the X register.
    - Only works in floating-point mode.
    - Example:
        - `FLOAT`; `2`; `1/x`: X == 0.5

### Logical Operations
- `AND`: X <- (X && Y)
    - Perform a bitwise AND operation on the number in the X register and the number in the Y register and store the result in the X register.
    - Example:
        - `0b1010`; `0b1100`; `AND`: X == 0b1000
- `OR`: X <- (X || Y)
    - Perform a bitwise OR operation on the number in the X register and the number in the Y register and store the result in the X register.
    - Example:
        - `0b1010`; `0b1100`; `OR`: X == 0b1110
- `XOR`: X <- (X ⊕ Y)
    - Perform a bitwise XOR operation on the number in the X register and the number in the Y register and store the result in the X register.
    - Example:
        - `0b1010`; `0b1100`; `XOR`: X == 0b0110
- `NOT`: X <- ~X
    - Perform a bitwise NOT operation on the number in the X register and store the result in the X register.
    - Example:
        - `0b1010`; `NOT`: X == 0b0101

### Shifting and Rotating Operations
- `SL` and `SR`: X <- X << 1 and X <- X >> 1
    - Shift the number in the X register left or right by one bit and store the result in the X register.
    - The bit shifted out is stored in the carry flag.
    - Example:
        - `0b1010`; `SL`: X == 0b0100, carry == 1
- `lj`: **WIP**

## Syntax
The syntax for the Saturnine Assembler is based on the examples in the HP-16C manual. Each line of code in a Saturnine program corresponds to a series of key presses on the HP-16C calculator. Each instruction is written on a separate line and comments are allowed using `//`. One key difference is that writing the `f` and `g` keys is unnecessary. The Saturnine Assembler will add them automatically when assembling.

The following is an example of the syntax for a Saturnine program:
**WIP**

## Usage
**WIP**
Initial mode settings? Could check if numbers are out of range on assembly