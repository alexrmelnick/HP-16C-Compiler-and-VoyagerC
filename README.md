# HP-16C VoyagerC Compiler and Saturnine Assembler

VoyagerC is a compiler to translate Clang-supported high-level languages (including C, C++, and Objective-C) into HP-16C "assembly" keystroke programming using a custom LLVM backend. Saturnine is an assembler to assemble a HP-16C-manual-based assembly programming language into printable text or into .16c format for loading directly into the JRPN 16C simulator. 

## Description
The HP-16C is a computer scientist's calculator produced from 1982 until 1989. It is still highly regarded and sought after by assembly programmers. This project aims to provide a user-friendly way to extend the usefulness of the HP-16C by allowing users to write programs in high-level languages and compile them into HP-16C keystroke programming.

## Philosophy
This project initially started as a C-based custom programming language designed around the HP-16C. This is where the name "VoyagerC" comes from. After completing the Saturnine Assembler, I started to do more research into complilers and realized that using Clang and LLVM had many advantages over writing my own language and compiler from scratch. Specifically:
- Clang already has full support for the entire C, C++, Objective-C, and Objective-C++ langauges, as well as many other languages which use Clang IL as on the backend.
- LLVM has decades of optimizations that would be impossible for me to implement on my own in a short time period. This is very important for the HP-16C which has a tiny combined 203 Bytes of program and data memory.
- Clang and LLVM are used extensively in industry. Gaining experience with these tools would give me a leg-up in the job market that writing my own compiler from scratch would not.

In short, Clang and LLVM allow me to compile many different languages into HP-16C keystroke programming with far more optimization than I would be able to implement on my own. This will result in a far more optimized compiler and will give me real world experience with tools used in industry. This is the direction that I will go in.

## Roadmap

This project is a work in progress and has a *very* long road ahead of it. Below is a rough roadmap:
1. Learn how to write HP-16C programs in keystroke programming. *In progress*
  - This is a necessary step to understand how to compile VoyagerC into HP-16C keystroke programming.
  - This will also help in understanding the limitations of the HP-16C and how to design VoyagerC to work within those constraints.
  - Write some programs in HP-16C keystroke programming to get a feel for the language.
2. Develop Saturnine Assembly Language and Assembler *In progress*
  - A prototype of the Saturnine Assembly Language and Assembler has been developed. However, it needs to be refined and extended to support more complex programs.
  - Specifically, a complete instruction set and feature list needs to be defined first. 
  - Then the assembler needs to be developed to translate Saturnine Assembly Language into HP-16C keystroke programming and .16c format.
  - I also want it to be able to generate a printable PDF with the sequences of keystrokes for manual input to the HP-16C for retro enthusiasts.
  - *Current Status*: Verify that the Saturnine Assembly Language and Assembler can handle complex programs and that the generated keystroke sequences are correct. I especially want to test and make sure that all instructions are working as intended.
3. Develop VoyagerC compiler using Clang and LLVM.
  - Requires extensive research into Clang and LLVM.
  - Want to add compiler warnings into Clang whenever chars/strings are used since the HP-16C can only display them as ASCII values.
  - Need to make a custom LLVM backend to support the HP-16C's unusual stack-based reverse-polish-notation instruction-set.

### Acknowledgements

This project is inspired by the [JRPN HP-16C Simulator](https://jrpn.jovial.com/) developed by William Foote.

### License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details
