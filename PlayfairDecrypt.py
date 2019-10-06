import numpy as np
from collections import OrderedDict

def PlayfairDecrypt(key: str, cipherText: str):
    alphabets = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    codeList = []
    key = key.replace('J', 'I')
    for k in key:
        if k not in codeList:
            codeList.append(k)
            alphabets = alphabets.replace(k, '')
    codeList = codeList + [a for a in alphabets]
    # print(codeList)
    codeMatrix = np.reshape([c for c in codeList], (5, 5))

    position = {}
    for i in range(5):
        for j in range(5):
            position[codeList[i*5+j]] = (i, j)
    
    plainText = ''
    textPair = [cipherText[i:i+2] for i in range(0, len(cipherText), 2)]
    for pair in textPair:
        x1, y1 = position[pair[0]]
        x2, y2 = position[pair[1]]
        if x1 == x2:
            plainText += codeMatrix[x1][(y1 - 1) % 5]
            plainText += codeMatrix[x2][(y2 - 1) % 5]
        elif y1 == y2:
            plainText += codeMatrix[(x1 - 1) % 5]
            plainText += codeMatrix[(x2 - 1) % 5]
        else:
            plainText += codeMatrix[x1][y2]
            plainText += codeMatrix[x2][y1]
    

    return plainText.lower()

# PlayfairDecrypt('COMP', 'HELLOO')