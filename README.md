# HP-16C Compiler and VoyagerC

This project is a compiler that translates VoyagerC, a custom, C-based high-level language, into HP-16C "assembly" keystroke programming.

## Description

The HP-16C Compiler allows users to write programs in VoyagerC and compile them into plaintext for typing into the HP-16C calculator or into the .16c format to be run on the JRPN HP-16C simulator. The HP-16C is a computer scientist's calculator produced from 1982 until 1989. It is still highly regarded and sought after by assembly programmers. This project aims to provide a user-friendly way to develop complex programs for the HP-16C.

## Getting Started

This project is a work in progress. Below is a rough roadmap:
1. Determine the Specifications of VoyagerC
  - VoyagerC is planned to be a modified subset of the C programming language with support for basic constructs (e.g., variables, conditional statements, functions) and will include all HP-16C button functions.
2. Study Compilers and HP-16C Keystroke Programming
  - Thoroughly understand compiler design and the specifics of HP-16C keystroke programming.
3. Develop the VoyagerC Compiler in C++
  - Begin by compiling into the .16c format used by the JRPN simulator since the simulator can import programs from files, which is convenient for testing.
  - Once the compiler can generate .16c files, add functionality to produce a more human-readable format for viewing and printing HP-16C "assembly".

### Prerequisites

- A C++ compiler to build the VoyagerC compiler.
- Knowledge of VoyagerC for writing HP-16C programs.
- An HP-16C calculator or the [JRPN HP-16C Simulator](https://jrpn.jovial.com/).

### Usage
- Write your program in VoyagerC.
- Use the compiler to translate your program into HP-16C "assembly" keystroke programming.
- Load the compiled program into the JRPN HP-16C Simulator or type it into your HP-16C calculator.

### Acknowledgements

This project is inspired by the [JRPN HP-16C Simulator](https://jrpn.jovial.com/) developed by William Foote.

### License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details
