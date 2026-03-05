# symbols for z numbers
SYMBOLS = {
    1: "H",   2: "He",  3: "Li",  4: "Be",  5: "B",
    6: "C",   7: "N",   8: "O",   9: "F",  10: "Ne",
    11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P",
    16: "S",  17: "Cl", 18: "Ar", 19: "K",  20: "Ca",
    21: "Sc", 22: "Ti", 23: "V",  24: "Cr", 25: "Mn",
    26: "Fe", 27: "Co", 28: "Ni", 29: "Cu", 30: "Zn",
    31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br",
    36: "Kr", 37: "Rb", 38: "Sr", 39: "Y",  40: "Zr",
    41: "Nb", 42: "Mo", 43: "Tc", 44: "Ru", 45: "Rh",
    46: "Pd", 47: "Ag", 48: "Cd", 49: "In", 50: "Sn",
    51: "Sb", 52: "Te", 53: "I",  54: "Xe", 55: "Cs",
    56: "Ba", 57: "La", 58: "Ce", 59: "Pr", 60: "Nd",
    61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd", 65: "Tb",
    66: "Dy", 67: "Ho", 68: "Er", 69: "Tm", 70: "Yb",
    71: "Lu", 72: "Hf", 73: "Ta", 74: "W",  75: "Re",
    76: "Os", 77: "Ir", 78: "Pt", 79: "Au", 80: "Hg",
    81: "Tl", 82: "Pb", 83: "Bi", 84: "Po", 85: "At",
    86: "Rn", 87: "Fr", 88: "Ra", 89: "Ac", 90: "Th",
    91: "Pa", 92: "U",  93: "Np", 94: "Pu", 95: "Am",
    96: "Cm", 97: "Bk", 98: "Cf", 99: "Es",100: "Fm",
    101:"Md", 102:"No", 103:"Lr", 104:"Rf", 105:"Db",
    106:"Sg", 107:"Bh", 108:"Hs", 109:"Mt", 110:"Ds",
    111:"Rg", 112:"Cn", 113:"Nh", 114:"Fl", 115:"Mc",
    116:"Lv", 117:"Ts", 118:"Og"
}

# labels for l numbers
LABELS = {0: 's', 1: 'p', 2: 'd', 3: 'f'}

# max n number
MAX_N = 8

# ecceptions to aufbau's principle
EXCEPTIONS = {
    24: (  # Cr
        3,
        [
            (4, 0, 0, -0.5), (3, 2, -2, -0.5),
            (3, 2, -1, -0.5), (3, 2, 0, -0.5), (3, 2, 1, -0.5), (3, 2, 2, -0.5)
        ]
    ),
    29: (  # Cu
        3,
        [
            (4, 0, 0, -0.5), (3, 2, -2, -0.5), (3, 2, -1, -0.5), 
            (3, 2, 0, -0.5), (3, 2, 1, -0.5), (3, 2, 2, -0.5), (3, 2, -2, 0.5),
            (3, 2, -1, 0.5), (3, 2, 0, 0.5), (3, 2, 1, 0.5), (3, 2, 2, 0.5)
        ]
    ),
    41: (  # Nb
        4,
        [
            (5, 0, 0, -0.5), (4, 2, -2, -0.5), (4, 2, -1, -0.5), 
            (4, 2, 0, -0.5), (4, 2, 1, -0.5), (4, 2, 2, -0.5)
        ]
    ),
    42: (  # Mo
        5,
        [
            (5, 0, 0, -0.5), (4, 2, -2, -0.5), (4, 2, -1, -0.5), 
            (4, 2, 0, -0.5), (4, 2, 1, -0.5), (4, 2, 2, -0.5)
        ]
    ),
    47: (  # Ag
        5,
        [
            (5, 0, 0, -0.5), (4, 2, -2, -0.5), (4, 2, -1, -0.5), 
            (4, 2, 0, -0.5), (4, 2, 1, -0.5), (4, 2, 2, -0.5), (4, 2, -2, 0.5), 
            (4, 2, -1, 0.5), (4, 2, 0, 0.5), (4, 2, 1, 0.5), (4, 2, 2, 0.5)
        ]
    ),
    79: (  # Au
        6,
        [
            (6, 0, 0, -0.5), (5, 2, -2, -0.5), (5, 2, -1, -0.5), 
            (5, 2, 0, -0.5), (5, 2, 1, -0.5), (5, 2, 2, -0.5), (5, 2, -2, 0.5),
            (5, 2, -1, 0.5), (5, 2, 0, 0.5), (5, 2, 1, 0.5), (5, 2, 2, 0.5)
        ]
    )
}

def aufbau(z):
    # generate all (n, l) combinations
    nls = [
        (n, l)
        for n in range(1, MAX_N + 1)
        for l in range(0, n)
    ]
    
    # sort (n, l) combinations by aufbau
    nls.sort(key=lambda x: (x[0] + x[1], x[0]))

    # compute electron states
    states = [
        (n, l, m_l, m_s)
        for n, l in nls
        for m_s in [-0.5, 0.5]
        for m_l in range(-l, l + 1)
    ]

    # get if element has exception
    exc = EXCEPTIONS.get(z)

    # yield first z electron states
    for i, elec in enumerate(states):
        if i >= z:
            break

        # if exception, yield that
        if exc is not None and elec[0] > exc[0]:
            for exc_elec in exc[1]:
                yield exc_elec
            return
        
        yield elec

def subshells(z):
    # initialize counters for configuration
    subshells = [] # will contain the subshells
    prev_n = 1     # previous n number
    prev_l = 0     # previous l number

    # initialize eletron state generator
    elecs = aufbau(z)
    elec = next(elecs) # get first electron state

    # go through all electron states
    while True:
        # initialize this subshell
        subshell = [prev_n, prev_l, 0]

        # fill it with all electron states matching n, l
        while(elec[0] == prev_n and elec[1] == prev_l):
            subshell[2] += 1

            # try getting next electron state
            try:
                elec = next(elecs)
            except StopIteration:
                # add half filled subshell and return
                subshells.append(subshell)
                return subshells
            
        # add subshell and move to next one
        subshells.append(subshell)
        prev_n = elec[0]
        prev_l = elec[1]

def get_noble(z):
    def block(n):
        return 2 * n ** 2

    noble = 0 # z number of noble gas
    row = 1   # distinguishes between the two rows periodic table blocks 
              # increase by 
    n = 1     # n number of noble gas

    # go through each row finding the biggest noble gas
    while noble + block(n) < z:
        # clamp row and increase n if needed
        if row >= 2:
            row = 0
            n += 1

        # go thorugh the next period
        noble += block(n) 
        row += 1

    return noble, n

# get z number
z = int(input("Enter Z number: "))
if z <= 0:
    print("Z number cannot be lower than 1")
    exit()

# print basic info
print("\n# ELEMENT")

print(f"Element with z = {z}, symbol [{SYMBOLS.get(z)}]")

# print all electron states
print("\n# ELECTRON STATES")

print("n\tl\tm_l\tm_e")
for n, l, m_l, m_s in aufbau(z):
    print(f"{n}\t{l}\t{m_l}\t{m_s}")

# print electron configuration
print("\n# CONFIGURATION")

# get first noble gas and print it
noble, noble_n = get_noble(z)
if noble != 0:    
    print(f"[{SYMBOLS.get(noble)}] ", end=' ')

# print all subshells after the noble gas
in_noble = noble != 0
for n, l, c in subshells(z):
    if in_noble and n != noble_n + 1: continue
    
    in_noble = False
    print(f"{n}{LABELS.get(l)}^{c} ", end=' ')
print()

# print expanded electron configuration
print("\n# EXPANDED CONFIGURATION")

for n, l, c in subshells(z):
    print(f"{n}{LABELS.get(l)}^{c} ", end=' ')
print()
