# HP-16C Compiler and VoyagerC

This project is a compiler that translates VoyagerC, a custom, C-based high-level language, into HP-16C "assembly" keystroke programming.

## Description

The HP-16C Compiler allows users to write programs in VoyagerC and compile them into plaintext for typing into the HP-16C calculator or into the .16c format to be run on the [JRPN HP-16C simulator](https://jrpn.jovial.com/). The HP-16C is a computer scientist's calculator produced from 1982 until 1989. To this day, it is considered the greatest programmer's calculator ever made and is still highly sought after by assembly programmers. This project aims to provide a user-friendly way to develop complex programs for the HP-16C.

## Getting Started

This project is a work in progress. Here is a rough roadmap:
1. Determine the rough specifications of VoyagerC
  - Currently, VoyagerC is planned to be a modified subset of the C programming language with support for with support for the basics (i.e., variables, conditional statements, functions, etc.) and will additionally include all of the functions of the HP-16C buttons. 
3. Thoroughly study compilers and HP-16C keystroke programming
4. Start work in C++ for the VoyagerC compiler
  - I am going to be away from my HP-16C for the summer so I will be beginning work on the compiling into the .16c format used by the JRPN simulator. The simulator has functionality for importing programs fromn file without having to key them manually into the calculator. This is highly desirable for testing the compiler as it removes the step of physically inputting the program.
  - After the compiler successfully compiles into the .16c format, I intend to add functionallity to generate a similar but more human-readable for viewing and printing of the HP-16C "assembly". 

### Prerequisites

- C++ compiling the compiler
- VoyagerC for writing HP-16C programs
- An HP-16C or the [JRPN HP-16C Simulator](https://jrpn.jovial.com/)
