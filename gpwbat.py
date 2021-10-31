import glob
import argparse

# discharge curve
table = {
    100: 4.186,
    99: 4.156,
    98: 4.143,
    97: 4.133,
    96: 4.122,
    95: 4.113,
    94: 4.103,
    93: 4.094,
    92: 4.086,
    91: 4.076,
    90: 4.067,
    89: 4.060,
    88: 4.051,
    87: 4.043,
    86: 4.036,
    85: 4.027,
    84: 4.019,
    83: 4.012,
    82: 4.004,
    81: 3.997,
    80: 3.989,
    79: 3.983,
    78: 3.976,
    77: 3.969,
    76: 3.961,
    75: 3.955,
    74: 3.949,
    73: 3.942,
    72: 3.935,
    71: 3.929,
    70: 3.922,
    69: 3.916,
    68: 3.909,
    67: 3.902,
    66: 3.896,
    65: 3.890,
    64: 3.883,
    63: 3.877,
    62: 3.870,
    61: 3.865,
    60: 3.859,
    59: 3.853,
    58: 3.848,
    57: 3.842,
    56: 3.837,
    55: 3.833,
    54: 3.828,
    53: 3.824,
    52: 3.819,
    51: 3.815,
    50: 3.811,
    49: 3.808,
    48: 3.804,
    47: 3.800,
    46: 3.797,
    45: 3.793,
    44: 3.790,
    43: 3.787,
    42: 3.784,
    41: 3.781,
    40: 3.778,
    39: 3.775,
    38: 3.772,
    37: 3.770,
    36: 3.767,
    35: 3.764,
    34: 3.762,
    33: 3.759,
    32: 3.757,
    31: 3.754,
    30: 3.751,
    29: 3.748,
    28: 3.744,
    27: 3.741,
    26: 3.737,
    25: 3.734,
    24: 3.730,
    23: 3.726,
    22: 3.724,
    21: 3.720,
    20: 3.717,
    19: 3.714,
    18: 3.710,
    17: 3.706,
    16: 3.702,
    15: 3.697,
    14: 3.693,
    13: 3.688,
    12: 3.683,
    11: 3.677,
    10: 3.671,
    9: 3.666,
    8: 3.662,
    7: 3.658,
    6: 3.654,
    5: 3.646,
    4: 3.633,
    3: 3.612,
    2: 3.579,
    1: 3.537,
    0: 3.500
}

parser = argparse.ArgumentParser()
parser.add_argument("-o", help="What gpwbat should print. Possible values are: `voltage`, `percentage`, or `both`. Defaults to percentage.", default="percentage")
args = parser.parse_args()

def getBatteryPath() -> str:
    # get the directory of every entry under power_supply
    possible = glob.glob("/sys/class/power_supply/*/*")
    for entry in possible:
        if "model_name" in entry:
            with open(entry) as f:
                if f.readline().strip() == "G Pro Wireless Gaming Mouse":
                    return entry.rstrip("/model_name")
    return ""

def printStatus(bpath : str):
    if bpath == "":
        print("Could not find battery path. Verify that your mouse appears under /sys/class/power_supply/ and try again.")
        return
    
    # read voltage
    with open(bpath+"/voltage_now") as f:
        voltage = float(f.readline().strip())/1000000
        if voltage > table[100]:
            if args.o == "percentage":
                print("100%")
            elif args.o == "voltage":
                print(f'{voltage}V')
            elif args.o == "both":
                print(f'{voltage}V 100%')
            else:
                print("100%")
        elif voltage < table[0]:
            if args.o == "percentage":
                print("0%")
            elif args.o == "voltage":
                print(f'{voltage}V')
            elif args.o == "both":
                print(f'{voltage}V 0%')
            else:
                print("0%")
        else:
            ck, cv = min(table.items(), key=lambda x: abs(voltage - x[1]))
            if args.o == "percentage":
                print(f'{ck}%')
            elif args.o == "voltage":
                print(f'{voltage}V')
            elif args.o == "both":
                print(f'{voltage}V {ck}%')
            else:
                print(f'{ck}%')


printStatus(getBatteryPath())