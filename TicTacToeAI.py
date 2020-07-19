import random


class TicTacToe:
    def __init__(self, cells="_" * 9):
        self.coords_map = {(1, 3): 0, (2, 3): 1, (3, 3): 2,
                           (1, 2): 3, (2, 2): 4, (3, 2): 5,
                           (1, 1): 6, (2, 1): 7, (3, 1): 8}
        self.reverse_coords_map = {v: k for k, v in self.coords_map.items()}
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
        """ Handle input from program. next_move must be a tuple of two integers."""
        if self.state == "play":
            self.execute_move(next_move, self.next_player)
            self.switch_player()
        self.print_field()
        self.check_condition()
        
    def execute_move(self, next_move, symbol):
        """Update cells with next_move and symbol. next_move must be a tuple of two integers."""
        self.cells[self.coords_map[next_move]] = symbol

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


class Player:
    available_difficulties = ["user", "loser", "easy", "medium", "hard"]

    def __init__(self, difficulty):
        self.difficulty = difficulty

    def __repr__(self):
        return f"Player({self.difficulty})"

    def request_move(self, game):
        """Return a tuple of two integers that are a valid play position in game, based on difficulty."""
        if self.difficulty == "user":
            return self.user_move(game)
        print(f'Making move level "{self.difficulty}"')
        if self.difficulty == "loser":  # Will never play a winning move if possible. If not, will play a random valid move.
            return self.loser_move(game)
        if self.difficulty == "easy":  # Plays randomly.
            return self.easy_move(game)
        if self.difficulty == "medium":  # Plays a winning move if possible. Otherwise blocks the opposing player's move. Otherwise it plays randomly.
            return self.medium_move(game)
        if self.difficulty == "hard":
            return self.hard_move(game)

    def user_move(self, game):
        while True:
            next_move = input("Enter the coordinates: ").split()
            if not all(value.isdigit() for value in next_move):
                print("You should enter numbers!")
                continue
            next_move = tuple(int(value) for value in next_move)
            if next_move not in game.coords_map:
                print("Coordinates should be from 1 to 3!")
                continue
            if game.cells[game.coords_map[next_move]] != "_":
                print("This cell is occupied! Choose another one!")
                continue
            return next_move 

    def loser_move(self, game):
        no_win_moves = []
        for i, symbol in enumerate(game.cells):
            if symbol == "_" and not self.check_win(game, i):
                no_win_moves.append(i)
        return random.choice([coords for coords in game.coords_map if game.coords_map[coords] in no_win_moves]) if no_win_moves else self.easy_move(game)
    
    def easy_move(self, game):
        return random.choice([coords for coords in game.coords_map if game.cells[game.coords_map[coords]] == "_"])

    def medium_move(self, game):
        for i, symbol in enumerate(game.cells):
            if symbol == "_" and self.check_win(game, i):
                return game.reverse_coords_map[i]
        other_symbol = "O" if game.next_player == "X" else "X"
        for i, symbol in enumerate(game.cells):
            if symbol == "_" and self.check_win(game, i, other_symbol):
                return game.reverse_coords_map[i]
        return self.easy_move(game)

    
    
    # def hard_move(self, game):
    #     for i, symbol in enumerate(game.cells):
    #         if symbol == "_" and self.check_win(game, i):
    #             for coords, ind in game.coords_map.items():
    #                 if ind == i:
    #                     return list(map(str, coords)) 
    #     other_symbol = "O" if game.next_player == "X" else "X"
    #     for i, symbol in enumerate(game.cells):
    #         if symbol == "_" and self.check_win(game, i, other_symbol):
    #             for coords, ind in game.coords_map.items():
    #                 if ind == i:
    #                     return list(map(str, coords)) 

    def check_win(self, game, cell_index, symbol=None):
        """Return True if placing symbol in cell_index results in a win, else return False. Symbol defaults to next_player symbol if not specified."""
        if not symbol:
            symbol = game.next_player
        cells_string = "".join(game.cells[:cell_index] + [symbol] + game.cells[cell_index + 1:])
        straights = [cells_string[:3], cells_string[3:6], cells_string[6:], cells_string[::3], cells_string[1::3], cells_string[2::3], cells_string[::4], cells_string[2:7:2]]
        return "XXX" in straights or "OOO" in straights      


def play(game, p1_diff, p2_diff):
    p1, p2 = Player(p1_diff), Player(p2_diff)    
    game.print_field()
    while True:
        game.handler(p1.request_move(game)) if game.next_player == "X" else game.handler(p2.request_move(game))
        if game.state == "exit": break


while True:
    command = input("Input command: ").split()
    if command and command[0] == "exit": break
    if len(command) == 3 and command[0] == "start" and all(word in Player.available_difficulties for word in command[1:]):
        game = TicTacToe()
        play(game, command[1], command[2])
    else:
        print("Bad parameters!")
