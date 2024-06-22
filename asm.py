from termcolor import colored

class Data:
    name = "" 
    type = ""
    value = ""
    def __str__(self) -> str:
        return f"name: {self.name}, type: {self.type}, value: {self.value}"

class Code:
    instruction = ""
    inputs = []
    def __str__(self) -> str:
        return f"instruction: {self.instruction}, inputs: {self.inputs}"

class Label:
    name = ""
    address = ""
    def __str__(self) -> str:
        return f"name: {self.name}, address: {self.address}"

def cmp(a, b):
    return not((a > b) - (a < b)) 

def isData(Data):
    for data in datas:
        if (data.name == Data):
            return True
    return False

def isReg(data):
    for register in registers:
        if (data == register or data == register[1:] or data == register[1] + 'h' or data == register[1] + 'l'):
            return True
    return False

def valueFinder(dataName, type):
    for data in datas:
        if (data.name == dataName):
            if (data.type == type or data.type == 's' + type):
                return data.value
            else:
                return None

def typeFinder(dataName):
    for data in datas:
        if (data.name == dataName):
            return data.type

def sizeFixer(value, bit, sign):
    length = len(value)
    if (length == bit):
        return value
    elif (length < bit):
        if (sign == "f"):
            value = ((bit - length) * "f") + value
        elif (sign == 0):
            value = ((bit - length) * "0") + value
        else:
            value = ((bit - length) * "1") + value
        return value
    else:
        return value[-bit:]

def appendStack(val):
    for i in range(0, len(val), 2):
        stack.append(value[i:i+2])

def negHex(num) :
    m = dict.fromkeys(range(16), 0); 
    digit = ord('0'); 
    c = ord('a'); 
    for i in range(16) :
        if (i < 10) :
            m[i] = chr(digit)
            digit += 1
        else :
            m[i] = chr(c)
            c += 1

    res = ""
    if (not num) :
        return "0"
    if (num > 0) :
        while (num) :
            res = m[num % 16] + res
            num //= 16
    else : 
        n = num + 2**32  
        while (n) :
            res = m[n % 16] + res 
            n //= 16
    return res  

def dec(number, base):
    result = 0
    power = len(number) - 1
    for i in number:
        try:
            result += int(i) * (base**power)
        except:
            if (i == 'a'):
                result += 10 * (base**power)
            elif (i == 'b'):
                result += 11 * (base**power)
            elif (i == 'c'):
                result += 12 * (base**power)
            elif (i == 'd'):
                result += 13 * (base**power)
            elif (i == 'e'):
                result += 14 * (base**power)
            elif (i == 'f'):
                result += 15 * (base**power)
        power -= 1
    return result

def whatBit(inp):
    if (isReg(inp)):
        for reg in registers:
            if (reg == inp):
                return 4
            elif (reg[1:] == inp):
                return 2
            elif (reg[1] + 'h' == inp or reg[1] + 'l' == inp):
                return 1
    elif (isData(inp)):
      Type = typeFinder(inp)
      if (Type == 'dword' or Type == 'sdword'):
        return 4
      elif (Type == 'word' or Type == 'sword'):
        return 2
      elif (Type == 'byte' or Type == 'sbyte'):
        return 1
    else:
        return 4

def whatTheFuckIsThis(inp):
    valueRes = ""
    try:
        valueRes = str(negHex(int(inp)))
    except:
        if (inp[-1] == 'o'):
            valueRes = str(negHex(dec((inp[:-1]), 8)))
        elif (inp[-1] == 'b'):
            valueRes = str(negHex(dec((inp[:-1]), 2)))
        elif (inp[-1] == 'h'):
            valueRes = str(negHex(dec((inp[:-1]), 16)))
    return valueRes

def isDec(number):
    if (number[-1] == 'b' or number[-1] == 'o' or number[-1] == 'h'):
        return False
    return True

def isEven(register):
    count = 0
    for bit in register:
        if (bit == '1'):
            count += 1
    if (count % 2 == 0):
        return True
    return False

def isNeg(register):
    negBits = ['7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    if (register[0] in negBits):
        return True
    return False

def isZero(register):
    for bit in register:
        if (bit != '0'):
            return False
    return True

def setAxFlag(num1, num2):
    num1 = dec(num1, 16)
    num2 = dec(num2, 16)
    carry = 0
    count = 0
    carries = ""
    while num1 > 0 or num2 > 0:
        sum = num1 % 2 + num2 % 2 + carry
        if sum >= 2:
            carry = 1
            count += 1
        else:
            carry = 0
        num1 = num1 // 10
        num2 = num2 // 10
        carries += str(carry)
    try:        
        if (carries[2] == 1):
            flags['af'] = True
        flags['af'] = False
    except:
        return False

def setCF_OF(value, size):
    is_neg = isNeg(value)
    value = dec(value, 16)
    flags['cf'] = value - 2**size == 0 or is_neg
    flags['of'] = value - 2**(size-1) == 0 or value + 2**(size-1) == -1

def setFlags(value):
    flags['sf'] = isNeg(value)
    flags['zf'] = isZero(value)
    flags['pf'] = isEven(value)
    
def printReg():
    print("Registers: ")
    print("32 bit:")
    for register in registers:
        print(f"{register} = {registers[register]}")
    
    print("16 bit:")
    for register in registers:
        print(f"{register[1:]} = {registers[register][4:]}")

    print("8 bit(l):")
    for register in registers:
        if (register[1:] in ['ax', 'bx', 'cx', 'dx']):
            print(f"{register[1] + 'l'} = {registers[register][4:][2:]}")
    
    print("8 bit(h):")
    for register in registers:
        if (register[1:] in ['ax', 'bx', 'cx', 'dx']):
            print(f"{register[1] + 'h'} = {registers[register][4:][:2]}")
    
    print("-------------------------------------")

def printFlags():
    print("Flags: ")
    for flag in flags:
        print(f"{flag} = {flags[flag]}")
    print("-------------------------------------")

def printData():
    print("Datas: ")
    for data in datas:
        print("name:", data.name, "\t type:", data.type, "\t value:", data.value)
    print("-------------------------------------")
        
def printStack():
    print("Stack: ")
    for i in range(len(stack) - 1, -1, -1):
        print(stack[i])
    print("-------------------------------------")

def printError(text, line):
    print(colored(f"\n########\nERROR:\n{text} -> in line {line} of code segment\n########\n", "red"))

registers = {
    'eax': "00000000",
    'ebx': "00000000",
    'ecx': "00000000",
    'edx': "00000000",
    'esi': "00000000",
    'edi': "00000000",
    'eip': "00000000",
    'esp': "00000000",
    'ebp': "00000000",
}

flags = {
    "of": False,
    "sf": False,
    "zf": False,
    "af": False,
    "pf": False,
    "cf": False
}

datas = []
codes = []
labels = []
stack = []

lines = []
while(True):
    print("1. Terminal")
    print("2. File")
    selection = input()
    if (selection == '1'):
        inp = input()
        while (inp != 'end'):
            lines.append(inp)
            inp = input()
        break
    elif (selection == '2'):
        # inp = input('Enter full path of the file: ')
        file = open("C:\\Users\\acer\\Desktop\\asm\\inp.txt", "r")
        # file = open(inp, "r")
        lines = file.readlines()
        break
    else:
        print("Enter a valid input")
        continue

dataFlag = False
codeFlag = False
lblAddress = -1
for i in lines:
    asmCode = i.lower().strip()
    if (len(asmCode.split()) == 0):
        continue
    if (asmCode == ".data"):
        dataFlag = True
        continue
    elif (asmCode == ".code"):
        codeFlag = True
        dataFlag = False
        continue
    if (dataFlag):
        dataCodeSplit = asmCode.split()
        data = Data()
        codeLength = len(dataCodeSplit)
        if (codeLength == 3):
            if (len(dataCodeSplit[2].split(',')) <= 1):                
                data.name = dataCodeSplit[0]
                data.type = dataCodeSplit[1]
                data.value = dataCodeSplit[2]
            else:
                data.name = dataCodeSplit[0]
                data.type = dataCodeSplit[1]
                data.value = dataCodeSplit[2].split(',')
        elif (codeLength == 2):
            data.name = ""
            data.type = dataCodeSplit[0]
            data.value = dataCodeSplit[1]
        elif (codeLength >= 4):
            data.name = dataCodeSplit[0]
            data.type = dataCodeSplit[1]
            array = []
            for i in range(2, codeLength):
                array.append(dataCodeSplit[i][:-1]) if dataCodeSplit[i][-1] == ',' else array.append(dataCodeSplit[i])
            data.value = array
        datas.append(data)
    elif (codeFlag):
        code = Code()
        code.inputs = []
        dataCodeSplit = asmCode.split()
        code.instruction = dataCodeSplit[0]
        for i in range(1, len(dataCodeSplit)):
            code.inputs.append(dataCodeSplit[i])
        codes.append(code)
        lblAddress += 1
    elif (not codeFlag and not dataFlag):
        code = Code()
        code.inputs = []
        dataCodeSplit = asmCode.split()
        code.instruction = dataCodeSplit[0]
        for i in range(1, len(dataCodeSplit)):
            code.inputs.append(dataCodeSplit[i])
        codes.append(code)
        lblAddress += 1
    if (asmCode[-1] == ":"):
        label = Label()
        label.name = asmCode[:-1]
        label.address = lblAddress
        labels.append(label)

address = 0
while (address != len(codes)):
    if (codes[address].instruction == "print_reg"):
        printReg()
    elif (codes[address].instruction == "print_flag"):
        printFlags()
    elif (codes[address].instruction == "show_stack"):
        printStack()
    elif (codes[address].instruction == "show_data"):
        printData()
    elif (codes[address].instruction == "mov"):
        Inputs = " ".join(codes[address].inputs)
        inputs = Inputs.split(',')
        inputs = [input.strip() for input in inputs]
        destination = inputs[0]
        source = inputs[1]
        for register in registers:
            if (register == destination):
                if (not isReg(source) and not isData(source)):
                    value = whatTheFuckIsThis(source)
                    value = sizeFixer(value, 8, 0)
                    registers[register] = value
                    break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg == source):
                            registers[register] = registers[reg]
                            break
                elif (isData(source)):
                    result = valueFinder(source, "dword")
                    value = whatTheFuckIsThis(result)
                    value = sizeFixer(value, 8, 0)
                    registers[register] = value
                    break
            elif (register[1:] == destination):
                if (not isReg(source) and not isData(source)):
                    value = whatTheFuckIsThis(source)
                    value = sizeFixer(value, 4, 0)
                    newVal = registers[register][:4] + value
                    registers[register] = newVal
                    break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1:] == source):
                            value = registers[register][:4] + registers[reg][4:]
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "word")
                    value = whatTheFuckIsThis(result)
                    value = sizeFixer(value, 4, 0)
                    newVal = registers[register][:4] + value
                    registers[register] = newVal
                    break
            elif (register[1] + 'l' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    value = whatTheFuckIsThis(source)
                    value = sizeFixer(value, 2, 0)
                    newVal = registers[register][:6] + value
                    registers[register] = newVal
                    break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'l' == source and reg[2] == 'x'):
                            value = registers[register][:6] + registers[reg][6:]
                            registers[register] = value
                            break
                        elif (reg[1] + 'h' == source and reg[2] == 'x'):
                            value = registers[register][:6] + registers[reg][4:6]
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    value = whatTheFuckIsThis(result)
                    value = sizeFixer(value, 2, 0)
                    newVal = registers[register][:6] + value
                    registers[register] = newVal
                    break
            elif (register[1] + 'h' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    value = whatTheFuckIsThis(source)
                    value = sizeFixer(value, 2, 0)
                    newVal = registers[register][:4] + value + registers[register][6:]
                    registers[register] = newVal
                    break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'h' == source and reg[2] == 'x'):
                            value = registers[register][:4] + registers[reg][4:6] + registers[register][6:]
                            registers[register] = value
                            break
                        elif (reg[1] + 'l' == source and reg[2] == 'x'):
                            value = registers[register][:4] + registers[reg][6:] + registers[register][6:]
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    value = whatTheFuckIsThis(result)
                    value = sizeFixer(value, 2, 0)
                    newVal = registers[register][:4] + value + registers[register][6:]
                    registers[register] = newVal
                    break 
            elif (isData(destination)):
                if (not isReg(source) and not isData(source)):
                    for data in datas:
                        if (data.name == destination):
                            data.value = source
                            break
                elif (isReg(source)):
                    for data in datas:
                        if (data.name == destination):
                            data.value = str(negHex(dec(registers[source], 16))) + 'h'
                            break
                else:
                    printError("invalid instruction operands", address + 1)
                    break
    elif (codes[address].instruction == "add"):
        Inputs = " ".join(codes[address].inputs)
        inputs = Inputs.split(',')
        inputs = [input.strip() for input in inputs]
        destination = inputs[0]
        source = inputs[1]
        for register in registers:
            if (register == destination):
                if (not isReg(source) and not isData(source)):
                    value = whatTheFuckIsThis(source)
                    value = str(hex(dec(registers[register], 16) + dec(value, 16)))[2:]
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 32)
                    value = sizeFixer(value, 8, 0)
                    registers[register] = value
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg == source):
                            value = str(hex(dec(registers[register], 16) + dec(registers[reg], 16)))[2:]
                            setAxFlag(registers[register], value)
                            setCF_OF(value, 32)
                            value = sizeFixer(value, 8, 0)
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "dword")
                    value = whatTheFuckIsThis(result)
                    value = str(hex(dec(registers[register], 16) + dec(value, 16)))[2:]
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 32)
                    value = sizeFixer(value, 8, 0)
                    registers[register] = value
                    # break
                setFlags(registers[register])
                break
            elif (register[1:] == destination):
                if (not isReg(source) and not isData(source)):
                    value = whatTheFuckIsThis(source)
                    value = str(hex(dec(registers[register][4:], 16) + dec(value, 16)))[2:]
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 16)
                    value = sizeFixer(value, 4, 0)
                    newVal = registers[register][:4] + value
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1:] == source):
                            value = str(hex(dec(registers[register][4:], 16) + dec(registers[reg][4:], 16)))[2:]
                            setAxFlag(registers[register], value)
                            setCF_OF(value, 16)
                            value = sizeFixer(value, 4, 0)
                            newVal = registers[register][:4] + value
                            registers[register] = newVal
                            break
                elif (isData(source)):
                    result = valueFinder(source, "word")
                    value = whatTheFuckIsThis(result)
                    value = str(hex(dec(registers[register][4:], 16) + dec(value, 16)))[2:]
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 16)
                    value = sizeFixer(value, 4, 0)
                    newVal = registers[register][:4] + value
                    registers[register] = newVal
                    # break
                setFlags(registers[register][1:])
                break
            elif (register[1] + 'l' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    value = whatTheFuckIsThis(source)
                    value = str(hex(dec(registers[register][6:], 16) + dec(value, 16)))[2:]
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 8)
                    value = sizeFixer(value, 2, 0)
                    newVal = registers[register][:6] + value
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'l' == source and reg[2] == 'x'):
                            value = str(hex(dec(registers[register][6:], 16) + dec(registers[reg][6:], 16)))[2:]
                            setAxFlag(registers[register], value)
                            setCF_OF(value, 8)
                            value = sizeFixer(value, 2, 0)
                            newVal = registers[register][:6] + value
                            registers[register] = newVal
                            break
                        elif (reg[1] + 'h' == source and reg[2] == 'x'):
                            value = str(hex(dec(registers[register][6:], 16) + dec(registers[reg][4:6], 16)))[2:]
                            setAxFlag(registers[register], value)
                            setCF_OF(value, 8)
                            value = sizeFixer(value, 2, 0)
                            newVal = registers[register][:6] + value
                            registers[register] = newVal
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    value = whatTheFuckIsThis(result)
                    value = str(hex(dec(registers[register][6:], 16) + dec(value, 16)))[2:]
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 8)
                    value = sizeFixer(value, 2, 0)
                    newVal = registers[register][:6] + value
                    registers[register] = newVal
                    # break
                setFlags(registers[register][6:])
                break
            elif (register[1] + 'h' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    value = whatTheFuckIsThis(source)
                    value = str(hex(dec(registers[register][4:6], 16) + dec(value, 16)))[2:]
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 8)
                    value = sizeFixer(value, 2, 0)
                    newVal = registers[register][:4] + value + registers[register][6:]
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'h' == source and reg[2] == 'x'):
                            value = str(hex(dec(registers[register][4:6], 16) + dec(registers[reg][4:6], 16)))[2:]
                            setAxFlag(registers[register], value)
                            setCF_OF(value, 8)
                            value = sizeFixer(value, 2, 0)
                            value = registers[register][:4] + value + registers[register][6:]
                            registers[register] = value
                            break
                        elif (reg[1] + 'l' == source and reg[2] == 'x'):
                            value = str(hex(dec(registers[register][4:6], 16) + dec(registers[reg][6:], 16)))[2:]
                            setAxFlag(registers[register], value)
                            setCF_OF(value, 8)
                            value = sizeFixer(value, 2, 0)
                            value = registers[register][:4] + value + registers[register][6:]
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    value = whatTheFuckIsThis(result)
                    value = str(hex(dec(registers[register][4:6], 16) + dec(value, 16)))[2:]
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 8)
                    value = sizeFixer(value, 2, 0)
                    newVal = registers[register][:4] + value + registers[register][6:]
                    registers[register] = newVal
                    # break
                setFlags(registers[register][4:6])
                break
            elif (isData(destination)):
                if (not isReg(source) and not isData(source)):
                    valueS = whatTheFuckIsThis(source)
                    for data in datas:
                        if (data.name == destination):
                            valueD = whatTheFuckIsThis(data.name)
                            data.value = str(hex(dec(valueD, 16) + dec(valueS, 16)))
                            break
                elif (isReg(source)):
                    for data in datas:
                        if (data.name == destination):
                            data.value = str(negHex(dec(valueS, 16) + dec(registers[source], 16)))
                            break
                else:
                    printError("invalid instruction operands", address + 1)
                    break   
    elif (codes[address].instruction == "sub"):
        Inputs = " ".join(codes[address].inputs)
        inputs = Inputs.split(',')
        inputs = [input.strip() for input in inputs]
        destination = inputs[0]
        source = inputs[1]
        for register in registers:
            if (register == destination):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 32)
                    value = sizeFixer(value, 8, 0)
                    registers[register] = value
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg == source):
                            value = str(negHex(dec(registers[register], 16) - dec(registers[reg], 16)))
                            setAxFlag(registers[register], value)
                            setCF_OF(value, 32)
                            value = sizeFixer(value, 8, 0)
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "dword")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 32)
                    value = sizeFixer(value, 8, 0)
                    registers[register] = value
                    # break
                setFlags(registers[register])
                break
            elif (register[1:] == destination):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register][4:], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 16)
                    value = sizeFixer(value, 4, 0)
                    newVal = registers[register][:4] + value
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1:] == source):
                            value = str(negHex(dec(registers[register][4:], 16) - dec(registers[reg][4:], 16)))
                            setAxFlag(registers[register], value)
                            setCF_OF(value, 16)
                            value = sizeFixer(value, 4, 0)
                            newVal = registers[register][:4] + value
                            registers[register] = newVal
                            break
                elif (isData(source)):
                    result = valueFinder(source, "word")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register][4:], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 16)
                    value = sizeFixer(value, 4, 0)
                    newVal = registers[register][:4] + value
                    registers[register] = newVal
                    # break
                setFlags(registers[register][1:])
                break
            elif (register[1] + 'l' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register][6:], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 8)
                    value = sizeFixer(value, 2, 0)
                    newVal = registers[register][:6] + value
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'l' == source and reg[2] == 'x'):
                            value = str(negHex(dec(registers[register][6:], 16) - dec(registers[reg][6:], 16)))
                            setAxFlag(registers[register], value)
                            setCF_OF(value, 8)
                            value = sizeFixer(value, 2, 0)
                            newVal = registers[register][:6] + value
                            registers[register] = newVal
                            break
                        elif (reg[1] + 'h' == source and reg[2] == 'x'):
                            value = str(negHex(dec(registers[register][6:], 16) - dec(registers[reg][4:6], 16)))
                            setAxFlag(registers[register], value)
                            setCF_OF(value, 8)
                            value = sizeFixer(value, 2, 0)
                            newVal = registers[register][:6] + value
                            registers[register] = newVal
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register][6:], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 8)
                    value = sizeFixer(value, 2, 0)
                    newVal = registers[register][:6] + value
                    registers[register] = newVal
                    # break
                setFlags(registers[register][6:])
                break
            elif (register[1] + 'h' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register][4:6], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 8)
                    value = sizeFixer(value, 2, 0)
                    newVal = registers[register][:4] + value + registers[register][6:]
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'h' == source and reg[2] == 'x'):
                            value = str(negHex(dec(registers[register][4:6], 16) - dec(registers[reg][4:6], 16)))
                            setAxFlag(registers[register], value)
                            setCF_OF(value, 8)
                            value = sizeFixer(value, 2, 0)
                            value = registers[register][:4] + value + registers[register][6:]
                            registers[register] = value
                            break
                        elif (reg[1] + 'l' == source and reg[2] == 'x'):
                            value = str(negHex(dec(registers[register][4:6], 16) - dec(registers[reg][6:], 16)))
                            setAxFlag(registers[register], value)
                            setCF_OF(value, 8)
                            value = sizeFixer(value, 2, 0)
                            value = registers[register][:4] + value + registers[register][6:]
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register][4:6], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    setCF_OF(value, 8)
                    value = sizeFixer(value, 2, 0)
                    newVal = registers[register][:4] + value + registers[register][6:]
                    registers[register] = newVal
                    # break
                setFlags(registers[register][4:6])
                break
            elif (isData(destination)):
                if (not isReg(source) and not isData(source)):
                    valueS = whatTheFuckIsThis(source)
                    for data in datas:
                        if (data.name == destination):
                            valueD = whatTheFuckIsThis(data.name)
                            value = str(negHex(dec(valueD, 16) - dec(valueS, 16)))    
                            setAxFlag(valueD, valueS)
                            setCF_OF(value, 32)
                            data.value = value
                            break
                elif (isReg(source)):
                    for data in datas:
                        if (data.name == destination):
                            value = str(negHex(dec(valueS) - dec(registers[source], 16)))
                            setAxFlag(registers[register], value)
                            setCF_OF(value, 32)
                            data.value = value
                            break
                else:
                    printError("invalid instruction operands", address + 1)
                    break
                setFlags(destination)
    elif (codes[address].instruction == "movsx"):
        Inputs = " ".join(codes[address].inputs)
        inputs = Inputs.split(',')
        inputs = [input.strip() for input in inputs]
        destination = inputs[0]
        source = inputs[1]
        for register in registers:
            if (register == destination):
                if (not isReg(source) and not isData(source)):
                    printError("invalid instrucion operands", address + 1)
                    break
                elif (isReg(source)):
                    bit = whatBit(source)
                    print(bit, "movsx") 
                    if (bit != 4):
                        for reg in registers:
                            if (reg[1:] == source):
                                if (isNeg(registers[reg])):
                                    registers[register] = sizeFixer(registers[reg], 8, 'f')
                                    break
                                elif (not isNeg(registers[reg])):
                                    registers[register] = sizeFixer(registers[reg], 8, 0)
                                    break
                            elif (reg[1] + 'l' == source and reg[2] == 'x'):
                                if (isNeg(registers[reg][6:])):
                                    registers[register] = sizeFixer(registers[reg][6:], 8, 'f')
                                    break
                                elif (not isNeg(registers[reg][6:])):
                                    registers[register] = sizeFixer(registers[reg][6:], 8, 0)
                                    break
                            elif (reg[1] + 'h' == source and reg[2] == 'x'):
                                if (isNeg(registers[reg][4:6])):
                                    registers[register] = sizeFixer(registers[reg][4:6], 8, 'f')
                                    break
                                elif (not isNeg(registers[reg][4:6])):
                                    registers[register] = sizeFixer(registers[reg][4:6], 8, 0)
                                    break
                    else:
                        printError("invalid instrucion operands", address + 1)
                        break
                elif (isData(source)):
                    bit = whatBit(source)
                    if (bit != 4):
                        result = valueFinder(source, "byte") or valueFinder(source, "word")
                        try:
                            value = str(hex(int(result)))[2:]
                        except:
                            if (result[-1] == 'o'):
                                value = str(hex(dec((result[:-1]), 8)))[2:]
                            elif (result[-1] == 'b'):
                                value = str(hex(dec((result[:-1]), 2)))[2:]
                            elif (result[-1] == 'h'):
                                value = str(hex(dec((result[:-1]), 16)))[2:]
                        if (isNeg(value)):
                            value = sizeFixer(value, 8, 'f')
                        elif (not isNeg(value)):
                            value = sizeFixer(value, 8, 0)
                        registers[register] = value
                        break
                    else:
                        printError("invalid instrucion operands", address + 1)
                        break
            elif (register[1:] == destination):
                if (not isReg(source) and not isData(source)):
                    printError("invalid instrucion operands", address + 1)
                    break
                elif (isReg(source)):
                    bit = whatBit(source)
                    if (bit == 1):
                        for reg in registers:
                            if (reg[1] + 'l' == source and reg[2] == 'x'):
                                if (isNeg(registers[reg][6:])):
                                    value = sizeFixer(registers[reg][6:], 4, 'f')
                                    registers[register] = registers[register][:4] + value
                                    break
                                elif (not isNeg(registers[reg][6:])):
                                    value = sizeFixer(registers[reg][6:], 4, 0)
                                    registers[register] = registers[register][:4] + value
                                    break
                            elif (reg[1] + 'h' == source and reg[2] == 'x'):
                                if (isNeg(registers[reg][4:6])):
                                    value = sizeFixer(registers[reg][4:6], 4, 'f')
                                    registers[register] = registers[register][:4] + value
                                    break
                                elif (not isNeg(registers[reg][4:6])):
                                    value = sizeFixer(registers[reg][4:6], 4, 0)
                                    registers[register] = registers[register][:4] + value
                                    break
                    else:
                        printError("invalid instrucion operands", address + 1)
                        break
                elif (isData(source)):
                    bit = whatBit(source)
                    if (bit == 1):
                        result = valueFinder(source, "byte")
                        try:
                            value = str(hex(int(result)))[2:]
                        except:
                            if (result[-1] == 'o'):
                                value = str(hex(dec((result[:-1]), 8)))[2:]
                            elif (result[-1] == 'b'):
                                value = str(hex(dec((result[:-1]), 2)))[2:]
                            elif (result[-1] == 'h'):
                                value = str(hex(dec((result[:-1]), 16)))[2:]
                        if (isNeg(value)):
                            value = sizeFixer(value, 4, 'f')
                        elif (not isNeg(value)):
                            value = sizeFixer(value, 4, 0)
                        registers[register] = registers[register][:4] + value
                        break
                    else:
                        printError("invalid instrucion operands", address + 1)
                        break  
            elif (register[1] + 'l' == destination and register[2] == 'x' or register[1] + 'h' == destination and register[2] == 'x'):
                printError("byte register cannot be first operand", address + 1)
                break
            elif (isData(destination)):
                printError("memory operand not allowed in context", address + 1)
                break
    elif (codes[address].instruction == "movzx"):
        Inputs = " ".join(codes[address].inputs)
        inputs = Inputs.split(',')
        inputs = [input.strip() for input in inputs]
        destination = inputs[0]
        source = inputs[1]
        for register in registers:
            if (register == destination):
                if (not isReg(source) and not isData(source)):
                    printError("invalid instrucion operands", address + 1)
                    break
                elif (isReg(source)):
                    bit = whatBit(source)
                    if (bit != 4):
                        for reg in registers:
                            if (reg[1:] == source):
                                registers[register] = sizeFixer(registers[reg], 8, 0)
                                break
                            elif (reg[1] + 'l' == source and reg[2] == 'x'):
                                registers[register] = sizeFixer(registers[reg][6:], 8, 0)
                                break
                            elif (reg[1] + 'h' == source and reg[2] == 'x'):
                                registers[register] = sizeFixer(registers[reg][4:6], 8, 0)
                                break
                    else:
                        printError("invalid instrucion operands", address + 1)
                        break
                elif (isData(source)):
                    bit = whatBit(source)
                    if (bit != 4):
                        result = valueFinder(source, "byte") or valueFinder(source, "word")
                        try:
                            value = str(hex(int(result)))[2:]
                        except:
                            if (result[-1] == 'o'):
                                value = str(hex(dec((result[:-1]), 8)))[2:]
                            elif (result[-1] == 'b'):
                                value = str(hex(dec((result[:-1]), 2)))[2:]
                            elif (result[-1] == 'h'):
                                value = str(hex(dec((result[:-1]), 16)))[2:]
                        value = sizeFixer(value, 8, 0)
                        registers[register] = value
                        break
                    else:
                        printError("invalid instrucion operands", address + 1)
                        break
            elif (register[1:] == destination):
                if (not isReg(source) and not isData(source)):
                    printError("invalid instrucion operands", address + 1)
                    break
                elif (isReg(source)):
                    bit = whatBit(source)
                    if (bit == 1):
                        for reg in registers:
                            if (reg[1] + 'l' == source and reg[2] == 'x'):
                                value = sizeFixer(registers[reg][6:], 4, 0)
                                registers[register] = value
                                break
                            elif (reg[1] + 'h' == source and reg[2] == 'x'):
                                value = sizeFixer(registers[reg][4:6], 4, 0)
                                registers[register] = value
                                break
                    else:
                        printError("invalid instrucion operands", address + 1)
                        break
                elif (isData(source)):
                    bit = whatBit(source)
                    if (bit == 1):
                        result = valueFinder(source, "byte")
                        try:
                            value = str(hex(int(result)))[2:]
                        except:
                            if (result[-1] == 'o'):
                                value = str(hex(dec((result[:-1]), 8)))[2:]
                            elif (result[-1] == 'b'):
                                value = str(hex(dec((result[:-1]), 2)))[2:]
                            elif (result[-1] == 'h'):
                                value = str(hex(dec((result[:-1]), 16)))[2:]
                        value = sizeFixer(value, 4, 0)
                        registers[register] = registers[register][:4] + value
                        break
                    else:
                        printError("invalid instrucion operands", address + 1)
                        break 
            elif (register[1] + 'l' == destination and register[2] == 'x' or register[1] + 'h' == destination and register[2] == 'x'):
                printError("byte register cannot be first operand", address + 1)
                break
            elif (isData(destination)):
                printError("memory operand not allowed in context", address + 1)
                break
    elif (codes[address].instruction == "xchg"):
        Inputs = " ".join(codes[address].inputs)
        inputs = Inputs.split(',')
        inputs = [input.strip() for input in inputs]
        destination = inputs[0]
        source = inputs[1]
        for register in registers:
            if (register == destination):
                if (isReg(source)):
                    for reg in registers:
                        if (reg == source):
                            registers[register], registers[reg] = registers[reg], registers[register]
                            break
                elif (isData(source)):
                    result = valueFinder(source, "dword")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 8, 0)
                    for data in datas:
                        if (data.value == result):
                            data.value = registers[register] + "h"
                            break
                    registers[register] = value
                    break
            elif (register[1:] == destination):
                if (isReg(source)):
                    for reg in registers:
                        if (reg[1:] == source):
                            temp = registers[register]
                            value = registers[register][:4] + registers[reg][4:]
                            registers[reg] = registers[reg][:4] + temp[4:]
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "word")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 4, 0)
                    for data in datas:
                        if (data.value == result):
                            data.value = registers[register][4:] + "h"
                            break
                    newVal = registers[register][:4] + value
                    registers[register] = newVal
                    break
            elif (register[1] + 'l' == destination and register[2] == 'x'):
                if (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'l' == source and reg[2] == 'x'):
                            temp = registers[register]
                            value = registers[register][:6] + registers[reg][6:]
                            registers[reg] = registers[reg][:6] + temp[6:]
                            registers[register] = value
                            break
                        elif (reg[1] + 'h' == source and reg[2] == 'x'):
                            temp = registers[register]
                            value = registers[register][:6] + registers[reg][4:6]
                            registers[reg] = registers[reg][:4] + temp[6:] + registers[reg][6:]
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    for data in datas:
                        if (data.value == result):
                            data.value = registers[register][6:] + "h"
                            break
                    newVal = registers[register][:6] + value
                    registers[register] = newVal
                    break
            elif (register[1] + 'h' == destination and register[2] == 'x'):
                if (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'h' == source and reg[2] == 'x'):
                            temp = registers[register]
                            value = registers[register][:4] + registers[reg][4:6] + registers[register][6:]
                            registers[reg] = registers[reg][:4] + temp[4:6] + registers[reg][6:]
                            registers[register] = value
                            break
                        elif (reg[1] + 'l' == source and reg[2] == 'x'):
                            temp = registers[register]
                            value = registers[register][:4] + registers[reg][6:] + registers[register][6:]
                            registers[reg] = registers[reg][:6] + temp[4:6]
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    for data in datas:
                        if (data.value == result):
                            data.value = registers[register][6:] + "h"
                            break
                    newVal = registers[register][:4] + value + registers[register][6:]
                    registers[register] = newVal
                    break
            elif (isData(destination)):
                valueD = whatTheFuckIsThis(valueFinder(destination, "byte") | valueFinder(destination, "word") | valueFinder(destination, "dword"))
                if (isReg(source)):
                    temp = str(negHex(dec(registers[source], 16)))
                    registers[source] = sizeFixer(valueD, whatBit(registers[source]) * 2, 0)
                    for data in datas:
                        if (data.name == destination):
                            data.value = temp
                            break
                else:
                    printError("invalid instruction operands", address + 1)
    elif (codes[address].instruction == "or"):
        Inputs = " ".join(codes[address].inputs)
        inputs = Inputs.split(',')
        inputs = [input.strip() for input in inputs]
        destination = inputs[0]
        source = inputs[1]
        for register in registers:
            if (register == destination):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = sizeFixer(value, 8, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register]), 16)
                    result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                    registers[register] = sizeFixer(result[2:], 8, 0)
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg == source):
                            inp1 = dec(registers[reg], 16)
                            inp2 = dec(registers[register], 16)
                            result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                            registers[register] = sizeFixer(result[2:], 8, 0)
                            break
                elif (isData(source)):
                    result = valueFinder(source, "dword") or valueFinder(source, "word") or valueFinder(source, "byte")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 8, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register]), 16)
                    result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                    registers[register] = sizeFixer(result[2:], 8, 0)
                    # break
                setFlags(registers[register])
                break
            elif (register[1:] == destination):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = sizeFixer(value, 4, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register]), 16)
                    result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                    newVal = registers[register][:4] + sizeFixer(result[2:0], 4, 0)
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1:] == source):
                            inp1 = dec((registers[reg][4:]), 16)
                            inp2 = dec((registers[register][4:]), 16)
                            result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                            value = registers[register][:4] + sizeFixer(result[2:0], 4, 0)
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "word")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 4, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register]), 16)
                    result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                    newVal = registers[register][:4] + sizeFixer(result[2:0], 4, 0)
                    registers[register] = newVal
                    # break
                setFlags(registers[register][1:])
                break
            elif (register[1] + 'l' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register][6:]), 16)
                    result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                    newVal = registers[register][:6] + sizeFixer(result[2:0], 2, 0)
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'l' == source and reg[2] == 'x'):
                            inp1 = dec((registers[reg][6:]), 16)
                            inp2 = dec((registers[register][6:]), 16)
                            result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                            value = registers[register][:6] + sizeFixer(result[2:], 2, 0)
                            registers[register] = value
                            break
                        elif (reg[1] + 'h' == source and reg[2] == 'x'):
                            inp1 = dec((registers[reg][4:6]), 16)
                            inp2 = dec((registers[register][6:]), 16)
                            result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                            value = registers[register][:6] + sizeFixer(result[2:], 2, 0)
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register][6:]), 16)
                    result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                    newVal = registers[register][:6] + sizeFixer(result[2:0], 2, 0)
                    registers[register] = newVal
                    # break
                setFlags(registers[register][6:])
                break
            elif (register[1] + 'h' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register][4:6]), 16)
                    result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                    newVal = registers[register][:4] + sizeFixer(result, 2, 0) + registers[register][6:]
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'h' == source and reg[2] == 'x'):
                            inp1 = dec((registers[reg][4:6]), 16)
                            inp2 = dec((registers[register][4:6]), 16)
                            result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                            value = registers[register][:4] + sizeFixer(result, 2, 0) + registers[register][6:]
                            registers[register] = value
                            break
                        elif (reg[1] + 'l' == source and reg[2] == 'x'):
                            inp1 = dec((registers[reg][6:]), 16)
                            inp2 = dec((registers[register][4:6]), 16)
                            result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                            value = registers[register][:4] + sizeFixer(result, 2, 0) + registers[register][6:]
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register][4:6]), 16)
                    result = hex(dec(str(bin(inp1 | inp2))[2:], 2))
                    newVal = registers[register][:4] + sizeFixer(result, 2, 0) + registers[register][6:]
                    registers[register] = newVal
                    # break
                setFlags(registers[register][4:6])
                break
            elif (isData(destination)):
                if (not isReg(source) and not isData(source)):
                    valueS = whatTheFuckIsThis(source)
                    for data in datas:
                        if (data.name == destination):
                            valueD = whatTheFuckIsThis(data.name)
                            data.value = str(hex(dec(valueD, 16) | dec(valueS, 16)))
                            break
                elif (isReg(source)):
                    for data in datas:
                        if (data.name == destination):
                            data.value = str(negHex(dec(valueS) | dec(registers[source], 16)))
                            break
                else:
                    printError("invalid instruction operands", address + 1)
                    break   
    elif (codes[address].instruction == "and"):
        Inputs = " ".join(codes[address].inputs)
        inputs = Inputs.split(',')
        inputs = [input.strip() for input in inputs]
        destination = inputs[0]
        source = inputs[1]
        for register in registers:
            if (register == destination):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = sizeFixer(value, 8, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register]), 16)
                    result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                    registers[register] = sizeFixer(result[2:], 8, 0)
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg == source):
                            inp1 = dec(registers[reg], 16)
                            inp2 = dec(registers[register], 16)
                            result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                            registers[register] = sizeFixer(result[2:], 8, 0)
                            break
                elif (isData(source)):
                    result = valueFinder(source, "dword") or valueFinder(source, "word") or valueFinder(source, "byte")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 8, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register]), 16)
                    result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                    registers[register] = sizeFixer(result[2:], 8, 0)
                    # break
                setFlags(registers[register])
                break
            elif (register[1:] == destination):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = sizeFixer(value, 4, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register]), 16)
                    result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                    newVal = registers[register][:4] + sizeFixer(result[2:0], 4, 0)
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1:] == source):
                            inp1 = dec((registers[reg][4:]), 16)
                            inp2 = dec((registers[register][4:]), 16)
                            result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                            value = registers[register][:4] + sizeFixer(result[2:0], 4, 0)
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "word")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 4, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register]), 16)
                    result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                    newVal = registers[register][:4] + sizeFixer(result[2:0], 4, 0)
                    registers[register] = newVal
                    # break
                setFlags(registers[register][1:])
                break
            elif (register[1] + 'l' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register][6:]), 16)
                    result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                    newVal = registers[register][:6] + sizeFixer(result[2:0], 2, 0)
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'l' == source and reg[2] == 'x'):
                            inp1 = dec((registers[reg][6:]), 16)
                            inp2 = dec((registers[register][6:]), 16)
                            result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                            value = registers[register][:6] + sizeFixer(result[2:], 2, 0)
                            registers[register] = value
                            break
                        elif (reg[1] + 'h' == source and reg[2] == 'x'):
                            inp1 = dec((registers[reg][4:6]), 16)
                            inp2 = dec((registers[register][6:]), 16)
                            result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                            value = registers[register][:6] + sizeFixer(result[2:], 2, 0)
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register][6:]), 16)
                    result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                    newVal = registers[register][:6] + sizeFixer(result[2:0], 2, 0)
                    registers[register] = newVal
                    # break
                setFlags(registers[register][6:])
                break
            elif (register[1] + 'h' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register][4:6]), 16)
                    result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                    newVal = registers[register][:4] + sizeFixer(result, 2, 0) + registers[register][6:]
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'h' == source and reg[2] == 'x'):
                            inp1 = dec((registers[reg][4:6]), 16)
                            inp2 = dec((registers[register][4:6]), 16)
                            result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                            value = registers[register][:4] + sizeFixer(result, 2, 0) + registers[register][6:]
                            registers[register] = value
                            break
                        elif (reg[1] + 'l' == source and reg[2] == 'x'):
                            inp1 = dec((registers[reg][6:]), 16)
                            inp2 = dec((registers[register][4:6]), 16)
                            result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                            value = registers[register][:4] + sizeFixer(result, 2, 0) + registers[register][6:]
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register][4:6]), 16)
                    result = hex(dec(str(bin(inp1 & inp2))[2:], 2))
                    newVal = registers[register][:4] + sizeFixer(result, 2, 0) + registers[register][6:]
                    registers[register] = newVal
                    # break
                setFlags(registers[register][4:6])
                break
            elif (isData(destination)):
                if (not isReg(source) and not isData(source)):
                    valueS = whatTheFuckIsThis(source)
                    for data in datas:
                        if (data.name == destination):
                            valueD = whatTheFuckIsThis(data.name)
                            data.value = str(hex(dec(valueD, 16) & dec(valueS, 16)))
                            break
                elif (isReg(source)):
                    for data in datas:
                        if (data.name == destination):
                            data.value = str(negHex(dec(valueS) & dec(registers[source], 16)))
                            break
                else:
                    printError("invalid instruction operands", address + 1)
                    break
    elif (codes[address].instruction == "xor"):
        Inputs = " ".join(codes[address].inputs)
        inputs = Inputs.split(',')
        inputs = [input.strip() for input in inputs]
        destination = inputs[0]
        source = inputs[1]
        for register in registers:
            if (register == destination):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = sizeFixer(value, 8, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register]), 16)
                    result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                    registers[register] = sizeFixer(result[2:], 8, 0)
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg == source):
                            inp1 = dec(registers[reg], 16)
                            inp2 = dec(registers[register], 16)
                            result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                            registers[register] = sizeFixer(result[2:], 8, 0)
                            break
                elif (isData(source)):
                    result = valueFinder(source, "dword") or valueFinder(source, "word") or valueFinder(source, "byte")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 8, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register]), 16)
                    result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                    registers[register] = sizeFixer(result[2:], 8, 0)
                    # break
                setFlags(registers[register])
                break
            elif (register[1:] == destination):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = sizeFixer(value, 4, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register]), 16)
                    result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                    newVal = registers[register][:4] + sizeFixer(result[2:0], 4, 0)
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1:] == source):
                            inp1 = dec((registers[reg][4:]), 16)
                            inp2 = dec((registers[register][4:]), 16)
                            result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                            value = registers[register][:4] + sizeFixer(result[2:0], 4, 0)
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "word")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 4, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register]), 16)
                    result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                    newVal = registers[register][:4] + sizeFixer(result[2:0], 4, 0)
                    registers[register] = newVal
                    # break
                setFlags(registers[register][1:])
                break
            elif (register[1] + 'l' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register][6:]), 16)
                    result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                    newVal = registers[register][:6] + sizeFixer(result[2:0], 2, 0)
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'l' == source and reg[2] == 'x'):
                            inp1 = dec((registers[reg][6:]), 16)
                            inp2 = dec((registers[register][6:]), 16)
                            result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                            value = registers[register][:6] + sizeFixer(result[2:], 2, 0)
                            registers[register] = value
                            break
                        elif (reg[1] + 'h' == source and reg[2] == 'x'):
                            inp1 = dec((registers[reg][4:6]), 16)
                            inp2 = dec((registers[register][6:]), 16)
                            result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                            value = registers[register][:6] + sizeFixer(result[2:], 2, 0)
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register][6:]), 16)
                    result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                    newVal = registers[register][:6] + sizeFixer(result[2:0], 2, 0)
                    registers[register] = newVal
                    # break
                setFlags(registers[register][6:])
                break
            elif (register[1] + 'h' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register][4:6]), 16)
                    result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                    newVal = registers[register][:4] + sizeFixer(result, 2, 0) + registers[register][6:]
                    registers[register] = newVal
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'h' == source and reg[2] == 'x'):
                            inp1 = dec((registers[reg][4:6]), 16)
                            inp2 = dec((registers[register][4:6]), 16)
                            result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                            value = registers[register][:4] + sizeFixer(result, 2, 0) + registers[register][6:]
                            registers[register] = value
                            break
                        elif (reg[1] + 'l' == source and reg[2] == 'x'):
                            inp1 = dec((registers[reg][6:]), 16)
                            inp2 = dec((registers[register][4:6]), 16)
                            result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                            value = registers[register][:4] + sizeFixer(result, 2, 0) + registers[register][6:]
                            registers[register] = value
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = sizeFixer(value, 2, 0)
                    inp1 = dec((value), 16)
                    inp2 = dec((registers[register][4:6]), 16)
                    result = hex(dec(str(bin(inp1 ^ inp2))[2:], 2))
                    newVal = registers[register][:4] + sizeFixer(result, 2, 0) + registers[register][6:]
                    registers[register] = newVal
                    # break
                setFlags(registers[register][4:6])
                break
            elif (isData(destination)):
                if (not isReg(source) and not isData(source)):
                    valueS = whatTheFuckIsThis(source)
                    for data in datas:
                        if (data.name == destination):
                            valueD = whatTheFuckIsThis(data.name)
                            data.value = str(hex(dec(valueD, 16) ^ dec(valueS, 16)))
                            break
                elif (isReg(source)):
                    for data in datas:
                        if (data.name == destination):
                            data.value = str(negHex(dec(valueS) ^ dec(registers[source], 16)))
                            break
                else:
                    printError("invalid instruction operands", address + 1)
                    break
    elif (codes[address].instruction == "inc"):
        inp = " ".join(codes[address].inputs)
        for register in registers:
            if (register == inp):
                setAxFlag(registers[register], "1")
                value = str(hex(dec(registers[register], 16) + 1))[2:]
                setCF_OF(value, 32)
                value = sizeFixer(value, 8, 0)
                registers[register] = value
                setFlags(registers[register])
                break
            elif (register[1:] == inp):
                setAxFlag(registers[register][4:], "1")
                value = str(hex(dec(registers[register][4:], 16) + 1))[2:]
                setCF_OF(value, 16)
                value = sizeFixer(value, 4, 0)
                registers[register] = registers[register][4:] + value
                setFlags(registers[register][4:])
                break
            elif (register[1] + 'l' == inp and register[2] == 'x'):
                setAxFlag(registers[register][6:], "1")
                value = str(hex(dec(registers[register][6:], 16) + 1))[2:]
                setCF_OF(value, 16)
                value = sizeFixer(value, 2, 0)
                registers[register] = registers[register][:6] + value
                setFlags(registers[register][6:])
                break
            elif (register[1] + 'h' == inp and register[2] == 'x'):
                setAxFlag(registers[register][4:6], "1")
                value = str(hex(dec(registers[register][4:6], 16) + 1))[2:]
                setCF_OF(value, 16)
                value = sizeFixer(value, 2, 0)
                registers[register] = registers[register][:4] + value + registers[register][6:]
                setFlags(registers[register][4:6])
                break
            elif (isData(inp)):
                result = valueFinder(inp, "byte") or valueFinder(inp, "word") or valueFinder(inp, "dword")
                setAxFlag(result, "-1")
                value = str(negHex(dec(whatTheFuckIsThis(result), 16) + 1))
                setCF_OF(value, 16)
                setFlags(value)
                for data in datas:
                    if (data.name == inp):
                        data.value = value
                        break
            elif (not isReg(inp) and not isData(inp)):
                printError("immediate operand not allowed", address + 1)
    elif (codes[address].instruction == "dec"):
        inp = " ".join(codes[address].inputs)
        for register in registers:
            if (register == inp):
                setAxFlag(registers[register], "1")
                value = str(negHex(dec(registers[register], 16) - 1))
                setCF_OF(value, 32)
                value = sizeFixer(value, 8, 0)
                registers[register] = value
                setFlags(registers[register])
                break
            elif (register[1:] == inp):
                setAxFlag(registers[register][4:], "1")
                value = str(negHex(dec(registers[register][4:], 16) - 1))
                setCF_OF(value, 16)
                value = sizeFixer(value, 4, 0)
                registers[register] = registers[register][4:] + value
                setFlags(registers[register][4:])
                break
            elif (register[1] + 'l' == inp and register[2] == 'x'):
                setAxFlag(registers[register][6:], "1")
                value = str(negHex(dec(registers[register][6:], 16) - 1))
                setCF_OF(value, 16)
                value = sizeFixer(value, 2, 0)
                registers[register] = registers[register][:6] + value
                setFlags(registers[register][6:])
                break
            elif (register[1] + 'h' == inp and register[2] == 'x'):
                setAxFlag(registers[register][4:6], "1")
                value = str(negHex(dec(registers[register][4:6], 16) - 1))
                setCF_OF(value, 16)
                value = sizeFixer(value, 2, 0)
                registers[register] = registers[register][:4] + value + registers[register][6:]
                setFlags(registers[register][4:6])
                break
            elif (isData(inp)):
                result = valueFinder(inp, "byte") or valueFinder(inp, "word") or valueFinder(inp, "dword")
                setAxFlag(result, "-1")
                value = str(negHex(dec(whatTheFuckIsThis(result), 16) - 1))
                setCF_OF(value, 16)
                setFlags(value)
                for data in datas:
                    if (data.name == inp):
                        data.value = value
                        break
            elif(not isReg(inp) and not isData(inp)):
                printError("immediate operand not allowed", address + 1)
                break
    elif (codes[address].instruction == "neg"):
        inp = " ".join(codes[address].inputs)
        for register in registers:
            if (register == inp):
                setAxFlag(registers[register], "1")
                value = str(negHex(-dec(registers[register], 16)))
                setCF_OF(value, 32)
                value = sizeFixer(value, 8, 0)
                registers[register] = value
                setFlags(registers[register])
                break
            elif (register[1:] == inp):
                setAxFlag(registers[register][4:], "1")
                value = str(negHex(-dec(registers[register][4:], 16)))
                setCF_OF(value, 16)
                value = sizeFixer(value, 4, 0)
                registers[register] = registers[register][4:] + value
                setFlags(registers[register][4:])
                break
            elif (register[1] + 'l' == inp and register[2] == 'x'):
                setAxFlag(registers[register][6:], "1")
                value = str(negHex(-dec(registers[register][6:], 16)))
                setCF_OF(value, 16)
                value = sizeFixer(value, 2, 0)
                registers[register] = registers[register][:6] + value
                setFlags(registers[register][6:])
                break
            elif (register[1] + 'h' == inp and register[2] == 'x'):
                setAxFlag(registers[register][4:6], "1")
                value = str(negHex(-dec(registers[register][4:6], 16)))
                setCF_OF(value, 16)
                value = sizeFixer(value, 2, 0)
                registers[register] = registers[register][:4] + value + registers[register][6:]
                setFlags(registers[register][4:6])
                break
            elif (isData(inp)):
                result = valueFinder(inp, "byte") or valueFinder(inp, "word") or valueFinder(inp, "dword")
                setAxFlag(result, "-1")
                value = str(negHex(-dec(whatTheFuckIsThis(result), 16)))
                setCF_OF(value, 16)
                setFlags(value)
                for data in datas:
                    if (data.name == inp):
                        data.value = value
                        break
            elif(not isReg(inp) and not isData(inp)):
                printError("immediate operand not allowed", address + 1)
                break
    elif (codes[address].instruction == "push"):
        Input = " ".join(codes[address].inputs)
        print(Input, "inp push")
        bit = whatBit(Input)
        errFlag = False
        if (isData(Input)):
            if (bit == 4):
                appendStack(sizeFixer(valueFinder(Input, "dword"), 8, 0))
            elif (bit == 2):
                appendStack(sizeFixer(valueFinder(Input, "word"), 4, 0))
        elif (isReg(Input)):
            if (bit == 4):
                for reg in registers:
                    if (reg == Input):
                        appendStack(registers[reg])
                        break
            elif (bit == 2):
                for reg in registers:
                    if (reg[1:] == Input):
                        stack.append(registers[reg])
                        break
            elif (bit == 1):
                printError("byte register cannot be first operand", address + 1)
                errFlag = True
        else:
            value = whatTheFuckIsThis(Input)
            if (len(value) < 2):
                value = sizeFixer(value, 2, 0)
            elif (len(value) < 4):
                value = sizeFixer(value, 4, 0)
            elif (len(value) < 8):
                value = sizeFixer(value, 8, 0)    
            appendStack(value)
        if (not errFlag):
            try:
                value = str(negHex(dec(registers['esp'], 16) - bit))
                value = sizeFixer(value, 8, 0)
                registers['esp'] = value
            except:
                print("error")
    elif (codes[address].instruction == "pop"):
        Input = " ".join(codes[address].inputs)
        if (len(stack) != 0):
            bit = whatBit(Input)
            if (isData(Input)):
                for data in datas:
                    if (data.name == Input):
                        if (data.type == "byte" or data.type == "sbyte"):
                            data.value = stack[-1]
                        elif (data.type == "word" or data.type == "sword"):
                            data.value = stack[-3:-1]
                        elif (data.type == "dword" or data.type == "sdword"):
                            data.value = stack[-5:-1]    
                        break
            elif (isReg(Input)):
                if (bit == 4):
                    for reg in registers:
                        if (reg == Input):
                            registers[reg] = stack[-5:-1]
                            stack.remove(stack[-5:-1])
                            break
                elif (bit == 2):
                    for reg in registers:
                        if (reg[1:] == Input):
                            registers[reg] = registers[reg][:4] + stack[-3:-1]
                            stack.remove(stack[-3:-1])
                            break
                elif (bit == 1):
                    printError("byte register cannot be first operand", address + 1)
                    errFlag = True
            if (not errFlag):
                try:
                    value = str(hex(dec(registers['esp'], 16) + bit)[2:])
                    value = sizeFixer(value, 8, 0)
                    registers['esp'] = value
                except:
                    print("error")
        else:
            printError("Stack is empty", address + 1)
    elif (codes[address].instruction == "jmp"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
            break
    elif (codes[address].instruction == "cmp"):
        Inputs = " ".join(codes[address].inputs)
        inputs = Inputs.split(',')
        inputs = [input.strip() for input in inputs]
        destination = inputs[0]
        source = inputs[1]
        for register in registers:
            if (register == destination):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    value = sizeFixer(value, 8, 0)
                    setCF_OF(value, 32)
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg == source):
                            value = str(negHex(dec(registers[register], 16) - dec(registers[reg], 16)))
                            setAxFlag(registers[register], value)
                            value = sizeFixer(value, 8, 0)
                            setCF_OF(value, 32)
                            break
                elif (isData(source)):
                    result = valueFinder(source, "dword")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    value = sizeFixer(value, 8, 0)
                    setCF_OF(value, 32)
                    # break
                setFlags(value)
                break
            elif (register[1:] == destination):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register][4:], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    value = sizeFixer(value, 4, 0)
                    setCF_OF(value, 16)
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1:] == source):
                            value = str(negHex(dec(registers[register][4:], 16) - dec(registers[reg][4:], 16)))
                            setAxFlag(registers[register], value)
                            value = sizeFixer(value, 4, 0)
                            setCF_OF(value, 16)
                            break
                elif (isData(source)):
                    result = valueFinder(source, "word")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register][4:], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    value = sizeFixer(value, 4, 0)
                    setCF_OF(value, 16)
                    # break
                setFlags(value)
                break
            elif (register[1] + 'l' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register][6:], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    value = sizeFixer(value, 2, 0)
                    setCF_OF(value, 8)
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'l' == source and reg[2] == 'x'):
                            value = str(negHex(dec(registers[register][6:], 16) - dec(registers[reg][6:], 16)))
                            setAxFlag(registers[register], value)
                            value = sizeFixer(value, 2, 0)
                            setCF_OF(value, 8)
                            break
                        elif (reg[1] + 'h' == source and reg[2] == 'x'):
                            value = str(negHex(dec(registers[register][6:], 16) - dec(registers[reg][4:6], 16)))
                            setAxFlag(registers[register], value)
                            value = sizeFixer(value, 2, 0)
                            setCF_OF(value, 8)
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    try:
                        value = str(hex(int(result)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register][6:], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    value = sizeFixer(value, 2, 0)
                    setCF_OF(value, 8)
                    # break
                setFlags(value)
                break
            elif (register[1] + 'h' == destination and register[2] == 'x'):
                if (not isReg(source) and not isData(source)):
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (source[-1] == 'o'):
                            value = str(hex(dec((source[:-1]), 8)))[2:]
                        elif (source[-1] == 'b'):
                            value = str(hex(dec((source[:-1]), 2)))[2:]
                        elif (source[-1] == 'h'):
                            value = str(hex(dec((source[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register][4:6], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    value = sizeFixer(value, 2, 0)
                    setCF_OF(value, 8)
                    # break
                elif (isReg(source)):
                    for reg in registers:
                        if (reg[1] + 'h' == source and reg[2] == 'x'):
                            value = str(negHex(dec(registers[register][4:6], 16) - dec(registers[reg][4:6], 16)))
                            setAxFlag(registers[register], value)
                            value = sizeFixer(value, 2, 0)
                            setCF_OF(value, 8)
                            break
                        elif (reg[1] + 'l' == source and reg[2] == 'x'):
                            value = str(negHex(dec(registers[register][4:6], 16) - dec(registers[reg][6:], 16)))
                            setAxFlag(registers[register], value)
                            value = sizeFixer(value, 2, 0)
                            setCF_OF(value, 8)
                            break
                elif (isData(source)):
                    result = valueFinder(source, "byte")
                    try:
                        value = str(hex(int(source)))[2:]
                    except:
                        if (result[-1] == 'o'):
                            value = str(hex(dec((result[:-1]), 8)))[2:]
                        elif (result[-1] == 'b'):
                            value = str(hex(dec((result[:-1]), 2)))[2:]
                        elif (result[-1] == 'h'):
                            value = str(hex(dec((result[:-1]), 16)))[2:]
                    value = str(negHex(dec(registers[register][4:6], 16) - dec(value, 16)))
                    setAxFlag(registers[register], value)
                    value = sizeFixer(value, 2, 0)
                    setCF_OF(value, 8)
                    # break
                setFlags(value)
                break
    elif (codes[address].instruction == "jz" or codes[address].instruction == "je"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['zf'] == True):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "jnz" or codes[address].instruction == "jne"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['zf'] == False):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "jc"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['cf'] == True):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "jnc"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['cf'] == False):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "jo"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['of'] == True):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "jno"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['of'] == False):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "js"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['sf'] == True):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "jns"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['sf'] == False):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "jp"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['pf'] == True):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "jnp"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['pf'] == False):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "ja" or codes[address].instruction == "jnbe"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['zf'] == False and flags['cf'] == False):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "jae" or codes[address].instruction == "jnb"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['cf'] == False):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "jnae" or codes[address].instruction == "jb"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['zf'] == False and flags['cf'] == True):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "jna" or codes[address].instruction == "jbe"):
        inp = " ".join(codes[address].inputs)
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (flags['zf'] == (not flags['cf'])):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)
    elif (codes[address].instruction == "loop"):
        inp = " ".join(codes[address].inputs)
        value = negHex(dec(registers['ecx'], 16) - 1)
        value = sizeFixer(value, 8, 0)
        registers['ecx'] = value
        findLabel = False
        for lbl in labels:
            if (lbl.name == inp):
                if (dec(registers['ecx'], 16) != 0):
                    address = lbl.address
                findLabel = True
                break
        if (not findLabel):
            printError("undifined symbol " + inp, address + 1)

    address += 1it