'''
Set of functions for use in the Games Den West Marches campaign.

Utilizes WM.txt, which contains info on each West Marches character as follows:

character name, player name, current level, EXP value, gold, guild coins (GC)
'''

LEVEL_TO_EXP = {1:1, 2:3, 3:7, 4:14, 5:24, 6:36, 7:52, 8:84, 9:120, 10:160,
11:204, 12:300, 13:404, 14:516, 15:636, 16:892, 17:1164, 18:1452, 19:1756, 20:2076}

def initialize():
    f = open("WM.txt", "r")
    i = f.read().splitlines()
    f.close()
    info = []
    for a in i:
        info.append(a.split(","))
    return info

def create_char(name, player, gold):
    # new character starts at level 1, and is 0% of the way to level 2, hence 1, 0
    # they also start with 0 guild coins (last entry)
    new_char = ",".join([name, player, "1", "0", gold, "0"]) + "\n"
    f = open("WM.txt", "a")
    f.write(new_char)
    f.close()
    ret = "Character created!\nName: " + name + "\nPlayer: " + player
    return ret

def gain_exp(name, player, EC):
    # gain exp according to a given chart
    info = initialize()
    found = False
    char_p = -1
    CL = -1
    CX = -1
    gold = -1
    GC = -1
    for char in info:
        if char[0].lower() == name.lower():
            char_p = char[1]
            CL = int(char[2])
            CX = int(char[3]) # current XP
            gold = int(char[4])
            GC = int(char[5])
            found = True
    print("CL", CL, "CX", CX, "gold", gold, "GC", GC)
    if found:
        if char_p != player and player != "Kaifin" and player != "Atharv":
            return ("It appears this is not your character :( This character belongs to " + char_p)
        LU = False
        CX += EC
        print(CX)
        if EC < 0:
            print("impossible encounter! XP should always be positive")
            return "impossible encounter! XP should always be positive"

        while CX >= LEVEL_TO_EXP[CL]:
            LU = True
            CL += 1
        update_char(name, player, CL, CX, gold, GC)

        if LU:
            print("level up")
            ret = "Congrats! You levelled up! You are now level " + str(CL) + ". You are " + str(LEVEL_TO_EXP[CL] - CX) + " EXP from your next level up!\nName: " + name + "\nPlayer: " + player
        else:
            print("no level up")
            ret = "You are level " + str(CL) + ". You are " + str(LEVEL_TO_EXP[CL] - CX) + " EXP from your next level up!\nName: " + name + "\nPlayer: " + player
        return ret
    else:
        return "character not found!"

def update_char(name, player, level, CX, gold, GC):
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
        lines[i] = ",".join([name, player, str(level), str(CX), str(gold), str(GC)]) + "\n"
        f.close()

        f = open("WM.txt", "w")
        f.writelines(lines)
        f.close()
    else:
        print("character not found")

def change_gold(name, player, change_amount):
    info = initialize()
    found = False
    CL = -1
    CX = -1
    gold = -1
    GC = -1
    for char in info:
        if char[0].lower() == name.lower():
            CL = int(char[2])
            CX = int(char[3]) # current XP
            gold = int(char[4])
            GC = int(char[5])
            found = True
    if found:
        if char_p != player and player != "Kaifin" and player != "Atharv":
            return ("It appears this is not your character :( This character belongs to " + char_p)
        if gold + change_amount < 0:
            return "Hey! You don't have enough money to do that! You only have " + str(gold) + " gold, and are trying to spend " + str(change_amount*(-1)) + "."
        update_char(name, player, CL, CX, gold + change_amount, GC)
        return "Your character " + str(name) + " now has " + str(gold + change_amount) + " gold!"
    else:
        return "Character not found!"

def get_status(name):
    info = initialize()
    player = -1
    CL = -1
    CX = -1
    gold = -1
    GC = -1
    for char in info:
        if char[0].lower() == name.lower():
            char[3] = (LEVEL_TO_EXP[int(char[2])] - int(char[3]))
            return char
    return None

def change_GC(name, player, change_amount):
    info = initialize()
    found = False
    CL = -1
    CX = -1
    gold = -1
    GC = -1
    for char in info:
        if char[0].lower() == name.lower():
            CL = int(char[2])
            CX = int(char[3]) # current XP
            gold = int(char[4])
            GC = int(char[5])
            found = True
    if found:
        if GC + change_amount < 0:
            return "Hey! You don't have enough money to do that! You only have " + str(GC) + " guild coins, and are trying to spend " + str(change_amount*(-1)) + "."
        update_char(name, player, CL, CX, gold, GC + change_amount)
        return "Your character " + str(name) + " now has " + str(GC + change_amount) + " guild coins!"
    else:
        "Character not found!"
