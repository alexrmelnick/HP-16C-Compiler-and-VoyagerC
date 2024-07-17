# HP-16C VoyagerC Compiler and Saturnine Assembler

VoyagerC is a compiler to translate Clang-supported high-level languages (including C, C++, and Objective-C) into HP-16C "assembly" keystroke programming using a custom LLVM backend. Saturnine is an assembler to assemble a HP-16C-manual-based assembly programming language into printable text or into .16c format for loading directly into the JRPN 16C simulator. 

## Description
The HP-16C is a computer scientist's calculator produced from 1982 until 1989. It is still highly regarded and sought after by assembly programmers. This project aims to provide a user-friendly way to extend the usefulness of the HP-16C by allowing users to write programs in high-level languages and compile them into HP-16C keystroke programming.

## Philosophy
This project initially started as a C-based custom programming language designed around the HP-16C. This is where the name "VoyagerC" comes from. After completing the Saturnine Assembler, I started to do more research into compilers and realized that using Clang and LLVM had many advantages over writing my own language and compiler from scratch. Specifically:
- Clang already has full support for the entire C, C++, Objective-C, and Objective-C++ languages, as well as many other languages which use Clang IL as on the backend.
- LLVM has decades of optimizations that would be impossible for me to implement on my own in a short time period. This is very important for the HP-16C which has a tiny combined 203 Bytes of program and data memory.
- Clang and LLVM are used extensively in industry. Gaining experience with these tools would give me a leg-up in the job market that writing my own compiler from scratch would not.

In short, Clang and LLVM allow me to compile many different languages into HP-16C keystroke programming with far more optimization than I would be able to implement on my own. This will result in a far more optimized compiler and will give me real world experience with tools used in industry. This is the direction that I will go in.

## Roadmap
This project is a work in progress and has a *very* long road ahead of it. Below is a rough roadmap (generated by ChatGPT):
### 1. Understand the HP-16C Architecture **(complete)**
- Research HP-16C Specifications:
  - Learn about its memory constraints (203 bytes for program and data).
  - Understand its instruction set and keypress programming method.
  - Study its reverse polish notation (RPN) input method.
### 1. Develop the Saturnine Assembler **(complete)**
- Define Assembly Language Syntax:
  - Design a simple assembly language that maps to HP-16C keypress sequences.
  - Define the syntax for arithmetic, logical, and control flow operations.
- Implement Assembler:
  - Develop a tool to parse assembly code and generate HP-16C keystroke sequences.
  - Handle memory constraints and ensure generated code fits within the 203-byte limit.
- Test Assembler:
  - Write assembly programs to test the assembler’s functionality.
  - Verify that the generated keystroke sequences produce the expected results.
### 2. Set Up Development Environment *(in progress)*
- Install Clang and LLVM:
  - Install Clang and LLVM on your development machine.
  - Familiarize yourself with LLVM’s architecture and intermediate representation (IR).
### 3. Design the Compiler Architecture
- Define the Project Scope:
  - Determine which subset of C you will support, given the HP-16C’s constraints.
  - Plan for how to handle memory management, given the limited memory.
- Set Up Project Structure:
  - Organize directories for source code, IR code, and target code.
  - Create a build system (e.g., using CMake) to manage compilation steps.
### 4. Frontend Development
- Lexical Analysis and Parsing:
  - Use Clang’s frontend capabilities to parse C code.
  - Modify Clang’s AST (Abstract Syntax Tree) to fit the HP-16C’s architecture.
- Semantic Analysis:
  - Implement semantic checks to ensure the source code adheres to your defined C subset.
### 5. Intermediate Representation (IR) Generation
- Generate LLVM IR:
  - Translate the Clang AST into LLVM IR.
  - Ensure the IR represents operations compatible with the HP-16C’s capabilities.
### 6. Backend Development
- Instruction Selection:
  - Map LLVM IR instructions to HP-16C keypress sequences.
  - Develop algorithms to handle arithmetic, logical, and control flow operations.
- Register Allocation and Memory Management:
  - Implement a register allocator suitable for the HP-16C’s architecture.
  - Design strategies for efficient memory use within the 203-byte limit.
### 7. Code Generation
- Generate Keypress Sequences:
  - Convert the LLVM IR (or an intermediary form) into keypress sequences.
  - Ensure generated code is optimized for memory usage and execution speed.
### 8. Testing and Debugging
- Develop Test Cases:
  - Write C programs that exercise different features of your compiler.
  - Create unit tests to verify the correctness of each component of the compiler.
- Simulate HP-16C Execution:
  - Develop or find a simulator for the HP-16C to test your generated code.
  - Debug and fix issues in the code generation process.
### 9. Optimization
- Code Optimization:
  - Implement optimizations specific to the HP-16C’s architecture.
  - Focus on reducing memory footprint and improving execution speed.
- Refine Compiler Performance:
  - Profile the compiler to identify and resolve performance bottlenecks.
### 10. Documentation and Finalization
- Write Documentation:
  - Document the design and implementation of your compiler.
  - Provide user guides for compiling C programs and loading them onto the HP-16C.
  - Hopefully this will be completed as the project progresses.
- Package and Distribute:
  - Prepare your compiler for distribution.
  - Create installation scripts and user manuals.

### Acknowledgements

This project is inspired by the [JRPN HP-16C Simulator](https://jrpn.jovial.com/) developed by William Foote.

### License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details
