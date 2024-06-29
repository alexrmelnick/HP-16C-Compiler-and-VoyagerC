
def is_number(token):
    # Check if the token is a number

    # Does token contain any characters other than -,.,0-9,A-F,a-f,b,o,x?
    acceptable_chars = "0123456789abcdefox-."

    for char in token:
        if(char not in acceptable_chars):
            return False

    # Does token contain more than one decimal point?
    if token.count(".") > 1:
        return False
    
    # Does token contain more than two negative signs?
    if token.count("-") > 2:
        return False
    
    # Does token contain more than one binary, octal, or hexadecimal prefix?
    if token.count("0b") > 1 or token.count("0o") > 1 or token.count("0x") > 1:
        return False
    
    # Does token contain more than one base prefix?
    if token.count("b") > 1 or token.count("o") > 1 or token.count("x") > 1:
        return False
    
    # Does token contain a prefix and a decimal point (floats are always base 10)?
    if (token.find("0b") != -1 and token.find(".")) or (token.find("0b") != -1 and token.find(".")) or (token.find("0x") != -1 and token.find(".")) or (token.find("0d") != -1 and token.find(".")):
        return False

    return True
