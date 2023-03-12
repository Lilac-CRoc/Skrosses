import os
import sys
import time

Blank = " "
Nought = "○"
Cross = "X"
Winner = "none"
Playing = True
NoughtTurn = False
Ask = True
b = {'a1': Blank, 'a2': Blank, 'a3': Blank, 'b1': Blank, 'b2': Blank,
     'b3': Blank, 'c1': Blank, 'c2': Blank, 'c3': Blank}
ValidMove = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']
check = []


def clear():
    # OS Independent terminal clear
    os.system('cls' if os.name == 'nt' else 'clear')


def quit_game():
    global Playing
    Playing = False
    clear()
    print("Exiting...")
    sys.exit("Program closed.")


def help_display():
    with open((os.path.join(os.path.dirname(__file__), 'help.txt')), 'rt') as f:
        for line in f:
            print(line.strip())
        print("\n")


def input_check():
    global Winner
    global NoughtTurn
    if NoughtTurn:
        current_player = Nought
    else:
        current_player = Cross
    while True:
        print(current_player, "'s turn: ", end='', sep="")
        texty = input()
        human1 = texty
        # Attempts to add either nought or cross into the board
        # and checks to see if the input is valid. If not
        # KeyError is raised and prints an error
        try:
            if human1.lower() == "resign" or human1.lower() == "r":
                print(current_player, "resigned!")
                time.sleep(1.5)
                if current_player == Nought:
                    Winner = Cross
                else:
                    Winner = Nought
                break
            if human1.lower() == "pass" or human1.lower() == "p":
                print(current_player, "passed its turn")
                time.sleep(0.75)
                break
            elif human1.lower() == "exit":
                confirm = input("Are you sure you want to exit? (Y/n)\n")
                if confirm.lower() == "yes" or confirm.lower() == "y":
                    quit_game()
                else:
                    if NoughtTurn:
                        NoughtTurn = False
                    else:
                        NoughtTurn = True
                break
            elif human1.lower() == "help" or human1.lower() == "h":
                clear()
                help_display()
                input("Press enter to continue...\n")
                update_board()
            else:
                # Check for invalid moves such as out of range moves
                # and ones that already has been filled
                if ValidMove.count(human1.lower()) == 0 or not b.get(human1.lower()) == " ":
                    raise KeyError
                if current_player == Nought:
                    b[human1.lower()] = Nought
                else:
                    b[human1.lower()] = Cross
                    # print("Successfully set",human1 ,"to", b[human1])
                break
        except KeyError:
            update_board()
            print("\"", human1, "\" is an invalid move!", sep="")


def update_board():
    clear()
    # Prints the board
    print("  a  b  c")
    print("1 ", b['a1'], " │", b['b1'], " │", b['c1'], sep="")
    print("  ――+――+――")
    print("2 ", b['a2'], " │", b['b2'], " │", b['c2'], sep="")
    print("  ――+――+――")
    print("3 ", b['a3'], " │", b['b3'], " │", b['c3'], sep="")


def update_turn():
    global NoughtTurn
    global Winner
    checking_side = "X"
    increment = 1
    # First checks for a winning combination. If not, check for if the board
    # is fully filled and declares a draw
    while True:
        matches = 0
        row_counter = 0
        if increment > 2:
            break
        elif increment == 2:
            checking_side = "○"
        check_grid = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3', 'a1', 'b1', 'c1',
                      'a2', 'b2', 'c2', 'a3', 'b3', 'c3', 'a1', 'b2', 'c3', 'a3', 'b2', 'c1']
        for i in range(len(check_grid)):
            if checking_side == b[check_grid.pop()]:
                matches = matches + 1
            row_counter = row_counter + 1
            if matches == 3 and row_counter > 2:
                Winner = checking_side
                break
            if row_counter > 2:
                row_counter = 0
                matches = 0
        increment = increment + 1
    if " " not in [*b.values()] and Winner == "none":
        Winner = "Draw!"
        # Passes turn to the next player if neither of the criteria matches
    if NoughtTurn:
        NoughtTurn = False
    else:
        NoughtTurn = True


update_board()
print("Use \"Help\" to show help")
try:
    while Playing:
        while Winner == "none":
            input_check()
            update_board()
            update_turn()
        if Winner == "Draw!":
            print(Winner)
        else:
            print(Winner, "Wins!")
        Ask = True
        replay = input("Do you want to play again? (Y/n)\n")
        while Ask:
            try:
                if replay.lower() == "yes" or replay.lower() == "y":
                    Ask = False
                    Winner = "none"
                    NoughtTurn = False
                    b.clear()
                    b = {'a1': Blank, 'a2': Blank, 'a3': Blank, 'b1': Blank, 'b2': Blank,
                         'b3': Blank, 'c1': Blank, 'c2': Blank, 'c3': Blank}
                    update_board()
                elif replay.lower() == "no" or replay.lower() == "n":
                    Ask = False
                    Playing = False
                else:
                    raise ValueError
            except ValueError:
                pass
finally:
    quit_game()
