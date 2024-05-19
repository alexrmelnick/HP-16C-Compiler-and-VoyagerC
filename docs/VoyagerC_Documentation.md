# The official VoyagerC documentation
Welcome to the official documentation for VoyagerC, a C-based programming language designed specifically for the HP-16C calculator. This documentation will provide an overview of VoyagerC, including the features it borrows from C, the included HP-16C functions, and the VoyagerC functions that are available. It will also provide information on the VoyagerC compiler and how to use it to compile VoyagerC programs into HP-16C keystroke programming. 

Please note that this documentation is a work in progress and will be updated as the VoyagerC project progresses. If you have any questions or suggestions for the documentation (or the project in general), please feel free to reach out. 

## Table of Contents
1. [Introduction](##introduction)
2. [What VoyagerC borrows from C](###what-voyagerc-borrows-from-c)
3. [Included HP-16C Functions](###hp-16c-functions)
4. [VoyagerC Functions](###voyagerc-functions)
5. [Voyager Compiler](###voyagerc-compiler)

## Introduction
VoyagerC is a custom compiled C-based programming language designed around the HP-16C calculator. It is intended to be used with the Voyager Compiler to write programs that can be compiled into HP-16C keystroke programming "assembly". The VoyagerC language is designed to be easy to use and to provide a familiar programming environment for those who are already familiar with C and the HP-16C calculator. The "VoyagerC" name gives a nod to the HP Voyager series of calculators, which includes not only the HP-16C, but also the HP-12C (still the most popular financial calculator in the world) and the HP-15C (a highly regarded scientific calculator).

It is important to note that VoyagerC is not a full implementation of the C programming language. It is a subset of C that has been designed to work with the HP-16C calculator. As such, not all C features are available in VoyagerC. Most notably, it does not support strings. However, VoyagerC does provide a wide range of functions that are specifically designed to work with the HP-16C calculator.

## What VoyagerC borrows from C
VoyagerC borrows many features from the C programming language. The initial version of VoyagerC will include the following features:
    - Variables
    - Comments
    - Control logic (if/else if/else)
    - Loops (for and while)
    - Functions
    - Arrays
    - Pointers
    - Arithmetic operators
    - Comparison operators
    - Logical operators
    - Bitwise operators
    - Assignment operators
    - Increment and decrement operators
    - Certain standard library functions including:
        - abs()
        - sqrt()
        - sizeOf()

## Included HP-16C Functions
The VoyagerC library includes the following functions that are specifically designed to work with the HP-16C calculator:
    - Rotations

## Voyager Compiler
VoyagerC programs are compiled using the Voyager Compiler. VoyagerC files are stored in the .voyc file format. The Voyager Compiler can compile these files into HP-16C keystroke programming "assembly" that can be typed into the HP-16C calculator or loaded into the JRPN HP-16C Simulator. 

The Voyager compiler is written in Python and is currently in development. 