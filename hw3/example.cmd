echo off
echo "Encrypt image with ECB, CBC, and CTR mode, respectively."
python ./Encrypt.py images/Tux.png ECB
python ./Encrypt.py images/Tux.png CBC
python ./Encrypt.py images/Tux.png CTR
echo "Finish Encryption."

echo "Decrypt image with ECB, CBC, and CTR mode, respectively."
python ./Decrypt.py images/Tux_ECB/Encrypted.png ECB
python ./Decrypt.py images/Tux_CBC/Encrypted.png CBC
python ./Decrypt.py images/Tux_CTR/Encrypted.png CTR
echo "Finish Decryption."