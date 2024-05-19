# HP-16C Compiler and VoyagerC

This project is a compiler that translates VoyagerC, a custom C library, into HP-16C "assembly" keystroke programming.

## Description

The HP-16C Compiler allows users to write programs in VoyagerC and compile them into plaintext for typing into the HP-16C calculator or into the .16c format to be run on the JRPN HP-16C simulator. The HP-16C is a computer scientist's calculator produced from 1982 until 1989. It is still highly regarded and sought after by assembly programmers. This project aims to provide a user-friendly way to extend the usefulness of the HP-16C by allowing users to write programs in a C-like language and compile them into HP-16C keystroke programming.

## Philosophy
There are two potential paths for this project:

1. **Create a Compiler to Use the HP-16C as a General-Purpose Computer**
2. **Create a Compiler to Extend the Usefulness of the HP-16C as a Calculator**

These two goals are quite different. Using the HP-16C as a general-purpose computer would require developing a hyper-optimized compiler capable of handling a wide range of C programs. The HP-16C has a total of 203 bytes of user accessible combined program and data memory. While this isn't impossible—consider the niche of Boot Sector Programs, which aim to create programs with a maximum size of 510 bytes (many impressive games have been made within this constraint, [check out these examples](https://gist.github.com/XlogicX/8204cf17c432cc2b968d138eb639494e))—running general-purpose programs on the HP-16C would mean programming in less than half that space. This is an extraordinarily challenging task and serves no practical purpose.

**The HP-16C is a calculator,** and it should be used as such. Therefore, the goal of this project is to extend the usefulness of the HP-16C as a calculator. This means creating a compiler that can handle complex programs that are specifically useful for its intended purpose.


## Getting Started

This project is a work in progress. Below is a rough roadmap:
1. Determine the Specifications of VoyagerC
  - VoyagerC is planned to be an extension for the C programming language designed around specific HP-16C buttons and functions.
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
