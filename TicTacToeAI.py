import random


class TicTacToe:
    def __init__(self, cells="_" * 9):
        self.coords_map = {(1, 3): 0, (2, 3): 1, (3, 3): 2,
                           (1, 2): 3, (2, 2): 4, (3, 2): 5,
                           (1, 1): 6, (2, 1): 7, (3, 1): 8}
        self.cells = list(cells)
        self.state = "play"
        self.next_player = "X"

    def print_field(self):
        print("""
---------
| {} {} {} |
| {} {} {} |
| {} {} {} |
---------
""".format(*self.cells))

    def handler(self, next_move):
        """ Handle input from program. next_move must be a list of two numbers representing coordinates."""
        if self.state == "play":
            self.execute_move(next_move, self.next_player)
        self.print_field()
        self.check_condition()
        
    def execute_move(self, next_move, symbol):
        """Update cells with next_move and symbol if valid and update player. Else, print error message."""
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
        """If the game is in any of the end conditions, print a message and change state to "exit"."""
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

    def switch_player(self):
        """Change next move."""
        self.next_player = "O" if self.next_player == "X" else "X"


class AIPlayer:
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty

    def __repr__(self):
        return f"AIPlayer({self.difficulty})"

    def request_move(self, game):
        """Return a tuple of two numbers that are a valid play position in game, based on difficulty."""
        if self.difficulty == "loser":  # Will never play a winning move if possible. If not, will play a random valid move.
            no_win_moves = []
            for i, symbol in enumerate(game.cells):
                if symbol == "_" and not self.check_win(game, i):
                    no_win_moves.append(i)
            return random.choice([list(map(str, coords)) for coords in game.coords_map if game.coords_map[coords] in no_win_moves]) if no_win_moves else AIPlayer("easy").request_move(game)
        if self.difficulty == "easy":  # Plays randomly.
            return random.choice([list(map(str, coords)) for coords in game.coords_map if game.cells[game.coords_map[coords]] == "_"])

    def check_win(self, game, cell_index):
        """Return True if placing next_player symbol in cell_index results in a win, else return False."""
        cells_string = "".join(game.cells[:cell_index] + [game.next_player] + game.cells[cell_index + 1:])
        straights = [cells_string[:3], cells_string[3:6], cells_string[6:], cells_string[::3], cells_string[1::3], cells_string[2::3], cells_string[::4], cells_string[2:7:2]]
        return "XXX" in straights or "OOO" in straights      

game = TicTacToe()
npc = AIPlayer("easy")
game.print_field()
while True:
    game.handler(input("Enter the coordinates: ").split())
    if game.state == "exit": break
    print(f'Making move level "{npc.difficulty}"')
    game.handler(npc.request_move(game))
    if game.state == "exit": break
