def VernamDecrypt(key: str, cipherText: str):
    plainText = ''
    nextKey = ''
    i = 0
    for char in cipherText:
        # print((ord(char) - 65),(ord(key[i])-65), chr((ord(char) - 65) ^ (ord(key[i]) - 65) + 65))
        temp = chr(((ord(char) - 65) ^ (ord(key[i]) - 65)) + 65)
        plainText += chr(ord(temp) + 32)
        nextKey += temp
        i += 1
        if i == len(key):
            key = nextKey
            nextKey = ''
            i = 0

    return plainText.lower()

# VernamDecrypt('ABC', 'HFJMK~F~N')