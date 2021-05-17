'''
Set of functions for use in the Games Den West Marches campaign.

Utilizes WM.txt, which contains info on each West Marches character as follows:

character name, player name, current level, EXP value
'''

def initialize():
    f = open("WM.txt", "r")
    i = f.read().splitlines()
    f.close()
    info = []
    for a in i:
        info.append(a.split(","))
    return info

def create_char(name, player):
    # new character starts at level 1, and is 0% of the way to level 2, hence 1, 0
    new_char = ",".join([name, player, "1", "0"]) + "\n"
    f = open("WM.txt", "a")
    f.write(new_char)
    f.close()

def gain_exp(name, player, EC):
    # gain exp according to the formula (EC - CL + 1) / CL
    # if the resulting XP is over 1, gain level(s)
    info = initialize()
    found = False
    CL = -1
    CX = -1
    for char in info:
        if char[0].lower() == name.lower():
            CL = int(char[2])
            CX = float(char[3]) # current XP
            found = True
    if found:
        CX += (EC - CL + 1) / CL
        if CX <= 0 or EC < CL:
            raise Exception("impossible encounter! EC should always be < CL")
        while CX >= 1:
            CL += 1
            CX -= 1
        update_char(name, player, CL, CX)
    else:
        print("character not found")
    return 

def update_char(name, player, level, CX):
    i = 0
    found = False
    info = initialize()

    for char in info:
        if char[0].lower() == name.lower():
            found = True
            break
        i += 1

    if found:
        f = open("WM.txt", "r")
        lines = f.readlines()
        lines[i] = ",".join([name, player, str(level), str(CX)]) + "\n"
        f.close()

        f = open("WM.txt", "w")
        f.writelines(lines)
        f.close()
    else:
        print("character not found")
        
gain_exp("character2", "player2", 8)