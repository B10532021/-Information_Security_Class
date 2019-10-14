def CaesarDecrypt(key: int, cipherText: str):
    key = int(key)
    plainText = ''
    for char in cipherText:
        # print(ord(char))
        temp = chr((ord(char) - key - 65) % 26 + 97)
        plainText += temp
    
    return plainText.lower()