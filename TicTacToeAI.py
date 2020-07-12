import random

class TicTacToe:
    def __init__(self, cells="_" * 9):
        self.coords_map = {(1, 3): 0, (2, 3): 1, (3, 3): 2,
                           (1, 2): 3, (2, 2): 4, (3, 2): 5,
                           (1, 1): 6, (2, 1): 7, (3, 1): 8}
        self.cells = list(cells)
        self.state = "playX"

    def print_field(self):
        print("""
---------
| {} {} {} |
| {} {} {} |
| {} {} {} |
---------
""".format(*self.cells))

    def handler(self, next_move):
        """ Handle input from program. next_move must be a list of numbers representing coordinates."""
        if self.state == "playX":
            self.execute_move(next_move, "X")
        elif self.state == "playO":
            self.execute_move(next_move, "O")
        self.print_field()
        self.check_condition()
        
    def execute_move(self, next_move, symbol):
        """ Update cells with next_move and symbol if valid and update player. Else, print error message."""
        if all(value.isdigit() for value in next_move):
            next_move = tuple(int(value) for value in next_move)
            if next_move not in self.coords_map:
                print("Coordinates should be from 1 to 3!")
            elif self.cells[self.coords_map[next_move]] != "_":
                print("This cell is occupied! Choose another one!")
            else:
                self.cells[self.coords_map[next_move]] = symbol
                self.switch_player()
        else:
            print("You should enter numbers!")

    def check_condition(self):
        cells_string = "".join(self.cells)
        straights = [cells_string[:3], cells_string[3:6], cells_string[6:], cells_string[::3], cells_string[1::3], cells_string[2::3], cells_string[::4], cells_string[2:7:2]]
        if abs(cells_string.count("X") - cells_string.count("O")) > 1 or "XXX" in straights and "OOO" in straights:
            print("Impossible")
            self.state = "exit"
        elif "XXX" in straights:
            print("X wins")
            self.state = "exit"
        elif "OOO" in straights:
            print("O wins")
            self.state = "exit"
        elif "_" not in cells_string: 
            print("Draw")
            self.state = "exit"
        else:
            print("Game not finished")

    def switch_player(self):
        self.state = "playO" if self.state == "playX" else "playX"
    
game = TicTacToe(input("Enter cells: "))
game.print_field()
while game.state != "exit":
    game.handler(input("Enter the coordinates: ").split())