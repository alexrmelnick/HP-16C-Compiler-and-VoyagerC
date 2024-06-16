# This is an assembler for the JRPN HP-16C simulator. It takes a text file with keypress programable "assembly
# code" for the HP-16C calculator and converts it into a format that can be read by the simulator. The assembly
# code is taken from the sample programs given in the HP-16C manual. The simulator is written in Python simply
# because I need to brush up on Python for my summer internship. 
# 
# The simulator is written in Python 3.12.3.
#TODO: Add the rest of the buttons to the dictionary
#TODO: Add functionality for detecting illegal buttons
#TODO: Figure out how to work with the #B button
#TODO: Need to account for SHOW [HEX/DEC/OCT/BIN] being having a space in the instruction
#TODO: Figure out how to count the number of bytes in the program and write code to throw an error if the program is too long
import sys
from datetime import datetime
from Buttons import buttons

def main():
    # Check if the user has entered the correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python JRPN_Assembler.py <filename>.16casm")
        sys.exit(1)

    # Open the input file, read it, then close it
    input_file = open(sys.argv[1], "r") # Open the file in read mode
    my_code = input_file.readlines() # Read all the lines of the input file into a list
    input_file.close()

    # Open the output file
    output_file_name = (sys.argv[1])[:-3] # Create the output file name by removing the last 3 characters of the input file name
    output_file = open(output_file_name, "w") # Open the output file in write mode with the same name as the input file and .16c extension

    # Write the header to the output file
    output_file.write("#  Program produced by Alex Melnick's JRPN Assembler.\n")
    output_file.write("#  Character encoding: UTF-8\n")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_file.write("#  Generated "+current_time+"\n") # Write the current date and time to the output file
    output_file.write("# Program occupies ### bytes.\n\n") # TODO: Calculate the number of bytes in the program

    # Write the first line of the output file (always the same)
    output_file.write("   000 {          } \n") # 10 spaces between the curly braces
    
    line_number = 1 # Initialize line number to 1 (line 0 is blank)

    # Loop through the list of lines in the input file and parse the assembly code
    for input_line_number, line in enumerate(my_code):
        if line.isspace(): # Skip empty lines
            continue

        # Split the line into a list of words
        words = line.split("#")[0].split() # Split the line at the "#"" character and then split the real line into words
        #! This is going to cause errors when the #B button is used

        # If any of the words are not in the dictionary, print an error message and exit
        # for word in words:
        #     if word not in buttons: # TODO: Add the dictionary of valid words
        #         print("Error: Unknown word "+word+" on line "+input_line_number)
        #         sys.exit(1)
        
        # Write the line number to the output file
        output_file.write("   "+str(line_number).zfill(3)+" { ")

        if(len(words) == 0):
            continue # This should have been caught by the empty line check above
        elif(len(words) == 1):
            output_file.write("      "+buttons[words[0]]+" } "+words[0]+"\n")
        elif(len(words) == 2):
            output_file.write("   "+buttons[words[0]]+" "+buttons[words[1]]+" } "+words[0]+" "+words[1]+"\n")
        elif(len(words) == 3):
            output_file.write(buttons[words[0]]+" "+buttons[words[1]]+" "+buttons[words[2]]+" } "+words[0]+" "+words[1]+" "+words[2]+"\n")
        else:
            print("Error: Too many words on line "+input_line_number)
            sys.exit(1)

        line_number += 1
    
    output_file.write("\n# End.\n") # Write end statement to the output file

    # Close the output file
    output_file.close()

    print("Assembly complete. Output written to "+output_file_name)

if __name__ == "__main__":
    main()