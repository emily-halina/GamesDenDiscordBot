# dnd dice roller v0.5, with parsing of Ax + b format
# TODO: add handling for any order / combination of die rolls (ie: 2d4 + 3d8 + 2d6 + 7 + 9)

import random

def main():
    input = get_input()
    parse_dice_rolls(input)

def get_input():
    return input('Enter your dice roll! ')

def parse_dice_rolls(input):
    '''
    Parses and rolls dice for Dungeons and Dragons.
    input: string representing a # of dice to roll and a modifier if needed (ie 3d6 + 5)
    output: a formatted string representing the result of the roll
    '''
    input = input.replace(' ', '')
    success = True
    roll_log = []
    # get the prefix
    try:
        prefix = ''
        i = 0
        while input[i].lower() != 'd':
            prefix += input[i]
            i += 1
        # if there is no prefix, roll the dice one time
        if prefix == '':
            prefix = 1
        prefix = int(prefix)

    except IndexError:
        print('invalid prefix!')
        success = False
    except TypeError:
        print('invalid prefix!')
        success = False
    else:
        # get the number of sides for the dice to have
        try:
            i += 1 # getting past 'd' here
            faces = ''
            # get the number of faces
            while input[i] not in ['+', '-'] and i < len(input)-1:
                faces += input[i]
                i += 1
            if input[i] not in ['+', '-']:
                faces += input[i]
            faces = int(faces)
            dice = str(prefix) + 'd' + str(faces) + ':'
            roll_log.append(dice)
            # roll the dice the correct number of times (according to prefix)
            total = 0
            for k in range(prefix):
                roll = random.randint(1, faces)
                total += roll
                roll_log.append('(' + str(roll) + ')')

        except Exception as e:
            print(e.args[0])
            success = False

        else:
            # handle the modifier
            add_sub = None
            if i <= len(input)-1 and input[i] in ['+', '-']:
                if input[i] == '+':
                    add_sub = 'add'
                else:
                    add_sub = 'sub'

            # get the modifier
            modifier = ''
            i += 1
            while i <= len(input)-1:
                modifier += input[i]
                i += 1

            # add or subtract the modifier, if there is one
            if modifier == '':
                modifier = '0'
            modifier = int(modifier)
            if add_sub == 'add':
                total += modifier
                roll_log.append('+')
            elif add_sub == 'sub':
                total -= modifier
                roll_log.append('-')
            if modifier != 0:
                roll_log.append(str(modifier))
            roll_log.append('total: ' + str(total))

    # finish up, returning the correctly formatted log of the roll
    if success:
        print(' '.join(roll_log))
        return ' '.join(roll_log)
    else:
        print('failure! Abort Abort')
        return 'Error! Please follow the format of AdB + C until I have enough brain cells to make it work for any format'

if __name__ == "__main__":
    main()
