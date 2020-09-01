# D&D dice roller v1.0
# takes in a list of dice

import random

def main():
    input = get_input()
    parse_dice_rolls(input)

def get_input():
    return input('Enter your dice roll! ')

def parse_dice_rolls(input):

    # parse the input into a list
    input = input.replace(' ', '')
    input_list = []
    chunk = ''
    for c in input:
        if c != '+' and c != '-':
            chunk += c
        else:
            input_list.append(chunk)
            input_list.append(c)
            chunk = ''

    if chunk != '':
        input_list.append(chunk)

    running_total = []
    roll_log = []
    # process the input
    for item in input_list:
        item = item.lower()
        # this is a dice
        if 'd' in item:
            roll_log.append(item + ':')
            # find prefix (if there is one)
            i = 0
            prefix = ''
            while item[i] != 'd':
                prefix += item[i]
                i += 1
            try:
                prefix = int(prefix)
            except:
                print('Whoops prefix')
                return 'Error! Please double-check your formatting and try again!'

            # get number of faces
            i += 1
            faces = ''
            while i < len(item):
                faces += item[i]
                i += 1
            try:
                faces = int(faces)
            except:
                print('Whoops faces')
                return 'Error! Please double-check your formatting and try again!'

            die_total = 0
            # roll the dice
            for k in range(prefix):
                roll = random.randint(1, faces)
                die_total += roll
                roll_log.append('(' + str(roll) + ')')
            running_total.append(die_total)

        else:
            roll_log.append(item)
            running_total.append(item)

    # tally up the running total accounting for signs
    add_sub = True
    total = 0
    for term in running_total:
        if term != '+' and term != '-':
            if add_sub:
                total += int(term)
            else:
                total -= int(term)
        else:
            if term == '+':
                add_sub = True
            else:
                add_sub = False

    roll_log.append('Total: ' + str(total))
    print(' '.join(roll_log))
    return ' '.join(roll_log)


if __name__ == "__main__":
    main()
