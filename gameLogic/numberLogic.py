import sympy as sp
import regex as re
from math import floor, ceil, log



def evaluateCostEquation(costEquation: str, *args: int, arglist: list = [None]) -> int | float:
    """
    Evaluates the cost equation.

    Args:
        costEquation (str): The cost equation to evaluate.
        *args: The arguments to put into the cost equation.

    Returns:
        int: The result of the cost equation.    
    """
    if not arglist[0] == None:
        args = tuple(arglist)
        
    # if there are too many arguments, it will break
    if f"%{len(args) + 1}%" in costEquation:
        raise ValueError(f"Incorrect number of arguments provided. Expected {costEquation.count("%")}, got {len(args)}")

    # if there are too few arguments, it will break
    if f"%{len(args)}%" in costEquation:
        raise ValueError(f"Incorrect number of arguments provided. Expected {costEquation.count("%")}, got {len(args)}")
    
    # break up the equation into a list of strings
    equation = splitCostEquation(costEquation)

    amountVarsFound = 1
    for i in range(len(equation)):
        # if it's a number, replace it with the argument
        if equation[i] == "%":
            equation[i] = str(args[amountVarsFound - 1])
            amountVarsFound += 1
    # join the list of strings into one string
    equation = "".join(equation)
    expr = sp.sympify(equation)
    result = expr.evalf()
    if type(result) == sp.Float:
        result = float(result)
    return result


def splitCostEquation(costEquation: str) -> list[str]:
    """
    Splits the cost equation into a list of strings.

    Args:
        costEquation (str): The cost equation to split.

    Returns:
        list[str]: The list of strings.
    """

    groups = []
    latestGroup = ""
    i = 0
    while i < len(costEquation):
        if costEquation[i] == "%":
            if latestGroup != "":
                groups.append(latestGroup)
                latestGroup = ""
            if costEquation[i + 1].isnumeric():
                groups.append("%")
                i = i + 1
        else:
            latestGroup += costEquation[i]
        i += 1
    if latestGroup != "":
        groups.append(latestGroup)
    return (groups)







def magnitude(number):
    if number == 0:
        return 0

    return int(log(number, 1000))

def nonilize(number):
    if number == 0:
        return 0

    k = 1000.0
    magnitude_ = magnitude(number)
    return '%.2f %s' % ((number*10) // (k**magnitude_) / 10, magnitudeDict[magnitude_ - 1])

def humanReadableNumber(number):
    if number == 0:
        return "0"
    if magnitude(number) > 100:
        if not len(str(number)) > 307: # max float size fix (also shout out to antimatter dimensions 1.79e308!!!)
            return '{:.2e}'.format(number)
        else:
            number = str(number)
            return number[1] + "." + number[2] + number[3] + "e" + str(len(number) - 1)
    else:
        if number < 1000:
            return str(number)
        elif number < 100_000:
            return '{:,}'.format(number)
        else:
            return nonilize(number)


magnitudeDict = {
    -1: "broken%",
    0:  "K",
    1:  "M",
    2:  "B",
    3:  "T",
    4:  "Qa",
    5:  "Qt",
    6:  "Sx",
    7:  "Sp",
    8:  "Oc",
    9:  "No",
    10:	"Dc",
    11:	"UDc",
    12:	"DDc",
    13:	"TDc",
    14:	"QaDc",
    15:	"QtDc",
    16:	"SxDc",
    17:	"SpDc",
    18: "ODc",
    19: "NDc",
    20: "Vg",
    21: "UVg",
    22: "DVg",
    23: "TVg",
    24: "QaVg",
    25: "QtVg",
    26: "SxVg",
    27: "SpVg",
    28: "OVg",
    29: "NVg",
    30: "Tg",
    31: "UTg",
    32: "DTg",
    33: "TTg",
    34: "QaTg",
    35: "QtTg",
    36: "SxTg",
    37: "SpTg",
    38: "OTg",
    39: "NTg",
    40: "Qd",
    41: "UQd",
    42: "DQd",
    43: "TQd",
    44: "QaQd",
    45: "QtQd",
    46: "SxQd",
    47: "SpQd",
    48: "OQd",
    49: "NQd",
    50: "Qi",
    51: "UQi",
    52: "DQi",
    53: "TQi",
    54: "QaQi",
    55: "QtQi",
    56: "SxQi",
    57: "SpQi",
    58: "OQi",
    59: "NQi",
    60: "Se",
    61: "USe",
    62: "DSe",
    63: "TSe",
    64: "QaSe",
    65: "QtSe",
    66: "SxSe",
    67: "SpSe",
    68: "OSe",
    69: "NSe",
    70: "St",
    71: "USt",
    72: "DSt",
    73: "TSt",
    74: "QaSt",
    75: "QtSt",
    76: "SxSt",
    77: "SpSt",
    78: "OSt",
    79: "NSt",
    80: "Og",
    81: "UOg",
    82: "DOg",
    83: "TOg",
    84: "QaOg",
    85: "QtOg",
    86: "SxOg",
    87: "SpOg",
    88: "OOg",
    89: "NOg",
    90: "Nn",
    91: "UNn",
    92: "DNn",
    93: "TNn",
    94: "QaNn",
    95: "QtNn",
    96: "SxNn",
    97: "SpNn",
    98:	"ONn",
    99:	"NNn",
    100: "Ce" 
}
