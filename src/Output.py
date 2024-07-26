from DEBUG import DEBUG

from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def output_16c(calculator_state):
    # Update the state of the calculator
    calculator_state.update_memory()
    calculator_state.update_program_length()
    
    # Output the assembled code in the .16c format
    output_file = open(calculator_state.output_file_name + ".16c", "w") # Open the file in write mode

    # Write the header to the output file
    output_file.write("#  Program produced by Alex Melnick's Jovial Assembler.\n")
    output_file.write("#  Character encoding: UTF-8\n")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_file.write(f"#  Generated {current_time}\n")  # Corrected line
    output_file.write(f"#  Program occupies {calculator_state.program_length} bytes.\n\n")  # Corrected line

    # Write the first line of the output file (always the same)
    output_file.write("   000 {          } \n") # 10 spaces between the curly braces

    # Write the keypresses to the output file
    for line_number, line in enumerate(calculator_state.program):
        line_number_str = str(line_number + 1).zfill(3)
        if line.has_modifier and line.has_argument:
            output_line = f"   {line_number_str} {{ {line.modifier_position} {line.instruction_position} {line.argument_position} }} {line.modifier} {line.instruction} {line.argument}\n"
        elif line.has_modifier:
            output_line = f"   {line_number_str} {{    {line.modifier_position} {line.instruction_position} }} {line.modifier} {line.instruction}\n"
        elif line.has_argument:
            output_line = f"   {line_number_str} {{    {line.instruction_position} {line.argument_position} }} {line.instruction} {line.argument}\n"
        else:
            output_line = f"   {line_number_str} {{       {line.instruction_position} }} {line.instruction}\n"
        
        if DEBUG: print("Writing line: ", output_line)
        
        output_file.write(output_line)
    
    output_file.write("\n# End.\n")  # Write end statement to the output file

    # Close the output file
    output_file.close()

def output_txt(calculator_state):
    # TODO: WRITE ME
    # Update the state of the calculator
    calculator_state.update_memory()
    calculator_state.update_program_length()
    
    # Output the assembled code in the .16c format
    output_file = open(calculator_state.output_file_name + ".16c", "w") # Open the file in write mode


    
def output_pdf(calculator_state):
    #TODO Include calculator listings

    # Parameters for the PDF
    font_name = "Dot Matrix" # Using a custom font for the program listing for a retro look
    font_path = "fonts/Dot-Matrix-Typeface-master/Dot Matrix Regular.TTF" # Thank you Daniel Hark for the font!
    line_spacing = 20  # Line spacing for the program listing

    c = canvas.Canvas(calculator_state.output_file_name + ".pdf", pagesize=LETTER)
    pdfmetrics.registerFont(TTFont(font_name, font_path))
    c.setFont(font_name, 12)  # Using Times-Roman font with size 12 because this is meant to be printed
    heading_y_position = 792 - 72  # 72 points (1 inch) from the top

    # Heading and Stats
    header = [
        f"Program Listing for {calculator_state.input_file_name} for the HP-16C Calculator",
        f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} with the Jovial Assembler by Alex Melnick",
        f"Calculator status (at end of program): {calculator_state.sign_mode} mode, {calculator_state.word_size}-bit words, {calculator_state.base} base",
        f"Program length: {calculator_state.program_length} Bytes",
        f"Registers used: {len(calculator_state.registers_used)} of {calculator_state.available_registers} available",
        f"Memory partition @ {calculator_state.memory_partition} Bytes"
    ]

    # Draw Heading and Stats
    for line in header:
        c.drawString(72, heading_y_position, line)
        heading_y_position -= line_spacing

    # Set the dash pattern for the line: 1 unit on, 3 units off
    c.setDash(1, 3)
    # Draw a line under the heading
    c.line(72, heading_y_position, 522, heading_y_position)
    heading_y_position -= line_spacing  # Move down for the next line

    # Column layout settings
    columns = [(72, heading_y_position), (228, heading_y_position), (384, heading_y_position)]  # Adjusted y position for columns start
    column_width = 200  # Not used in this example, but useful for text wrapping
    current_column = 0  # Start with the first column


    # Iterate over the program lines and add them to the PDF
    for line_number, line in enumerate(calculator_state.program, start=1):
        x_position, y_position = columns[current_column]
        line_content = f"{line_number-1:03}: {line}"  # Format line content
        c.drawString(x_position, y_position, line_content)
        y_position -= line_spacing  # Move down for the next line
        columns[current_column] = (x_position, y_position)  # Update the y position in the columns array

        # Check if we need to switch columns or pages
        if y_position < 72:  # Near the bottom of the page
            current_column += 1  # Move to the next column
            if current_column > 2:  # If beyond the third column, create a new page
                c.showPage()
                c.setFont(font_name, 12)
                current_column = 0  # Reset to the first column
                # Reset y position for the new column or page
                heading_y_position = 792 - 72  # 72 points (1 inch) from the top
                columns = [(72, heading_y_position), (228, heading_y_position), (384, heading_y_position)]  # Adjusted y position for columns start

    c.save()  # Save the PDF
