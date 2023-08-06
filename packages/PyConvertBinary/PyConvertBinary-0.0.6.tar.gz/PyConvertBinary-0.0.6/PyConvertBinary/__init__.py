Hexadecimal = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F')
def BinToDec(num):
    answer = 0
    if isinstance(num, float):
        return 'Error: float\n{} is a float not a base {}'.format(num, '2 binary')
    num = ''.join(str(num)[::-1])
    for _ in range(len(num)):
        if num[_] == '1':
            answer += 2 ** _
        elif num[_] == '0':
            pass
        else:
            return "Error: Not Binary\n{} in {} makes it not a base 2 binary".format(num[_], ''.join(reversed(num)))
    return answer
def BinToOct(num):
    return DecToOct(BinToDec(num))
def BinToHex(num):
    return DecToHex(BinToDec(num))
def DecToBin(num):
    List = ''
    if isinstance(num, float):
        return 'Error: float\n{} is a float not a base {}'.format(num, '10 decimal')
    num = int(num)
    while num > 0:
        if num % 2 != 0:
            List += '1'
        else:
            List += '0'
        num = num // 2
    return ''.join(List[::-1])
def DecToOct(num):
    remainder = []
    if isinstance(num, float):
        return 'Error: float\n{} is not a base {}'.format(num, '10 decimal')
    num = int(num)
    while num > 0:
        remainder += [num % 8]
        num = num // 8
    num = ''
    for _ in remainder:
        num += Hexadecimal[_]
    return ''.join(num[::-1])
def DecToHex(num):
    remainder = []
    if isinstance(num, float):
        return 'Error: float\n{} is not a base {}'.format(num, '10 decimal')
    num = int(num)
    while num > 0:
        remainder += [num % 16]
        num = num // 16
    num = ''
    for _ in remainder:
        num += Hexadecimal[_]
    return ''.join(num[::-1])
def HexToBin(num):
    return DecToBin(HexToDec(num))
def HexToDec(num):
    num = str(num).upper()
    answer = 0
    count = 0
    for _ in num:
        if _ not in Hexadecimal:
            return 'Not Hex Format'
    num = num[::-1]
    for _ in num:
        answer += (Hexadecimal.index(_) * 16 ** count)
        count += 1
    return answer
def HexToOct(num):
    return DecToOct(HexToDec(num))
def OctToBin(num):
    return DecToBin(OctToDec(num))
def OctToDec(num):
    num = str(num).upper()
    answer = 0
    count = 0
    for _ in num:
        if _ not in Hexadecimal[:8]:
            return 'Not Oct Format'
    num = num[::-1]
    for _ in num:
        answer += (Hexadecimal.index(_) * 8 ** count)
        count += 1
    return answer
def OctToHex(num):
    DecToHex(OctToDec(num))
def AddressBin(num, Type):
    List = []
    num = num.split('.')
    if Type == 'Dec':
        for _ in num:
            List += [DecToBin(_)]
        num = '.'.join(List)
    elif Type == 'Hex':
        for _ in num:
            List.append(HexToBin(_))
        num = ':'.join(List)
    return num