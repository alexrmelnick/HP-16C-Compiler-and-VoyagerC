# Dictionary of valid buttons on the HP-16C calculator and their corresponding positions on the keyboard
# Position of 11 is the top left button, 
#TODO Double check encodings for all buttons and their positions

buttons = {
    # Alphanumeric keys
    'A': ' A',
    'B': ' B',
    'C': ' C',
    'D': ' D',
    'E': ' E',
    'F': ' F',
    '0': ' 0',
    '1': ' 1',
    '2': ' 2',
    '3': ' 3',
    '4': ' 4',
    '5': ' 5',
    '6': ' 6',
    '7': ' 7',
    '8': ' 8',
    '9': ' 9',
    # Regular keys
    '/': '10',
    'GSB': '21',
    'GTO': '22',
    'HEX': '23',
    'DEC': '24',
    'OCT': '25',
    'BIN': '26',
    '*': '20',
    'R/S': '31',
    'SST': '32',
    'R\/': '33',
    'X<=>Y': '34',
    'BSP': '35',
    'ENTER': '36', #? Enter key takes up 2 spaces, so I am not sure if this is correct
    '-': '30',
    'f': '42',
    'g': '43',
    'STO': '44',
    'RCL': '45',
    '.' : '48',
    'CHS': '49',
    '+': '40',
    # f keys
    'SL': '11',
    'SR': '12',
    'RL': '13',
    'RR': '14',
    'RLn': '15',
    'RRn': '16',
    'MASKL': '17',
    'MASKR': '18',
    'RMD': '19',
    'XOR': '10',
    'X<=>(i)': '21',
    'X<=>I': '22',
    # 'SHOW HEX': '23', #* This is a special case because it has a space in the instruction
    # 'SHOW DEC': '24',
    # 'SHOW OCT': '25',
    # 'SHOW BIN': '26',
    'AND': '20',
    '(i)': '31',
    'I': '32',
    # 'CLEAR PRGM': '33', #* This is a special case because it has a space in the instruction
    # 'CLEAR REG': '34',
    # 'CLEAR PREFIX': '35',
    'WINDOW': '36', #? This key takes up 2 spaces, so I am not sure if this is correct
    '1s': '37',
    '2s': '38',
    '3s': '39',
    'NOT': '30',
    'WSIZE': '44',
    'FLOAT': '45',
    'MEM': '47',
    'STATUS': '48',
    'EEX': '49',
    'OR': '40',
    # g keys
    'LJ': '11',
    'ASR': '12',
    'RLC': '13',
    'RRC': '14',
    'RLCn': '15',
    'RRCn': '16',
    # '#B': '17', #* This is a special case because it has a hashtag in the instruction
    'ABS': '18',
    'DBLR': '19',
    'DBL/': '10',
    'RTN': '21',
    'LBL': '22',
    'DSZ': '23',
    'ISZ': '24',
    'SQRTx': '25', #? Not sure if this is correct encoding
    '1/x': '26',
    'SF': '27',
    'CF': '28',
    'F?': '29',
    'DBLx': '20',
    'P/R': '31',
    'BST': '32',
    'R^': '33',
    'PSE': '34',
    'CLx': '35',
    'LSTx': '36', #* This key takes up 2 spaces, so I am not sure if this is correct
    'x<=y': '37',
    'x<0': '38',
    'x>y': '39',
    'x>0': '30',
    '<': '44',
    '>': '45',
    'x!=y': '47',
    'x!=0': '48',
    'x==y': '49',
    'x==0': '40'
}

# Handle the case of an int other than 0-10
def get_button(key):
    try:
        return buttons[key]
    except KeyError:
        return key