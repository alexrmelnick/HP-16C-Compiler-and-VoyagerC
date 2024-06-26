f_modifier_instrs = [
    'CLEAR REG',
    'X<=>(i)',
    'X<=>I',
    'SHOW HEX',
    'SHOW DEC',
    'SHOW OCT',
    'SHOW BIN',
    'SL',
    'SR',
    'RL',
    'RR',
    'RLn',
    'RRn',
    'MASKL',
    'MASKR',
    'RMD',
    'XOR',
    'WSIZE',
    'FLOAT',
    'SB',
    'CB',
    'B?',
    'AND',
    'WINDOW',
    '1s',
    '2s',
    'UNSGN',
    'NOT',
    'EEX',
    'OR'
]

g_modifier_instrs = [
    'R^',
    'PSE',
    'CLX',
    'RTN',
    'LBL',
    'DSZ',
    'ISZ',
    'SQRTx',
    '1/x',
    'LJ',
    'ASR',
    'RLC',
    'RRC',
    'RLCn',
    'RRCn',
    '#B',
    'ABS',
    'DBLR',
    'DBL/',
    '<',
    '>',
    'SF',
    'CF',
    'F?',
    'DBLx',
    'X<=Y',
    'X<0',
    'X>Y',
    'X>0',
    'LSTx',
    'X!=Y',
    'X!=0',
    'X==Y',
    'X==0'
]

button_positions = {
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
    'Rv': '33',
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
    'SHOW HEX': '23', #* This is a special case because it has a space in the instruction
    'SHOW DEC': '24',
    'SHOW OCT': '25',
    'SHOW BIN': '26',
    'AND': '20',
    '(i)': '31',
    'I': '32',
    'i': '32', # I dont know why this is being passes as lower case
    'CLEAR PRGM': '33', #* This is a special case because it has a space in the instruction
    'CLEAR REG': '34',
    'CLEAR PREFIX': '35',
    'WINDOW': '36', #? This key takes up 2 spaces, so I am not sure if this is correct
    '1s': '37',
    '2s': '38',
    # 'UNSGN': '39',    # I believe there is a bug in JRPN with the UNSGN key position, but this is what the export file outputs for it so thats the way it goes
    'UNSGN': '3',
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
    '#B': '17', #* This is a special case because it has a hashtag in the instruction
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
    'X<=Y': '37',
    'X<0': '38',
    'X>Y': '39',
    'X>0': '30',
    '<': '44',
    '>': '45',
    'X!=Y': '47',
    'X!=0': '48',
    'X==Y': '49',
    'X==0': '40',
    'SB': '27',
    'B?': '29',
}

mnemonic_to_instr = {
    '+': '+',
    '-': '-',
    '*': '*',
    '/': '/',
    'rmd': 'RMD',
    'abs': 'ABS',
    'sqrt': 'SQRTx',
    'sqrtx': 'SQRTx',
    '1/x': '1/x',
    'and': 'AND',
    'or': 'OR',
    'xor': 'XOR',
    'not': 'NOT',
    'sl': 'SL',
    'sr': 'SR',
    'lj': 'LJ',
    'asr': 'ASR',
    'asl': 'SL',
    'rl': 'RL',
    'rr': 'RR',
    'rlc': 'RLC',
    'rrc': 'RRC',
    'rln': 'RLn',
    'rrn': 'RRn',
    'rlcn': 'RLCn',
    'rrcn': 'RRCn',
    'sb': 'SB',
    'cb': 'CB',
    'maskl': 'MASKL',
    'maskr': 'MASKR',
    '#b': '#B',
    'dbl*': 'DBLx',
    'dbl/': 'DBL/',
    'dblrmd': 'DBLR',
    'enter': 'ENTER',
    'r^': 'R^',
    'rv': 'Rv',
    'x<>y': 'X<=>Y',
    'x<=>y': 'X<=Y',
    'x<>i': 'X<=>I',
    'x<=>i': 'X<=>I',
    'x<>(i)': 'X<=>(i)',
    'x<=>(i)': 'X<=>(i)',
    'clx': 'CLx',
    'sto': 'STO',
    'rcl': 'RCL',
    '(i)': '(i)',
    'i': 'I',
    'sf': 'SF',
    'cf': 'CF',
    'lbl': 'LBL',
    'gto': 'GTO',
    'gsb': 'GSB',
    'rtn': 'RTN',
    'dsz': 'DSZ',
    'isz': 'ISZ',
    'x<=y': 'X<=Y',
    'x>y': 'X>Y',
    'x=y': 'X==Y',
    'x==y': 'X==Y',
    'x!=y': 'X!=Y',
    'x/=y': 'X!=Y',
    'x<0': 'X<0',
    'x>0': 'X>0',
    'x=0': 'X==0',
    'x==0': 'X==0',
    'x!=0': 'X!=0',
    'x/=0': 'X!=0',
    'b?': 'B?',
    'f?': 'F?',
    'hex': 'HEX',
    'dec': 'DEC',
    'oct': 'OCT',
    'bin': 'BIN',
    'wsize': 'WSIZE',
    'unsigned': 'UNSGN',
    'unsgn': 'UNSGN',
    '1\'s': '1s',
    '1s': '1s',
    '2\'s': '2s',
    '2s': '2s',
    'float': 'FLOAT',
    'show': 'SHOW',
    'pse': 'PSE',
    'window': 'WINDOW',
    '<': '<',
    '>': '>',
    'r/s': 'R/S',
    'clear': 'CLEAR',
    'chs': 'CHS',
    'eex': 'EEX',  
    '.': '.',
}

instructions_with_arguments = [
    'sto',
    'rcl',
    'sf',
    'cf',
    'f?',
    'sb',
    'cb',
    'b?',
    'lbl',
    'gto',
    'gsb',
    'show',
    'float',
    'window',
    'clear'
]