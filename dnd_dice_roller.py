# D&D dice roller v1.0
# takes in a list of dice

import random


def main():
    content = get_input()
    parse_dice_rolls(content)


def get_input():
    return input("Enter your dice roll! ")


def parse_dice_rolls(content):
    # parse the input into a list
    content = content.replace(" ", "")
    content = content.replace("💯", "100")  # 💯
    if content == "":
        return random.randint(1, 100)
    input_list = []
    modifier = 0
    chunk = ""
    add_sub = True

    for c in content:
        if c != "+" and c != "-":
            chunk += c
        else:
            input_list.append(chunk)
            input_list.append(c)
            chunk = ""

    if chunk != "":
        input_list.append(chunk)

    running_total = []
    roll_log = []
    # process the input
    for item in input_list:
        item = item.lower()
        # this is a dice
        if "d" in item:
            new_dice = list()
            new_dice.append(item + ":")
            # find prefix (if there is one)
            i = 0
            prefix = ""
            while item[i] != "d":
                prefix += item[i]
                i += 1
            if prefix == "":
                prefix = "1"
            try:
                prefix = int(prefix)
            except ValueError:
                print("Whoops prefix")
                return "Error! Please double-check your formatting and try again!"

            # get number of faces
            i += 1
            faces = ""
            while i < len(item):
                faces += item[i]
                i += 1
            try:
                faces = int(faces)
            except ValueError:
                print("Whoops faces")
                return "Error! Please double-check your formatting and try again!"

            if faces == 0:
                return "do not try to roll a d0 please."
            die_total = 0
            # roll the dice
            for k in range(prefix):
                roll = random.randint(1, faces)
                die_total += roll
                new_dice.append("(" + str(roll) + ")")
            running_total.append(die_total)
            roll_log.append(new_dice)

        else:
            roll_log.append(item)
            running_total.append(item)
            print(roll_log)
            if item == "+":
                add_sub = True
            elif item == "-":
                add_sub = not add_sub
            elif item != "":  # debug this later
                if add_sub:
                    modifier += int(item)
                else:
                    modifier -= int(item)

    # tally up the running total accounting for signs
    add_sub = True
    total = 0
    for term in running_total:
        if term != "+" and term != "-" and term != "":
            if add_sub:
                total += int(term)
            else:
                total -= int(term)
        else:
            if term == "+":
                add_sub = True
            else:
                add_sub = not add_sub

    roll_log.append(modifier)
    roll_log.append(str(total))
    print(roll_log)
    return roll_log


if __name__ == "__main__":
    main()
