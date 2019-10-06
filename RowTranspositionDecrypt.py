import math

def RowDecrypt(key: str, cipherText: str):
    plainText = ''
    rows = int(math.ceil(len(cipherText) / len(key)))
    spaceLeft = rows * len(key) - len(cipherText)
    cipherMatrix = [[] for i in range(len(key))]

    for i in range(len(key)):
        pos = key.find(str(i + 1))
        if pos + spaceLeft >= len(key):
            cipherMatrix[i] = list(cipherText[:rows - 1] + '_')
            cipherText = cipherText[rows - 1:]
        else:
            cipherMatrix[i] = list(cipherText[:rows])
            cipherText = cipherText[rows:]

    for row in range(rows):
        for col in key:
            if cipherMatrix[int(col) - 1][row] == '_':
                continue
            plainText += cipherMatrix[int(col) - 1][row]


    print(plainText.lower())

RowDecrypt('4312567', 'TTNAAPTMTSUOAODWCOIXKNLYPET')