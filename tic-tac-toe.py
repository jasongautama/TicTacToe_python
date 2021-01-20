import itertools
from colorama import Fore, Back, Style, init
init() #colorama.init() for windows

"""
def win(:list[list])
This function checks if a player wins the game
it checks for Horizontal, Vertical (|), and Diagonal (/ or \)
parameter: :game [list[list]] (Integer)
return: Boolean
"""
def win(game):
    #win_msg = Fore.GREEN + "\n!!Congratulation!!" + Style.RESET_ALL
    def print_win_msg(player, winType):
        msg = f"\n!!Congratulation!! Player {player} wins {winType}"
        if (player == 0):
            print(Fore.MAGENTA + msg + Style.RESET_ALL)
        else:
            print(Fore.GREEN + msg + Style.RESET_ALL)
    
    def all_same(line):
        #use List count() method to check if the element == length of the board
        # and it's not the starting board element (0)
        if line.count(line[0]) == len(line) and line[0] != 0:
            return True
        else:
            return False
    #Horizontal
    for row in game:
        if all_same(row):
            print_win_msg(row[0], "Horizontally")
            return True
    #Diagonal
    diags = [] 
    #1. from left to right (\)
    for idx in range(len(game)):
        diags.append(game[idx][idx])
    if all_same(diags):
        print_win_msg(diags[0], "Diagonally (\\)")
        return True
    #2. from right to left (/)
    diags = []
    #len(game) = 3 | [{0,3},{1,2}, {2,1}, {3,0}]
    for col, row in enumerate(reversed(range(len(game)))):
        diags.append(game[row][col])
    if all_same(diags):
        print_win_msg(diags[0], "Diagonally (/)")
        return True

    #Vertical
    for col in range(len(game)):
        check = []
        for row in game:
            check.append(row[col])
        if all_same(check):
            print_win_msg(check[0], "Vertically")
            return True
    
    return False

def convert_char_to_idx(char):
    ascii_num = ord(char.upper())#return Unicode/ASCII of char
    try:
        if ascii_num >= 65 and ascii_num <= 90:
            return ascii_num - 65
        else:
            raise ValueError
    except ValueError as e:
        print(Fore.RED + "Column character does not exist " + Style.RESET_ALL, e)     
        return -1  
    except Exception as e:
        print(Fore.RED + "Something went wrong in convert_char_to_idx()" + Style.RESET_ALL, e)
        return -1

"""
def game_board(:list[list], :int, :int, :int, :Boolean)
Display the Tic Tac Toe Board with dynamic size according to user input
return: :list[list(int)](int), :Boolean
"""
#naming convention for function (using underscore)
def game_board(game_map, player=0, row=0, col='A', just_display=False): 
    try:
        column = convert_char_to_idx(col)
        if column == -1:
            raise IndexError

        if game_map[row][column] != 0:
            print(Fore.RED +"This position is occupied! Choose another!" + Style.RESET_ALL)
            return game_map, False    
        print("   "+"  ".join([chr(65 + i) for i in range(len(game_map))])) #65 is A in ASCII code
        if not just_display:
            game_map[row][column] = player
        for count, row in enumerate(game_map):
            colored_row = ""
            for item in row:
                if item == 0:
                    colored_row += "   "
                elif item == 1:
                    colored_row += Fore.GREEN + ' X ' + Style.RESET_ALL
                elif item == 2:
                    colored_row += Fore.MAGENTA + ' O ' + Style.RESET_ALL
            print(count, colored_row)
        return game_map, True
    except IndexError as e:
        msg_error = Fore.RED + "Error: did you input row as 0, 1, 2, .. OR column as A, B, C, ..?" + Style.RESET_ALL
        print(msg_error, e)
        return game_map, False

    except Exception as e: #general Exception
        msg_error = Fore.RED + "Something went very wrong in game_board()!" + Style.RESET_ALL
        print(msg_error, e)
        return game_map, False

    #else:
    #finally:


### __main__ ###
play = True
players = [1,2]
while play:
    game_size = int(input("what size game of tic tac toe (max size: 9) ? "))
    if game_size <= 0 or game_size > 9:
        print("Invalid size! Goodbye..")
        break

    game = [[0 for i in range(game_size)] for i in range(game_size)]
    game_won = False
    game, _ = game_board(game, just_display=True)
    player_choice = itertools.cycle([1,2])

    while not game_won:
        current_player = next(player_choice)
        print(f"Current Player: {current_player}")
        played = False
        while not played:
            column_choice = input("What column do you want to play? (a,b,c, ..): ")[0]
            row_choice  = int(input("What row do you want to play? (0,1,2, ..): "))
            game, played = game_board(game, current_player, row_choice, column_choice)

        if win(game):
            game_won = True
            again = input("Play again? (y/n)")
            if again.lower() == 'y':
                print("restarting")
            elif again.lower() == 'n':
                print("Bye")
                play = False
            else:
                print("Not a valid answer, Goodbye")
                play = False