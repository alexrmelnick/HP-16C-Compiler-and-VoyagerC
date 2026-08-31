# HP-16C Jovial Assembler

The Jovial Assembler is an assembler to assemble a custom assembly programming language into a printable keystroke programming text .pdf, into .16c format for loading directly into the JRPN 16C simulator, or into .txt format for the HP16C Emulator. 

Jovial supports descriptive symbolic labels and forward references. A label can use traditional assembler syntax or the calculator-style `LBL` instruction:

```text
loop:
    RCL 0
    GTO loop

LBL helper
    RTN
```

Symbols are case-insensitive and are automatically assigned to the HP-16C's 16 physical labels (`0`–`9` and `A`–`F`). Existing programs using physical labels continue to work. `LBL name = A` can pin a symbol to a particular physical label when exact keystroke compatibility matters.

## Description
The HP-16C is a computer scientist's calculator produced from 1982 until 1989. It is still highly regarded and sought after by assembly programmers. This project aims to provide a user-friendly way to extend the usefulness of the HP-16C by allowing users to write programs in a text editor and assembler them into keystroke programming sequences. The Jovial assembly language is based on the sample programs found in the HP-16C manual. The assembler is written in Python and is designed to be easily extendible to other simulators.

This project started after I received an HP-16C for my birthday. I was absolutely fascinated by the calculator and its programming capabilities. I wanted to write programs for it, but I found the manual programming method to be very cumbersome. I looked online and found various simulators, but none of them offered a connivent way to write programs other than "typing" them in manually. One open-source project, the JRPN 16C simulator, had a human readable format for importing and exporting programs, so I decided to write an assembler targeting it first. I then targeted the HP16C emulator once I realized it had the option to import programs in plain text as well. The HP16C emulator allows you to see the Program memory, Registers, and Stack all at once, so it is extremely useful for debugging. This project gave me the opportunity to learn about the HP-16C's architecture and assembly capabilities. As well, it gave me to opportunity to contribute to the open-source community.


## Usage/Installation

The Jovial Assembler is written in Python 3.12. Other Python 3 versions may work, but they have not been tested.

### Standalone executables

The `dist` folder contains standalone executables that do not require Python:

- `jovial.exe` for 64-bit Windows.
- `jovial-linux-x86_64` for 64-bit Linux systems using the x86-64 architecture and glibc 2.28 or newer.

On Linux, make the downloaded file executable before running it:

```bash
chmod +x jovial-linux-x86_64
./jovial-linux-x86_64 --help
```

On either platform, pass an input `.jov` file and the desired output filename:

```bash
jovial-linux-x86_64 -i program.jov -o program.pdf
```

The generated `.pdf`, `.16c`, or `.txt` file is written to the path supplied with `-o`. You can optionally put the executable on your system `PATH` and invoke it as `jovial`.

### Building executables

Both platforms use the checked-in `jovial.spec` PyInstaller definition. After installing Python 3.12 and the dependencies in `requirements.txt`, build on the target operating system (PyInstaller does not cross-compile):

```bash
# Linux
./build-linux.sh

# Windows (PowerShell)
python -m PyInstaller --clean --noconfirm jovial.spec
```

The GitHub Actions workflow in `.github/workflows/build-executables.yml` also builds and tests downloadable Windows x86-64 and Linux x86-64 artifacts on every main-branch push, pull request, version tag, or manual run.


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
### 3. Write an installer for the Jovial Assembler **(complete for now)**
  - Standalone executables are available for Windows x86-64 and Linux x86-64.
  - You can add the appropriate executable to your path to run it from the command line.
  - I hope to one day make a proper installer for the program so this is automated.
### 4. Extend the Jovial Assembler to new simulators **(complete)**
  - Add support for Jamie O'Connell's HP-16C Emulator.
### 5. Rework Argument Parsing **(complete)**
  - Rework command line arguments, possibly using a library that is more robust.
  - Might reword the requirement for initial settings to be optional. It may be better to have them included in the program itself, so that the program is self-contained.
    - Could have them be optional and checks will not be done if they are not included and are not yet set.
  - Write a script to automatically update all the files in the `tests` folders when the assembler is updated.
### 6. Future hopes and dreams
  - Add support for the PX16C Kit. 
    - This is closed source, so this will require either cooperation from the developer or reverse engineering. 
  - Add support for a macOS executable.
  - Add the ability to combine multiple programs into 1 single file seamlessly so that you can keep a library of programs.
    - Need to be able to handle conflicting labels and memory addresses.
  - Figure out how to disable the traceback when the task is terminated manually. 
  - Improve installation process.

### Acknowledgements

This project designed to work with the [JRPN HP-16C Simulator](https://jrpn.jovial.com/) developed by William Foote and the [HP16C Emulator](http://www.hp16c.org/) developed by Jamie O'Connell. 

Thank you Paul Flo Williams for your [Dotrice Font Family](https://www.1001fonts.com/dotrice-font.html), which I used for the PDF output. I have gone through many font choices for this project, and this is the best one I have found that is open-source, mono-spaced, and in the dot matrix style of the 1980s.

### License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details
