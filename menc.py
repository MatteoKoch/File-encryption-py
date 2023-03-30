import sys
import numpy as np


def progressbar(it, prefix="", size=60, out=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, "█"*x, "."*(size-x), j, count),
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)


def generateKey(a):
    key = ''
    for i in a:
        key += bin(256 - ord(i)).replace('0b', '')
    return key


def getBits(txt):
    bits = []
    for i in range(0, 8-len(txt)):
        bits.append(int(0))
    for i in range(len(txt)):
        bits.append(int(txt[i]))
    return bits


def getName(file, wr):
    for i in reversed(range(len(file))):
        if file[i] == '.' or file[i] == 46:
            if wr:
                return file[:i], file[i:]
            else:
                return file[i:]
    return 0


def toInt(nr):
    sum = 0;
    for i in reversed(range(len(nr))):
        sum += pow(2,7-i)*int(nr[i])
    return sum


def compare(a, b, reverse):
    if reverse:
        bInput = bin(255-a).replace('0b', '')
    else:
        bInput = bin(a).replace('0b', '')
    bMask = getBits(bInput)
    bOpfer = [int(bit) for bit in b]
    res = []
    for i in range(8):
        bTeller = bool(bOpfer[i]) ^ bool(bMask[i])
        if bTeller:
            res.append(str(1))
        else:
            res.append(str(0))
    return "".join(res)


def de_magie(content, a):
    key = generateKey(a)
    newContent = []
    for i in progressbar(range(len(content)), "Entschlüsseln: ", 40):
        keyIndex = (i * 8) % len(key)
        binary = str(compare(ord(content[i]), key[keyIndex:keyIndex + 8], True))
        newContent.append(255-toInt(binary))

    return newContent


def en_magie(content, a):
    key = generateKey(a)
    newContent = []
    content = bytearray(content)
    content = np.array(content)
    for i in progressbar(range(len(content)), "Verschlüsseln: ", 40):
        keyIndex = (i * 8) % len(key)
        binary = str(compare(content[i], key[keyIndex:keyIndex + 8], False))
        newContent.append(chr(toInt(binary)).encode())

    return newContent


def decmat_turbocrypt(a):
    fileName = getName(sys.argv[2], True)[0]
    fileType = getName(sys.argv[2], True)[1]
    if fileType == '.menc':
        oldFile = open(sys.argv[2], 'rb')
        oldFileRead = oldFile.read()
        oldFileType = getName(oldFileRead, True)[1].decode('utf-8')
        oldFileContent = getName(oldFileRead, True)[0].decode()
        newFile = open(f'{fileName}2{oldFileType}', 'wb')

        deContent = bytearray(de_magie(oldFileContent, a))
        deContent = np.array(deContent)

        for i in range(len(deContent)):
            newFile.write(deContent[i])
        newFile.close()
        oldFile.close()
    else:
        print("du kannst nur .men Dateien decrypten!")


def encmat_turbocrypt(a):
    fileName = getName(sys.argv[2], True)[0]
    fileType = getName(sys.argv[2], True)[1]
    newFile = open(f'{fileName}.menc', 'wb')
    oldFile = open(sys.argv[2], 'rb')
    oldContent = oldFile.read()

    enContent = en_magie(oldContent, a)

    for i in range(len(enContent)):
        newFile.write(enContent[i])
    newFile.write(fileType.encode())
    oldFile.close()
    newFile.close()


if len(sys.argv) == 4:
    if sys.argv[3] != '':
        try:
            if sys.argv[1] == '-e':
                encmat_turbocrypt(sys.argv[3])
            elif sys.argv[1] == '-d':
                decmat_turbocrypt(sys.argv[3])
        except KeyboardInterrupt:
            print("\nTastaturabbruch")
        except AttributeError:
            print("File ist leer")
        except TypeError:
            print("File ist leer")
        except ZeroDivisionError:
            print("Du kannst nur ein Mal verschlüsseln")
    else:
        print("Falsches Passwort!")
else:
    error_msg = "Da fehlt was! Aufbau:\n" \
                "python main.py (-e/-d) [Datei] [Passwort]"
    print(error_msg)
