import sys

input_file = sys.argv[1]
output_file = sys.argv[2]
from bitstring import BitArray

fh1 = open(input_file, 'r')
fh2 = open(output_file, 'w')

memory = {
    '0x00010000': 0,
    '0x00010004': 0,
    '0x00010008': 0,
    '0x0001000c': 0,
    '0x00010010': 0,
    '0x00010014': 0,
    '0x00010018': 0,
    '0x0001001c': 0,
    '0x00010020': 0,
    '0x00010024': 0,
    '0x00010028': 0,
    '0x0001002c': 0,
    '0x00010030': 0,
    '0x00010034': 0,
    '0x00010038': 0,
    '0x0001003c': 0,
    '0x00010040': 0,
    '0x00010044': 0,
    '0x00010048': 0,
    '0x0001004c': 0,
    '0x00010050': 0,
    '0x00010054': 0,
    '0x00010058': 0,
    '0x0001005c': 0,
    '0x00010060': 0,
    '0x00010064': 0,
    '0x00010068': 0,
    '0x0001006c': 0,
    '0x00010070': 0,
    '0x00010074': 0,
    '0x00010078': 0,
    '0x0001007c': 0,
}

register_track = {
    "zero": 0,
    "ra": 0,
    "sp": 256,
    "gp": 0,
    "tp": 0,
    "t0": 0,
    "t1": 0,
    "t2": 0,
    "s0": 0,
    # "fp": 0,
    "s1": 0,
    "a0": 0,
    "a1": 0,
    "a2": 0,
    "a3": 0,
    "a4": 0,
    "a5": 0,
    "a6": 0,
    "a7": 0,
    "s2": 0,
    "s3": 0,
    "s4": 0,
    "s5": 0,
    "s6": 0,
    "s7": 0,
    "s8": 0,
    "s9": 0,
    "s10": 0,
    "s11": 0,
    "t3": 0,
    "t4": 0,
    "t5": 0,
    "t6": 0,
}

registor = {
    "00000": "zero",
    "00001": "ra",
    "00010": "sp",
    "00011": "gp",
    "00100": "tp",
    "00101": "t0",
    "00110": "t1",
    "00111": "t2",
    "01000": "s0",
    # "01000": "fp",
    "01001": "s1",
    "01010": "a0",
    "01011": "a1",
    "01100": "a2",
    "01101": "a3",
    "01110": "a4",
    "01111": "a5",
    "10000": "a6",
    "10001": "a7",
    "10010": "s2",
    "10011": "s3",
    "10100": "s4",
    "10101": "s5",
    "10110": "s6",
    "10111": "s7",
    "11000": "s8",
    "11001": "s9",
    "11010": "s10",
    "11011": "s11",
    "11100": "t3",
    "11101": "t4",
    "11110": "t5",
    "11111": "t6",
}

virtual_halt = '00000000000000000000000001100011'
PC = 0


def findTwoscomplement(str):
    n = len(str)
    i = n - 1

    while (i >= 0):
        if (str[i] == '1'):
            break
        i -= 1

    if (i == -1):
        return '1' + str

    k = i - 1
    while (k >= 0):

        if (str[k] == '1'):
            str = list(str)
            str[k] = '0'
            str = ''.join(str)
        else:
            str = list(str)
            str[k] = '1'
            str = ''.join(str)
        k -= 1
    return str


# signed
def btod(val):
    if (val[0] == '0'):
        return int(val, 2)
    else:
        val_final = findTwoscomplement(val)
        return -1 * int(val_final, 2)


# unsigned
def unsigned(bString):
    value = BitArray(bin=bString).uint
    return value


def Binary_Conversion(num):
    ans = '{0:032b}'.format(int(num))
    if (int(num) >= 0):
        return ans
    else:
        index = 0
        for i in range(len(ans) - 1, 0, -1):
            if (ans[i] == "1"):
                index = i
                break

        for i in range(index - 1, -1, -1):
            if (ans[i] == "1"):
                ans = ans[:i] + "0" + ans[i + 1:]
            else:
                ans = ans[:i] + "1" + ans[i + 1:]

        return ans


def extension(l):
    l=l[2:]
    l=l.zfill(8)
    l="0x"+l
    return l




def simulator(line):
    global PC
    global register_track
    global registor
    global memory
    opcode = line[25:]
    func3 = line[17:20]
    rd = line[20:25]
    rs1 = line[12:17]
    rs2 = line[7:12]
    func7 = line[0:7]

    # R-TYPE INSTRUCTION
    if opcode == '0110011':
        if (func3 == '000'):
            if (func7 == '0000000'):
                register_track[registor[rd]] = register_track[registor[rs1]] + register_track[registor[rs2]]
                PC = PC + 4
            elif (func7 == '0100000'):
                register_track[registor[rd]] = register_track[registor[rs1]] - register_track[registor[rs2]]
                PC = PC + 4
        if (func3 == '001'):
            shift_amount = Binary_Conversion(register_track[registor[rs2]])[-5:]
            val=unsigned(shift_amount)
            register_track[registor[rd]] = register_track[registor[rs1]] << val
            PC = PC + 4

        # doubtful
        if (func3 == '010'):
            # slt instruction
            signed_rs1 = register_track[registor[rs1]]
            signed_rs2 = register_track[registor[rs2]]
            if signed_rs1 < signed_rs2:
                register_track[registor[rd]] = 1
            else:
                register_track[registor[rd]] = 0
            PC = PC + 4

        # sltu
        if (func3 == '011'):
            if unsigned(Binary_Conversion(register_track[registor[rs1]])) < unsigned(Binary_Conversion(register_track[registor[rs2]])):
                register_track[registor[rd]] = 1
            else:
                register_track[registor[rd]] = 0
            PC = PC + 4

        if (func3 == '100'):
            register_track[registor[rd]] = register_track[registor[rs1]] ^ register_track[registor[rs2]]
            PC = PC + 4

        if (func3 == '101'):
            # doubtful
            shift_amount = Binary_Conversion(register_track[registor[rs2]])[-5:]
            val = unsigned(shift_amount)
            register_track[registor[rd]] = register_track[registor[rs1]] >> val
            PC = PC + 4

        if (func3 == '110'):
            register_track[registor[rd]] = register_track[registor[rs1]] | register_track[registor[rs2]]
            PC = PC + 4

        if (func3 == '111'):
            register_track[registor[rd]] = register_track[registor[rs1]] & register_track[registor[rs2]]
            PC = PC + 4

    # I-TYPE INSTRUCTION
    elif (opcode == '0000011'):
        imm1 = line[0:12]
        final_imm = imm1 + imm1[0] * 20
        s = extension(f'{hex((register_track[registor[rs1]] + btod(final_imm)))}')
        register_track[registor[rd]] = memory[s]
        PC = PC + 4
    elif (opcode == '0010011'):
        if func3 == '000':
            imm1 = line[0:12]
            final_imm = imm1[0] * 20 + imm1
            register_track[registor[rd]] = register_track[registor[rs1]] + btod(final_imm)
            PC = PC + 4
        if func3 == '011':
            imm1 = line[0:12]
            final_imm = imm1[0] * 20 + imm1
            if unsigned(Binary_Conversion(register_track[registor[rs1]])) < unsigned(final_imm):
                register_track[registor[rd]] = 1
                PC = PC + 4
            else:
                register_track[registor[rd]] = 0
                PC = PC + 4

    elif (opcode == '1100111'):
        imm1 = line[0:12]
        final_imm = imm1[0] * 20 + imm1
        register_track[registor[rd]] = PC + 4
        pc = register_track[registor[rs1]] + btod(final_imm)
        if (pc % 2 != 0):
            pc = pc - 1
        PC = pc

    # S-TYPE INSTRUCTION
    elif (opcode == '0100011'):
        imm1 = func7 + rd
        final_imm = imm1[0] * 20 + imm1
        s = extension(f'{hex((register_track[registor[rs1]] + btod(final_imm)))}')

        # print(register_track[registor[rs1]] + btod(imm1))
        memory[s] = register_track[registor[rs2]]
        PC = PC + 4

    # U-TYPE INSTRUCTION
    elif (opcode == '0110111'):
        final_imm = line[0:20]
        register_track[registor[rd]] = btod((final_imm + "000000000000"))
        PC = PC + 4
    elif (opcode == '0010111'):
        final_imm = line[0:20]
        register_track[registor[rd]] = PC + btod((final_imm + "000000000000"))
        PC = PC + 4

    # B-TYPE INSTRUCTION
    elif (opcode == '1100011'):
        imm1 = line[0:7]
        imm2 = line[20:25]
        final_imm = imm1[0] * 20 + imm2[-1] + imm1[1:] + imm2[0:-1] + '0'
        final_imm = btod(final_imm)
        # beq instruction:
        if (func3 == '000'):
            if (register_track[registor[rs1]] == register_track[registor[rs2]]):
                PC = PC + final_imm

            else:
                PC = PC + 4
        # bne
        if (func3 == '001'):
            if (register_track[registor[rs1]] != register_track[registor[rs2]]):
                PC = PC + final_imm
            else:
                PC = PC + 4
        # blt signed value
        if (func3 == '100'):
            if (register_track[registor[rs1]] < register_track[registor[rs2]]):
                PC = PC + final_imm
            else:
                PC = PC + 4
        # bge
        if (func3 == '101'):
            if (register_track[registor[rs1]] > register_track[registor[rs2]]):
                PC = PC + final_imm
            else:
                PC = PC + 4
        # bltu
        if (func3 == '110'):
            if (unsigned(Binary_Conversion(register_track[registor[rs1]])) < unsigned(Binary_Conversion(register_track[registor[rs2]]))):
                PC = PC + final_imm
            else:
                PC = PC + 4
        # #bgeu
        if (func3 == '111'):
            if (unsigned(Binary_Conversion(register_track[registor[rs1]])) > unsigned(Binary_Conversion(register_track[registor[rs2]]))):
                PC = PC + final_imm
            else:
                PC = PC + 4

    # J-TYPE INSTRUCTION
    elif (opcode == '1101111'):
        start_imm = line[0:20]
        register_track[registor[rd]] = PC + 4
        final_imm = start_imm[0] * 12 + start_imm[12:] + start_imm[11] + start_imm[1:11] + '0'
        final_imm = btod(final_imm)
        PC = PC + final_imm
        if (PC % 2 != 0):
            PC = PC - 1



lines = [line.rstrip() for line in fh1.readlines()]
lines = list(filter(None, lines))
lines_count = len(lines)

while (PC <= 4 * lines_count and lines[PC//4] != virtual_halt):
    # doubt, pc is to be written after instruction call or before
    simulator(lines[PC//4])
    register_track['zero'] = 0
    fh2.write('0b' + Binary_Conversion(PC) + ' ')
    for i in register_track.keys():
        fh2.write('0b' + Binary_Conversion(register_track[i]) + ' ')
    fh2.write('\n')

fh2.write('0b' + Binary_Conversion(PC) + ' ')
for i in register_track.keys():
    fh2.write('0b' + Binary_Conversion(register_track[i]) + ' ')
fh2.write('\n')

for i in memory.keys():
    fh2.write(i + ':' + '0b' + Binary_Conversion(memory[i]))
    fh2.write('\n')