def CaesarDecrypt(key, cipherText):
    plainText = ''
    for char in cipherText:
        # print(ord(char))
        temp = chr((ord(char) - key - 65) % 26 + 97)
        plainText += temp
    
    print(plainText)