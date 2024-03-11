import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

# dictionary
opcode_mapping = {
    "add": ["0110011", "R"],
    "sub": ["0110011", "R"],
    "sll": ["0110011", "R"],
    "slt": ["0110011", "R"],
    "sltu": ["0110011", "R"],
    "xor": ["0110011", "R"],
    "srl": ["0110011", "R"],
    "or": ["0110011", "R"],
    "and": ["0110011", "R"],
    "lw": ["0000011", "I"],
    "addi": ["0010011", "I"],
    "sltiu": ["0010011", "I"],
    "jalr": ["1100111", "I"],
    "sw": ["0100011", "S"],
    "beq": ["1100011", "B"],
    "bne": ["1100011", "B"],
    "blt": ["1100011", "B"],
    "bge": ["1100011", "B"],
    "bltu": ["1100011", "B"],
    "bgeu": ["1100011", "B"],
    "lui": ["0110111", "U"],
    "auipc": ["0010111", "U"],
    "jal": ["1101111", "J"],
    # bonus instrictions:
    "mul": ["", ""],
    "rst": ["", ""],
    "halt": ["", ""],
    "rvrs": ["", ""],
}

label_dict = {}

registor = {
    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "fp": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111",
}

funct3_7_R = {'add': ['000', '0000000'], 'sub': ['000', '0100000'], 'sll': ['001', '0000000'],
              'slt': ['010', '0000000'], 'sltu': ['011', '0000000'], 'xor': ['100', '0000000'],
              'srl': ['101', '0000000'], 'or': ['110', '0000000'], 'and': ['111', '0000000']
              }

fh1 = open(input_file, "r")
fh2 = open(output_file, "w")


# CHECK FOR OPCODE VALIDITY
def CheckOpcodeValidity(line):
    cmd = line.split()[0]
    if (cmd in opcode_mapping.keys()):
        return True
    else:
        return False


# GET THE TYPE OF INSTRUCTION
def Type_Of_Instruction(line):
    if (CheckOpcodeValidity(line)):
        cmd = (line.strip()).split()[0]
        type = opcode_mapping[cmd][1]
    else:
        fh2.write("invalid instruction")
        fh1.close()
        exit()
    return type


def lenChecker(line):
    if CheckOpcodeValidity(line):
        line_split = [item for item in line.replace(',', ' ').split()]
        cmd = line_split[0]
        if opcode_mapping[cmd][1] == "R" and len(line_split) == 4:
            return True
        elif opcode_mapping[cmd][1] == "I" and (len(line_split) == 4 or len(line_split) == 3):
            return True
        elif opcode_mapping[cmd][1] == "S" and len(line_split) == 3:
            return True
        elif opcode_mapping[cmd][1] == "B" and len(line_split) == 4:
            return True
        elif opcode_mapping[cmd][1] == "U" and len(line_split) == 3:
            return True
        elif opcode_mapping[cmd][1] == "J" and len(line_split) == 3:
            return True
    else:
        return False


# VALID REGISTER
def Valid_Register(reg):
    if reg in registor.keys():
        return True
    else:
        return False


# VALID IMMEDIATE
def Valid_Immediate(line, imm):
    type = Type_Of_Instruction(line)

    if (type == "I" or type == "S" or type == "B"):
        if int(imm) >= -2 ** 11 or int(imm) <= 2 ** 11 - 1:
            return True
        else:
            fh2.write("ERROR")
    elif (type == "U" or type == "J"):
        if int(imm) in range(-2 ** 19, 2 ** 19 - 1):
            return True
    else:
        fh2.write("ERROR")
        exit()


# BINARY CONVERSION
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


def stringtoint(str):
    j = 0
    ans = 0
    for i in str[::-1]:
        ans += int(i) * pow(2, j)
        j = j + 1
    return ans


def comp(n):
    a = abs(n)
    b = bin(a)[2:]
    inverse_s = ''
    for i in b:

        if i == '0':
            inverse_s += '1'

        else:
            inverse_s += '0'

    sum = bin(stringtoint(inverse_s) + 1)
    sum = sum[2:]
    return sum


def bitext(str, n):
    if (str[0] == '1'):
        for i in range(n - len(str)):
            str = "1" + str
    else:
        for i in range(n - len(str)):
            str = "0" + str

    return str


def isLabel(imm):
    if (imm in label_dict.keys()):
        return True
    else:
        return False


def label_point(str):
    return label_dict[str]


def R_Type(line, line_count):
    line_split = [item for item in line.replace(',', ' ').split()]
    if (Valid_Register(line_split[1]) and Valid_Register(line_split[2]) and Valid_Register(
            line_split[3]) and lenChecker(line)):
        ans = ''
        ans += funct3_7_R[line_split[0]][1] + registor[line_split[3]] + registor[line_split[2]] + \
               funct3_7_R[line_split[0]][0]
        ans += registor[line_split[1]] + opcode_mapping[line_split[0]][0]
        fh2.write(ans)
        fh2.write('\n')
    else:
        fh2.write(f'invalid instruction at line {line_count}')
        fh2.close()
        fh1.close()
        exit()


def I_Type(str, line_count):
    l = str.split(" ")
    opcode = l[0]
    rest = l[1]
    l1 = rest.split(",")

    if (len(l1) == 3):
        rd = l1[0]
        rs = l1[1]
        imm = l1[2]
    else:
        rd = l1[0]
        l2 = l1[1].split("(")
        imm = l2[0]
        s = l2[1]
        rs = s[:len(s) - 1]

    if (CheckOpcodeValidity(opcode) and Valid_Register(rs) and Valid_Register(rd) and Valid_Immediate(str,
                                                                                                      imm) and lenChecker(
            line)):
        funct3 = {"lw": "010", "addi": "000", "sltiu": "011", "jalr": "000"}

        imm = Binary_Conversion(imm)
        imm2 = imm[::-1]
        ans = ""
        ans += imm2[11:0:-1] + imm2[0] + registor[rs] + funct3[opcode] + registor[rd] + opcode_mapping[opcode][0]
        fh2.write(ans)
        fh2.write('\n')
    else:
        fh2.write(f'invalid instruction at line {line_count}')
        fh2.close()
        fh1.close()
        exit()


def J_Type(line, line_count):
    line_split = [item for item in line.replace(',', ' ').split()]
    reg = line_split[1]
    imm = line_split[2]
    if (CheckOpcodeValidity(line_split[0]) and Valid_Register(reg) and Valid_Immediate(line, imm) and lenChecker(line)):
        Bin_Converted = Binary_Conversion(imm)
        Bin_reverse = Bin_Converted[::-1]
        ans = ""
        ans += Bin_reverse[20] + Bin_reverse[10:1:-1] + Bin_reverse[1] + Bin_reverse[11] + Bin_reverse[19:12:-1] + \
               Bin_reverse[12] + registor[reg] + opcode_mapping[line_split[0]][0]
        fh2.write(ans)
        fh2.write('\n')
    else:
        fh2.write(f'invalid instruction at line {line_count}')
        fh2.close()
        fh1.close()
        exit()


def U_Type(line, line_count):
    line_split = [item for item in line.replace(',', ' ').split()]
    reg = line_split[1]
    imm = line_split[2]
    if (CheckOpcodeValidity(line_split[0]) and Valid_Register(reg) and Valid_Immediate(line, imm) and lenChecker(line)):
        Bin_Converted = Binary_Conversion(imm)
        Bin_reverse = Bin_Converted[::-1]
        Bin_ans = Bin_reverse[12:32]
        Bin_final = Bin_ans[::-1]
        final_ans = ''
        final_ans += Bin_final
        final_ans += registor[reg]
        final_ans += opcode_mapping[line_split[0]][0]
        fh2.write(final_ans)
        fh2.write('\n')
    else:
        fh2.write(f'invalid instruction at line {line_count}')
        fh2.close()
        fh1.close()
        exit()


def S_Type(str, line_count):
    l = str.split(" ")
    opcode = l[0]
    rest = l[1]
    l1 = rest.split(",")
    rs1 = l1[0]
    l2 = l1[1].split("(")
    imm = l2[0]
    s = l2[1]
    rs2 = s[:len(s) - 1]
    if (CheckOpcodeValidity(opcode) and Valid_Register(rs1) and Valid_Register(rs2) and Valid_Immediate(str, imm) and lenChecker(line)):
        imm = Binary_Conversion(imm)
        imm2 = imm[::-1]
        fh2.write(imm2[11:4:-1] + registor[rs1] + registor[rs2] + '010' + imm2[4:0:-1] + imm2[0] + '0100011')
        fh2.write('\n')
    else:
        fh2.write(f'invalid instruction at line {line_count}')
        fh2.close()
        fh1.close()
        exit()


def B_Type(line, line_address, line_count):
    func3 = {"beq": "000", "bne": "001", "blt": "100", "bge": "101", "bltu": "110", "bgeu": "111"}
    line_split = [item for item in line.replace(',', ' ').split()]
    cmd = line_split[0]
    rs1 = line_split[1]
    rs2 = line_split[2]
    imm = line_split[3]
    if (imm.isdigit()):
        if (CheckOpcodeValidity(cmd) and Valid_Register(rs1) and Valid_Register(rs2) and Valid_Immediate(line,
                                                                                                         imm) and lenChecker(
                line)):
            imm = Binary_Conversion(imm)
            imm2 = imm[::-1]
            ans = ""
            ans += imm2[12] + imm2[10:5:-1] + imm2[5] + registor[rs2] + registor[rs1] + func3[cmd] + imm2[4:1:-1] + \
                   imm2[1] + imm2[11] + opcode_mapping[cmd][0]
            fh2.write(ans)
            fh2.write('\n')
        else:
            fh2.write(f'invalid instruction at line {line_count}')
            fh2.close()
            fh1.close()
            exit()
    elif (isLabel(imm)):
        if (CheckOpcodeValidity(cmd) and Valid_Register(rs1) and Valid_Register(rs2) and lenChecker(line)):

            num = label_point(imm) - line_address
            imm = Binary_Conversion(str(num))[::-1]
            ans = ""
            ans += imm[12] + imm[10:5:-1] + imm[5] + registor[rs2] + registor[rs1] + func3[cmd] + imm[4:1:-1] + imm[1] + \
                   imm[11] + opcode_mapping[cmd][0]
            fh2.write(ans)
            fh2.write('\n')
        else:
            fh2.write(f'invalid instruction at line {line_count}')
            fh2.close()
            fh1.close()
            exit()
    else:
        fh2.write(f'invalid instruction at line {line_count}')
        fh2.close()
        fh1.close()
        exit()


# CODE FOR LABEL INSTRUCTION
def Label_Instr(line, label_name, line_address, line_count):
    if label_name in label_dict:
        if CheckOpcodeValidity(line):
            instr_type = Type_Of_Instruction(line)
            if (instr_type == 'I'):
                I_Type(line)
            elif (instr_type == 'J'):
                J_Type(line)
            elif (instr_type == 'R'):
                R_Type(line)
            elif (instr_type == 'S'):
                S_Type(line)
            elif (instr_type == 'U'):
                U_Type(line)
            elif (instr_type == 'B'):
                B_Type(line, line_address)
        else:
            fh2.write(f'invalid instruction at line {line_count}')
            fh2.close()
            fh1.close()
            exit()
    else:
        fh2.write(f'invalid instruction at line {line_count}')
        fh1.close()
        exit()


# CHECK IF THE INSTRUCTION IS A LABEL INSTRUCTION OR NOT

def Get_Label_Name(line):
    line_split = [item for item in line.replace(',', ' ').split()]
    return line_split[0][:-1]


def Chk_Label_Instr(line):
    line_split = [item for item in line.replace(',', ' ').split()]
    if (line_split[0][-1] == ':'):
        return True
    else:
        return False


lines = [line.strip() for line in fh1.readlines()]
lines = list(filter(None, lines))
line_count = 1
virtual_halt = 'beq zero,zero,0'

if (lines[-1] == virtual_halt):
    line_address = 0
    # get label address
    for line in lines:
        if Chk_Label_Instr(line):
            label_name = Get_Label_Name(line)
            if (label_name not in label_dict):
                label_dict[label_name] = line_address
        line_address += 4

    line_address = 0

    for line in lines:
        if (line == virtual_halt):
            B_Type(line, line_address, line_count)
            fh2.close()
            fh1.close()
            exit()

        elif Chk_Label_Instr(line):
            label_name = Get_Label_Name(line)
            line = line.replace(f'{label_name}: ', '')
            Label_Instr(line, label_name, line_address, line_count)

        elif CheckOpcodeValidity(line) and lenChecker(line):
            type = Type_Of_Instruction(line)
            if (type == 'R'):
                # print('hi')
                R_Type(line, line_count)
            elif (type == 'S'):
                S_Type(line, line_count)
            elif (type == 'I'):
                I_Type(line, line_count)
            elif (type == 'J'):
                J_Type(line, line_count)
            elif (type == 'B'):
                B_Type(line, line_address, line_count)
            elif (type == 'U'):
                U_Type(line, line_count)
        else:

            fh2.write(f'invalid instruction at line {line_count}')
            fh2.close()
            fh1.close()
            exit()
        line_address += 4
        line_count += 1

else:
    fh2.write('invalid syntax at last line')
    fh2.close()
    fh1.close()
    exit()

fh2.close()
fh1.close()
