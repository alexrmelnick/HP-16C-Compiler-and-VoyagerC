# Welcome to the official documentation for the Saturnine Assembler
This documentation will provide an overview of the Saturnine Assembler, including the features it provides, the syntax it uses, and how to use it to write programs for the HP-16C Simulator and the JRPN HP-16C Simulator.

Please note that this documentation is a work in progress and will be updated as the SRPN Assembler project progresses. If you have any questions or suggestions for the documentation (or the project in general), please feel free to reach out.


## Table of Contents
1. [Introduction](##introduction)
2. [Registers and Memory](##registers-and-memory)
3. [Instruction Set](##instruction-set)
4. [Syntax](##syntax)
5. [Examples](##examples)


## Introduction
Saturnine is a custom assembly language designed specifically for the HP-16C calculator. It is intended to be used with the JRPN HP-16C Simulator to write programs that can be run on the simulator. It is modeled on the HP-16C keystroke programming language provided in the HP-16C manual with some small simplifications for ease of programming. The Saturnine Assembler is designed to be easy to use and to provide a familiar programming environment for those who are already familiar with the HP-16C calculator.

The Saturnine Assembler gets its name from the JRPN HP-16C Simulator. JRPN stands for Jovial Reverse Polish Notation. One meaning of "Jovial" is "of Jupiter". The next planet after Jupiter is Saturn, so the name "Saturnine" was chosen. The word "Saturnine" has a few meanings, one of which is "gloomy or sullen in temperament". This is a appropriate given the HP-16C's challenge to program.

This guide will repeat lots of information from the HP-16C manual. Part of the reason for its existence is to serve as my notes while learning the HP-16C keystroke programming language. I hope it will be useful to others as well.


## Registers and Memory
This will be my attempt to summarize how the memory and registers work on the HP-16C. This is a work in progress and will be updated as I learn more. You may find comparisons to MIPS, the only other assembly language I have experience with. However, the two are quite different.

Moved from below, might delete later:
- Entering a number places it in the X register. The values previously stored in the X, Y, and Z registers are shifted to the Y, Z, and T registers, respectively. The T register is lost.


## Instruction Set
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
- `sqrt`: X <- sqrt(X)
    - Calculate the square root of the number in the X register and store the result in the X register.
    - If in integer mode, the result is truncated to the nearest integer.
- `1/x`: X <- (1 / X)
    - Calculate the reciprocal of the number in the X register and store the result in the X register.
    - Only works in floating-point mode.
    - Example:
        - `float`; `2`; `1/x`: X == 0.5

### Logical Operations