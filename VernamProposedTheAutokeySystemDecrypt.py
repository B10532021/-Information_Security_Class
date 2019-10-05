def PlayfairDecrypt(key, cipherText):
    plainText = ''
    nextKey = ''
    i = 0
    for char in cipherText:
        temp += chr((ord(char) - 65) ^ (ord(key[i]) - 65) + 65)
        plainText += temp
        nextKey += temp
        i += 1
        if i == len(key):
            key = nextKey
            nextKey = ''
            i = 0

    print(plainText)