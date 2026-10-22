def get_count(x):
    return x[0]

def compress(in_file, out_file, limit = 0.05):
    print("=" * 80)
    text = open(in_file, encoding="utf-8", newline="").read()

    # count character frequency  
    count = {}
    for ch in text:
        count[ch] = count.get(ch, 0) + 1

    print(f"Character Frequency: {count}")

    # characters < limit 
    others = []
    for ch in count:
        if count[ch] / len(text) <= limit:
            others.append(ch)
    
    print(f"Others: {others}")

    items = []
    for ch in count:
        if ch not in others:
            items.append([count[ch], [ch]])
    if others:
        total = 0
        for ch in others:
            total += count[ch]
        items.append([total, ["OTHERS"]])

    print(f"Symbols To be coded: {items}")

    # huffman coding
    codes = {}
    for item in items:
        codes[item[1][0]] = ""

    # Edge case if there is only one item in the list
    if len(items) == 1:
        codes[items[0][1][0]] = "0"       

    while len(items) > 1:
        items.sort(key=get_count)
        a = items.pop(0)
        b = items.pop(0)
        for s in a[1]:
            codes[s] = "0" + codes[s]
        for s in b[1]:
            codes[s] = "1" + codes[s]
        items.append([a[0] + b[0], a[1] + b[1]])

    # minimum bits to represent rare chars 
    width = 0
    while 2 ** width < len(others):
        width += 1

    bits = ""
    for ch in text:
        if ch in others:
            index = others.index(ch)
            bits += codes["OTHERS"]
            if width > 0:
                bits += format(index, "0" + str(width) + "b")
        else:
            bits += codes[ch]


    pad = (8 - len(bits) % 8) % 8
    bits += "0" * pad
    data = bytearray()
    for i in range(0, len(bits), 8):
        data.append(int(bits[i:i + 8], 2))
    open(out_file, "wb").write(data)

    # overhead list
    info = open(out_file + ".info", "w")
    info.write(str(len(text)) + "\n")
    info.write(str(pad) + "\n")
    for s in codes:
        name = s if s == "OTHERS" else str(ord(s))
        info.write(name + " " + codes[s] + "\n")
    info.write("RARE " + " ".join(str(ord(ch)) for ch in others) + "\n")
    info.close()

    print(f"Original: {len(text) * 8}")
    print(f"Compressed: {len(bits) - pad} bits")
    print("Codes :", codes)
    print("=" * 80)

def decompress(in_file, out_file):
    lines = open(in_file + ".info").read().split("\n")
    n_symbols = int(lines[0])
    pad = int(lines[1])
    decode = {}                 
    others = []
    for line in lines[2:]:
        if line.startswith("RARE"):
            others = [chr(int(x)) for x in line.split()[1:]]
        elif line != "":
            name, code = line.split()
            decode[code] = name if name == "OTHERS" else chr(int(name))

    width = 0
    while 2 ** width < len(others):
        width += 1

    bits = ""
    for byte in open(in_file, "rb").read():
        bits += format(byte, "08b")
    bits = bits[:len(bits) - pad]

    text = ""
    code = ""
    i = 0
    while i < len(bits):
        code += bits[i]
        i += 1
        if code in decode:
            if decode[code] == "OTHERS":
                index = int(bits[i:i + width], 2) if width > 0 else 0
                i += width
                text += others[index]
            else:
                text += decode[code]
            code = ""

    open(out_file, "w", encoding="utf-8", newline="").write(text)
    print(f"Decompressed {len(text)} characters")

mode = input("compress or decompress? (c/d): ")
in_file = input("Input file: ")
out_file = input("Output file: ")
if mode == "c":
    limit = float(input("Minimum limit of probability (e.g. 0.05): "))
    compress(in_file, out_file, limit)
else:
    decompress(in_file, out_file)