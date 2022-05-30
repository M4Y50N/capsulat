n = int(input())

while n > 0:
    senha = input()

    if len(senha) != 20:
        print("INVALID DATA")
        continue
    elif senha[:2] != "RA":
        print("INVALID DATA")
        continue
    elif not(senha[2:].isnumeric()):
        print("INVALID DATA")
        continue

    print(int(senha[2:]))
