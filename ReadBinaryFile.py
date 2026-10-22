binaryFile = input("Binary File: ")
data = open(binaryFile, "rb").read()
bits = ""
for byte in data:
    bits += format(byte, "08b")
print(bits)