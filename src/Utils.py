import logging

def is_number(token):
    # Check if the token is a number
    logging.debug(f"Checking if token is a number: {token}")

    # Does token contain any characters other than -,.,0-9,A-F,a-f,b,o,x?
    acceptable_chars = "0123456789aAbBcCdDeEfFox-."

    for char in token:
        if(char not in acceptable_chars):
            logging.debug(f"Token contains invalid character: {char}")
            return False

    # Check that token isn't just "-" or "." or "0x" or "0o" or "0b" or "0d"
    if token == "-" or token == "." or token == "0x" or token == "0o" or token == "0b" or token == "0d":
        logging.debug("Token is just a prefix or a decimal point")
        return False

    # Does token contain more than one decimal point?
    if token.count(".") > 1:
        logging.debug("Token contains more than one decimal point")
        return False
    
    # Does token contain more than two negative signs?
    if token.count("-") > 2:
        logging.debug("Token contains more than two negative signs")
        return False
    
    # Does token contain more than one binary, octal, or hexadecimal prefix?
    if token.count("0b") > 1 or token.count("0o") > 1 or token.count("0x") > 1:
        logging.debug("Token contains more than one base prefix")
        return False
    
    # Does token contain more than one base prefix?
    if token.count("b") > 1 or token.count("o") > 1 or token.count("x") > 1 or token.count("d") > 1:
        logging.debug("Token contains more than one base prefix")
        return False
    
    # Does token contain a prefix and a decimal point (floats are always base 10)?
    if (token.find("0b") != -1 and token.find(".") != -1) or (token.find("0o") != -1 and token.find(".") != -1) or (token.find("0x") != -1 and token.find(".") != -1) or (token.find("0d") != -1 and token.find(".") != -1):
        logging.debug("Token contains a base prefix and a decimal point")
        return False
    
    if token == "DEC" or token == "dec":
        logging.debug("Token is a base")
        return False

    logging.debug("Token is a number")
    return True
