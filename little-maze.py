import json


USE = 'e'
EMPTY = ''
FLOOR = '_'
EXIT = 'X'
DOOR = 'D'
SECRET = 'S'
WALL = '*'
ITEMS = 'i'
STARTING_LOCATION = 'start'


def load_map(map_file_name):
    """
        When a map file name is passed the file will load the grid and return it.
        Should you modify this function? No you shouldn't.

    :param map_file_name: a string representing the file name.
    :return: a 2D list which contains the current map.
    """
    with open(map_file_name) as map_file:
        the_map = json.loads(map_file.read())

    return the_map


def play_game(the_grid, row, col, items, door, secret):
    """
    Prints the grid of the game.
    :param the_grid: the map
    :param row: specific row in grid
    :param col: specific column in grid
    :param items: items player has collected, can be empty list
    :param door: indices of where a player has unlocked a door, can be empty list
    :param secret: indices of where a player has unlocked a secret, can be empty list
    """
    # unicode player symbol
    player = '\u1330'

    # opens door if player has unlocked it
    if len(door) != 0:
        for i in range(len(the_grid)):
            for j in range(len(the_grid[i])):
                for k in range(len(door)):
                    for l in range(len(door[k])):
                        if i == door[k][0] and j == door[k][1]:
                            the_grid[i][j]['symbol'] = '_'

    # reveals secret if player has unlocked it
    if len(secret) != 0:
        for i in range(len(the_grid)):
            for j in range(len(the_grid[i])):
                for k in range(len(secret)):
                    for l in range(len(secret[k])):
                        if i == secret[k][0] and j == secret[k][1]:
                            the_grid[i][j]['symbol'] = 'D'

    # prints the grid
    for i in range(len(the_grid)):
        for j in range(len(the_grid[i])):
            if i == row and j == col:
                print(player, end=' ')
            elif the_grid[i][j]['symbol'] == 's':
                print('*', end=' ')
            # replaces i with _ if the player picked up the item
            elif the_grid[i][j]['items']:
                check_item = ''.join(the_grid[i][j]['items'])
                if check_item in items:
                    the_grid[i][j]['items'] = []
                    print('_', end=' ')
                else:
                    print(ITEMS, end=' ')
            else:
                print(the_grid[i][j]['symbol'], end=' ')
        print()


def make_move(the_grid):
    """
    Changes the player's current index based on the moves they want to make. Calls other functions to check doors, secrets, items, and to print the new grid after each move.
    :param the_grid: the map
    """
    items_list = []
    full_items = []
    door_activate = []
    secret_activate = []
    current_row = 0
    current_col = 0
    # if "start":True in map, start there. if not, start at the_grid[0][0]
    for i in range(len(the_grid)):
        for j in range(len(the_grid[i])):
            if "start" in the_grid[i][j]:
                if the_grid[i][j]["start"] == True:
                    current_row = i
                    current_col = j
    current_space = the_grid[current_row][current_col]['symbol']

    # calls play_game to print board at starting index
    play_game(the_grid, current_row, current_col, items_list, door_activate, secret_activate)
    user_move = 'go'

    # loop keeps going until player quits or wins
    while current_space != 'x' and user_move != 'q':
        user_move = input('Enter Move (wasd) (e to activate doors or secrets, q to exit the game): ')
        # checks that the player does not go out of bounds by calling check_move function, returns bool
        if user_move == 'w':
            if check_move(the_grid, (current_row - 1), current_col, items_list) == False:
                current_row += 0
            else:
                current_row -= 1
        elif user_move == 'a':
            if check_move(the_grid, current_row, (current_col - 1), items_list) == False:
                current_col += 0
            else:
                current_col -= 1
        elif user_move == 's':
            if check_move(the_grid, (current_row + 1), current_col, items_list) == False:
                current_row += 0
            else:
                current_row += 1
        elif user_move == 'd':
            if check_move(the_grid, current_row, (current_col + 1), items_list) == False:
                current_col += 0
            else:
                current_col += 1
        # calls check_door and check_secrets to see if the player has unlocked the doors, returns lists
        elif user_move == 'e':
            door_activate = check_door(the_grid, current_row, current_col, items_list)
            secret_activate = check_secrets(the_grid, current_row, current_col, items_list)
            if len(secret_activate) != 0:
                print('You found a secret!')
        # updates the player's current index
        current_space = the_grid[current_row][current_col]['symbol']
        # adds items they may have picked up
        full_items.append(check_items(the_grid, current_row, current_col))
        # puts items in list (because they may have picked up nothing, which returned an empty list)
        for i in range(len(full_items)):
            for j in range(len(full_items[i])):
                if full_items[i][j] != []:
                    if full_items[i][j] not in items_list:
                        items_list.append(full_items[i][j])
        # print new grid with new index
        play_game(the_grid, current_row, current_col, items_list, door_activate, secret_activate)
        # printing inventory
        print('Your inventory is: ', end='')
        print(', '.join(items_list))

    # print if player quits or wins
    if user_move == 'q':
        print('Finished.')
    else:
        print('You win!')


def check_move(the_grid, row, col):
    """
    Checks that the player did not go out of range of the grid.
    :param the_grid: the map
    :return: move = True if legal move, False if illegal move
    """
    move = True
    if row < 0 or row > (len(the_grid) - 1):
        move = False
    elif col < 0 or col > (len(the_grid[0]) - 1):
        move = False
    else:
        for i in range(len(the_grid)):
            for j in range(len(the_grid[i])):
                if the_grid[row][col]['symbol'] == '*':
                    move = False
                elif the_grid[row][col]['symbol'] == 'd':
                    move = False
                elif the_grid[row][col]['symbol'] == 's':
                    move = False

    return move


def check_door(the_grid, row, col, items_list):
    """
    Checks if the player can unlock a door.
    :param the_grid: the map
    :param row: current row of player
    :param col: current col of player
    :param items_list: player's current items
    :return: list of indices of door if unlocked, empty list if not
    """
    open_door = []
    # goes through all the spaces 1 away from current index
    if row + 1 < len(the_grid):
        if the_grid[row+1][col]['symbol'] == 'd':
            # if they need an item and have it, add the door index
            if 'requires' in the_grid[row+1][col]:
                for item in the_grid[row+1][col]['requires']:
                    need_item = item
                if need_item in items_list:
                    door_space = [row + 1, col]
                    open_door.append(door_space)
                # tell them what item they need if they don't have it
                else:
                    print('You still need: ', need_item)
            # if no requirements, add the door index
            else:
                door_space = [row + 1, col]
                open_door.append(door_space)
        if col + 1 <= len(the_grid[0]) - 1:
            if the_grid[row + 1][col + 1]['symbol'] == 'd':
                if 'requires' in the_grid[row + 1][col+1]:
                    for item in the_grid[row + 1][col+1]['requires']:
                        need_item = item
                    if need_item in items_list:
                        door_space = [row + 1, col+1]
                        open_door.append(door_space)
                    else:
                        print('You still need: ', need_item)
                else:
                    door_space = [row + 1, col+1]
                    open_door.append(door_space)
        if col - 1 >= 0:
            if the_grid[row + 1][col - 1]['symbol'] == 'd':
                if 'requires' in the_grid[row + 1][col-1]:
                    for item in the_grid[row + 1][col-1]['requires']:
                        need_item = item
                    if need_item in items_list:
                        door_space = [row + 1, col-1]
                        open_door.append(door_space)
                    else:
                        print('You still need: ', need_item)
                else:
                    door_space = [row + 1, col-1]
                    open_door.append(door_space)
    if row - 1 >= 0:
        if the_grid[row-1][col]['symbol'] == 'd':
            if 'requires' in the_grid[row-1][col]:
                for item in the_grid[row-1][col]['requires']:
                    need_item = item
                if need_item in items_list:
                    door_space = [row - 1, col]
                    open_door.append(door_space)
                else:
                    print('You still need: ', need_item)
            else:
                door_space = [row - 1, col]
                open_door.append(door_space)
        if col + 1 <= len(the_grid[0]) - 1:
            if the_grid[row - 1][col + 1]['symbol'] == 'd':
                if 'requires' in the_grid[row - 1][col+1]:
                    for item in the_grid[row - 1][col+1]['requires']:
                        need_item = item
                    if need_item in items_list:
                        door_space = [row - 1, col+1]
                        open_door.append(door_space)
                    else:
                        print('You still need: ', need_item)
                else:
                    door_space = [row - 1, col+1]
                    open_door.append(door_space)
        if col - 1 >= 0:
            if the_grid[row - 1][col - 1]['symbol'] == 'd':
                if 'requires' in the_grid[row - 1][col-1]:
                    for item in the_grid[row - 1][col-1]['requires']:
                        need_item = item
                    if need_item in items_list:
                        door_space = [row - 1, col-1]
                        open_door.append(door_space)
                    else:
                        print('You still need: ', need_item)
                else:
                    door_space = [row - 1, col-1]
                    open_door.append(door_space)
    if col + 1 <= len(the_grid[0]) - 1:
        if the_grid[row][col+1]['symbol'] == 'd':
            if 'requires' in the_grid[row][col+1]:
                for item in the_grid[row][col+1]['requires']:
                    need_item = item
                if need_item in items_list:
                    door_space = [row, col+1]
                    open_door.append(door_space)
                else:
                    print('You still need: ', need_item)
            else:
                door_space = [row, col + 1]
                open_door.append(door_space)
    if col - 1 >= 0:
        if the_grid[row][col-1]['symbol'] == 'd':
            if 'requires' in the_grid[row][col-1]:
                for item in the_grid[row][col-1]['requires']:
                    need_item = item
                if need_item in items_list:
                    door_space = [row, col-1]
                    open_door.append(door_space)
                else:
                    print('You still need: ', need_item)
            else:
                door_space = [row, col - 1]
                open_door.append(door_space)

    return open_door


def check_secrets(the_grid, row, col, items):
    """
    Checks if the player can unlock secret doors.
    :param the_grid: the map
    :param row: player's current row
    :param col: player's current col
    :param items: list of items player currently has
    :return: list of indices of secret unlocked, empty list if nothing unlocked
    """
    secrets_index = []
    # checks all the spaces 1 away from current index
    if row + 1 < len(the_grid):
        if the_grid[row + 1][col]['symbol'] == 's':
            # if secret requires something, check if the player has it
            if 'requires' in the_grid[row+1][col]:
                for item in the_grid[row+1][col]['requires']:
                    need_item = item
                # if they have the item, add the index to list
                if need_item in items:
                    secret_space = [row + 1, col]
                    secrets_index.append(secret_space)
            # if they don't need an item, add the index to the list
            else:
                secret_space = [row + 1, col]
                secrets_index.append(secret_space)
        if col + 1 <= len(the_grid[0]) - 1:
            if the_grid[row + 1][col + 1]['symbol'] == 's':
                if 'requires' in the_grid[row + 1][col+1]:
                    for item in the_grid[row + 1][col+1]['requires']:
                        need_item = item
                    if need_item in items:
                        secret_space = [row + 1, col+1]
                        secrets_index.append(secret_space)
                else:
                    secret_space = [row + 1, col+1]
                    secrets_index.append(secret_space)
        if col - 1 >= 0:
            if the_grid[row + 1][col - 1]['symbol'] == 's':
                if 'requires' in the_grid[row + 1][col-1]:
                    for item in the_grid[row + 1][col-1]['requires']:
                        need_item = item
                    if need_item in items:
                        secret_space = [row + 1, col-1]
                        secrets_index.append(secret_space)
                else:
                    secret_space = [row + 1, col-1]
                    secrets_index.append(secret_space)
    if row - 1 >= 0:
        if the_grid[row - 1][col]['symbol'] == 's':
            if 'requires' in the_grid[row-1][col]:
                for item in the_grid[row-1][col]['requires']:
                    need_item = item
                if need_item in items:
                    secret_space = [row - 1, col]
                    secrets_index.append(secret_space)
            else:
                secret_space = [row - 1, col]
                secrets_index.append(secret_space)
        if col + 1 <= len(the_grid[0]) - 1:
            if the_grid[row - 1][col + 1]['symbol'] == 's':
                if 'requires' in the_grid[row - 1][col+1]:
                    for item in the_grid[row - 1][col+1]['requires']:
                        need_item = item
                    if need_item in items:
                        secret_space = [row - 1, col+1]
                        secrets_index.append(secret_space)
                else:
                    secret_space = [row - 1, col+1]
                    secrets_index.append(secret_space)
        if col - 1 >= 0:
            if the_grid[row - 1][col - 1]['symbol'] == 's':
                if 'requires' in the_grid[row - 1][col-1]:
                    for item in the_grid[row - 1][col-1]['requires']:
                        need_item = item
                    if need_item in items:
                        secret_space = [row - 1, col-1]
                        secrets_index.append(secret_space)
                else:
                    secret_space = [row - 1, col - 1]
                    secrets_index.append(secret_space)
    if col + 1 <= len(the_grid[0]) - 1:
        if the_grid[row][col + 1]['symbol'] == 's':
            if 'requires' in the_grid[row][col+1]:
                for item in the_grid[row][col+1]['requires']:
                    need_item = item
                if need_item in items:
                    secret_space = [row, col+1]
                    secrets_index.append(secret_space)
            else:
                secret_space = [row, col + 1]
                secrets_index.append(secret_space)
    if col - 1 >= 0:
        if the_grid[row][col - 1]['symbol'] == 's':
            if 'requires' in the_grid[row][col-1]:
                for item in the_grid[row][col-1]['requires']:
                    need_item = item
                if need_item in items:
                    secret_space = [row, col-1]
                    secrets_index.append(secret_space)
            else:
                secret_space = [row, col - 1]
                secrets_index.append(secret_space)

    return secrets_index


def check_items(the_grid, row, col):
    """
    Adds items the player has picked up
    :param the_grid: the map
    :param row: current row of player
    :param col: current col of player
    :return: list of inventory, empty if no items are picked up
    """
    inventory = []
    for item in the_grid[row][col]['items']:
        inventory.append(item)

    return inventory


if __name__ == '__main__':
    map_file_name = input('What map do you want to load? ')
    the_game_map = load_map(map_file_name)
    if the_game_map:
        # calls make_move
        make_move(the_game_map)