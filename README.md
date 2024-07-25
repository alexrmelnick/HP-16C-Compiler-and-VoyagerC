# HP-16C Jovial Assembler

The Jovial Assembler is an assembler to assemble a custom assembly programming language into a printable keystroke programming text .pdf or into .16c format for loading directly into the JRPN 16C simulator. 

## Description
The HP-16C is a computer scientist's calculator produced from 1982 until 1989. It is still highly regarded and sought after by assembly programmers. This project aims to provide a user-friendly way to extend the usefulness of the HP-16C by allowing users to write programs in a text editor and assembler them into keystroke programming sequences. The Jovial assembly language is based on the sample programs found in the HP-16C manual. The assembler is written in Python and is designed to be easily extendible to other simulators.

This project started after I received an HP-16C for my birthday. I was absolutely fascinated by the calculator and its programming capabilities. I wanted to write programs for it, but I found the manual programming method to be very cumbersome. I looked online and found various simulators, but none of them offered a connivent way to write programs other than "typing" them in manually. One open-source project, the JRPN 16C simulator, had a human readable format for importing and exporting programs, so I decided to write an assembler targeting it first. This gave me the opportunity to learn about the HP-16C's architecture and assembly capabilities. As well, it gave me to opportunity to contribute to the open-source community.


## Usage/Installation
The Jovial Assembler is written in Python 3.12. Other versions of Python 3 may work, but they have not been tested. You can use the Jovial Assembler by using the following methods. Options 2 and 3 require python to be installed on your system.:

1. Download the `jovial.exe` file in the `dist` folder or clone the repo. 
2. Run the `jovial.exe` file. This is a standalone executable that does not require Python to be installed. 
  - This file is created using PyInstaller and is located in the `dist` folder. 
  - The assembled file will be saved in the same directory as the executable.
  - This file is only available for Windows. If you would like to run the assembler on another operating system, you will need to install Python 3.12 and run the assembler from the command line.
  - Updated versions of the executable can be built by running the following command:
    - `pyinstaller src/Jovial_Assembler.py --clean --onefile --path src --name jovial
3. If you want to run the assembler from the command line using the `jovial` with arguments, add the folder containing the `jovial.exe` file to your system's PATH variable.
  - Follow [these instructions here if you are unfamiliar with this process](https://stackoverflow.com/questions/4822400/register-an-exe-so-you-can-run-it-from-any-command-line-in-windows).


## Roadmap
### 1. Understand the HP-16C Architecture **(complete)**
- Research HP-16C Specifications:
  - Learn about its memory constraints (203 bytes for program and data).
  - Understand its instruction set and keypress programming method.
  - Study its reverse polish notation (RPN) input method.
### 2. Develop the Jovial Assembler **(complete)**
- Define Assembly Language Syntax:
  - Design a simple assembly language that maps to HP-16C keypress sequences.
  - Define the syntax for arithmetic, logical, and control flow operations.
- Implement Assembler:
  - Develop a tool to parse assembly code and generate HP-16C keystroke sequences.
  - Handle memory constraints and ensure generated code fits within the 203-byte limit.
- Test Assembler:
  - Write assembly programs to test the assembler’s functionality.
  - Verify that the generated keystroke sequences produce the expected results.
### 3. Write an installer for the Jovial Assembler **(in progress)**
  - Write a script to install the Jovial Assembler on a user's system.
    - Currently it can be manually installed on Windows
    - I would like to make an automated installer and add support for Linux and MacOS.
### 4. Extend the Jovial Assembler to new simulators
  - Add support for Jamie O'Connell's HP-16C Emulator.
  - Add support for the PX16C Kit. 
    - These are both closed source, so this will require either cooperation from the developers or reverse engineering. 

### Acknowledgements

This project designed to work with the [JRPN HP-16C Simulator](https://jrpn.jovial.com/) developed by William Foote.

### License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details
