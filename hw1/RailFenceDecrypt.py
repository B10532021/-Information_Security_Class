def RailFenceDecrypt(key: int, cipherText: str):
    key = int(key)
    plainText = ''
    railMatrix = [['*' for i in range(len(cipherText))] for j in range(key)]
    down = False
    row = 0
    col = 0

    for i in range(len(cipherText)):
        if row is 0:
            down = True
        elif row is key - 1:
            down = False
        railMatrix[row][col] = '?'
        col += 1

        if down:
            row += 1
        else:
            row -= 1
    
    pos = 0
    for i in range(key):
        for j in range(len(cipherText)):
            if railMatrix[i][j] == '?' and pos < len(cipherText):
                railMatrix[i][j] = cipherText[pos]
                pos += 1
    
    row, col = 0, 0
    for i in range(len(cipherText)):
        if row is 0:
            down = True
        elif row is key - 1:
            down = False

        if railMatrix[row][col] != '?' and railMatrix[row][col] != '':
            plainText += railMatrix[row][col]
            col += 1

        if down:
            row += 1
        else:
            row -= 1

    return plainText.lower()

# RailFenceDecrypt(3, 'HOLELWRDLO')