# Welcome to the official documentation for the Saturnine Assembler
This documentation will provide an overview of the Saturnine Assembler, including the features it provides, the syntax it uses, and how to use it to write programs for the HP-16C Simulator and the JRPN HP-16C Simulator.

Please note that this documentation is a work in progress and will be updated as the SRPN Assembler project progresses. If you have any questions or suggestions for the documentation (or the project in general), please feel free to reach out.


## Table of Contents
1. [Introduction](##introduction)
2. [Registers, Memory, and Flags](##registers-memory-and-flags)
3. [Instruction Set](##instruction-set)
4. [Syntax](##syntax)
5. [Examples](##examples)


## Introduction
Saturnine is a custom assembly language designed specifically for the HP-16C calculator. It is intended to be used with the JRPN HP-16C Simulator to write programs that can be run on the simulator. It is modeled on the HP-16C keystroke programming language provided in the HP-16C manual with some small simplifications for ease of programming. The Saturnine Assembler is designed to be easy to use and to provide a familiar programming environment for those who are already familiar with the HP-16C calculator.

The Saturnine Assembler gets its name from the JRPN HP-16C Simulator. JRPN stands for Jovial Reverse Polish Notation. One meaning of "Jovial" is "of Jupiter". The next planet after Jupiter is Saturn, so the name "Saturnine" was chosen. The word "Saturnine" has a few meanings, one of which is "gloomy or sullen in temperament". This is a appropriate given the HP-16C's challenge to program.

This guide will repeat lots of information from the HP-16C manual. Part of the reason for its existence is to serve as my notes while learning the HP-16C keystroke programming language. I hope it will be useful to others as well.


## Registers, Memory, and Flags
This will be my attempt to summarize how the registers, memory, and flags work on the HP-16C. This is a work in progress and will be updated as I learn more. You may find comparisons to MIPS, the only other assembly language I have experience with. However, the two are quite different.

### Registers
The HP-16C has 6 registers. It has a 4 register stack that can be used to store intermediate values, a Last X register which retains a copy of the X register, and an I register for indexing. 
The stack registers, in *reverse* order, are as follows:
- X: The main register. It is the closest thing the HP-16C has to a general purpose register. Most operations are performed using the X register. It's contents are what is generally displayed on the screen and it is the only register that can be directly accessed.
- Y: The second register. It is used for calculations that require 2 operands and to store intermediate values during calculations.
- Z: The third register. It is used to store intermediate values during calculations.
- T: The fourth register. It is used to store intermediate values during calculations. It is lost when a new value is entered into the X register.
The stack registers can rotate depending on the operation. There are 3 types of operations: Stack Lift, Stack Drop, No Stack Change. These most easily understood by looking at the stack as a vertical list of registers. Stack Lift operations move the registers up, Stack Drop operations move the registers down, and No Stack Change operations leave the registers in place. Here is a diagram showing these operations:
![Stack Lift and Drop Diagram](Images/Stack_Lifts_and_Drops_Diagram.png)
The values stored in the stack can be rotated into and out of the X register using the `R^` and `Rv` instructions. The values of the X and Y registers can also be swapped with `X<>Y`. These allow the Y, Z, and T registers to be used more like general purpose registers. 

Additionally, there are 2 more registers, however they are not part of the stack:
- Last X: This register stores the value of the X register before the last operation was performed. It is useful for recalling the previous value of the X register.
- I: This register is used to store the index of the current memory register. It is used in conjunction with the memory operations to allow for indirect memory access. This allows for more flexible memory operations. It can also be used with special functions to simplify for-loop control. 

### Memory
**WIP**

### Flags
**WIP**


## Instruction Set
Each instruction in the Saturnine Assembly Language corresponds to a key press on the HP-16C calculator. Instructions are all based on the keys of 16C, but with some changes to make them typeable from a standard QWERTY keyboard. **Instructions are not case sensitive.** The documentation below will list them as they are on the HP-16C keys, but you may see them in all lowercase in the other files. 

The following is a list of the instructions available in the Saturnine Assembly Language:
### Numeric Input
- `0` through `9`: Enter the corresponding digit in base 10.
- `.`: Enter the decimal point in floating-point mode.
- `A` through `F`: Enter the corresponding digit in base 16.
- `-`: Set the sign of the number to negative in 1's or 2's complement mode.
- To specify the base of the number, use 0b### for binary, 0o### for octal, 0d### for decimal, and 0x### for hexadecimal. If no base is specified, the number is assumed to be in decimal.
- Note that entering a number is its own operation and requires a separate instruction to do an operation with it.
- Examples:
    - `3`: X <- 3
    - `0b1010`: X <- 0d10

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
- `SQRT`: X <- sqrt(X)
    - Calculate the square root of the number in the X register and store the result in the X register.
    - If in integer mode, the result is truncated to the nearest integer.
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
- `lj`: **WIP**s
