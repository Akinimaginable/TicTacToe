from pygame import display, event, KEYDOWN, K_RETURN, K_SPACE, QUIT, mouse, MOUSEBUTTONDOWN, draw
from random import choice
from constants import *


class AI:
    def __init__(self, num: int):
        self.board: list = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.branch: list = []
        self.num: int = num
        self.probabilities: list = [[] for _ in range(9)]
        self.tree: list = [[] for _ in range(9)]

    def set_board(self, board: list) -> None:
        self.board = board

    def set_num(self, num: int) -> None:
        self.num = num

    def move_prediction(self, turn: int, board: list, nb_turn: int) -> None:
        """
        predict all possible plays and save the winning one
        """
        if winner(board)[0]:
            if turn == self.num:  # Next turn
                self.branch.append(-1 / (nb_turn ** 3))
            else:
                self.branch.append(1 / (nb_turn ** 3))
        elif is_board_full(board):
            self.branch.append(0)
        else:
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        next_turn = 1 if turn == -1 else -1
                        next_board = [[k for k in row] for row in board]
                        next_board[i][j] = turn
                        self.move_prediction(next_turn, next_board, nb_turn + 1)

    def first_move(self, turn: int) -> None:
        """
        1) predict all winning plays depending on the first play
        2) fill the tree with all winning plays
        """
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    next_turn = 1 if turn == -1 else -1
                    next_board = [[k for k in row] for row in self.board]
                    next_board[i][j] = turn
                    self.move_prediction(next_turn, next_board, 1)
                    self.tree[i * 3 + j] = self.branch
                    self.branch = []

    def proba(self) -> None:
        """
        calculates all the winning probabilities
        """
        for i in range(len(self.tree)):
            total = 0
            nb = len(self.tree[i])
            for j in self.tree[i]:
                total += j
            if nb:
                self.probabilities[i] = total / nb

    def best_move(self) -> int:
        """
        plays depending on the highest probabilities
        """
        maxi = -1  # -1 is the min
        best_move = -1  # if board is full: no position

        for i in range(len(self.probabilities)):
            if self.probabilities[i] != []:
                if self.probabilities[i] >= maxi:
                    maxi = self.probabilities[i]
                    best_move = i

        return best_move

    def move(self) -> int:
        """
        call the others functions and reset needed values
        """
        self.first_move(self.num)
        self.proba()
        best = self.best_move()
        self.tree = [[] for _ in range(9)]
        self.probabilities = [[] for _ in range(9)]
        return best


def check_winner() -> None:
    """
    1) check if the winning condition is complete and redraw the form in red so highlight the line
    2) set ended to true if someone won
    """
    global ended
    result = winner(d)
    if result[0]:
        positions = result[1]
        for p in positions:
            x, y = p
            put_cross(x + 1, y + 1, RED) if turn % 2 == 0 else put_circle(x + 1, y + 1, RED)
        ended = True


def init() -> tuple:
    """
    1) draw a new board and set default vars
    2) return the first player
    """
    global d, ended, turn
    player = choice(((0, 1), (1, 0)))
    game.fill((255, 255, 255))
    d = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    turn, ended = 0, False

    draw.lines(game, BLACK, False, ((CASE, 0), (CASE, WIN)), WEIGHT - 3)
    draw.lines(game, BLACK, False, ((win15, 0), (win15, WIN)), WEIGHT - 3)
    draw.lines(game, BLACK, False, ((0, CASE), (WIN, CASE)), WEIGHT - 3)
    draw.lines(game, BLACK, False, ((0, win15), (WIN, win15)), WEIGHT - 3)
    display.update()

    return player


def is_board_full(game_data: list) -> bool:
    """
    check if the board is full or not
    """
    if 0 in game_data[0] or 0 in game_data[1] or 0 in game_data[2]:
        return False

    return True


def put_circle(x: int, y: int, color: tuple) -> None:
    """
    1) add the circle in the game data
    2) draws a circle at defined coordinates
    """
    d[y - 1][x - 1] = 1
    draw.circle(game, color, (x * CASE - 50, y * CASE - 50), CASE // 3, WEIGHT - 1)


def put_cross(x: int, y: int, color: tuple) -> None:
    """
    1) add the cross in the game data
    2) draws a cross at defined coordinates
    """
    d[y - 1][x - 1] = -1
    x, y = x * CASE - 50, y * CASE - 50
    draw.lines(
        game,
        color,
        False,
        (
            (x - 35, y - 35),
            (x + 35, y + 35),
            (x, y),
            (x + 35, y - 35),
            (x - 35, y + 35),
        ),
        WEIGHT
    )


def winner(game_data):
    """
    check if the winning condition is complete and return the coordinates
    """
    for x1 in range(3):
        sum_x, sum_y = 0, 0
        for y1 in range(3):
            sum_x += game_data[x1][y1]
            sum_y += game_data[y1][x1]
        if sum_x == 3:
            return 1, ((0, x1), (1, x1), (2, x1))
        elif sum_x == -3:
            return -1, ((0, x1), (1, x1), (2, x1))
        elif sum_y == 3:
            return 1, ((x1, 0), (x1, 1), (x1, 2))
        elif sum_y == -3:
            return -1, ((x1, 0), (x1, 1), (x1, 2))

    d1 = game_data[0][0] + game_data[1][1] + game_data[2][2]
    d2 = game_data[0][2] + game_data[1][1] + game_data[2][0]
    if d1 == 3:
        return 1, ((0, 0), (1, 1), (2, 2))
    elif d1 == -3:
        return -1, ((0, 0), (1, 1), (2, 2))
    elif d2 == 3:
        return 1, ((0, 2), (1, 1), (2, 0))
    elif d2 == -3:
        return -1, ((0, 2), (1, 1), (2, 0))

    return None, ()


def main() -> None:
    global ended, turn
    display.set_caption("Tic tac toe v1.3")
    player = init()
    bot = AI(-1) if player[0] == 0 else AI(1)

    while True:  # Main loop
        event_handler = event.wait()
        if event_handler.type == QUIT:
            break

        # Clear and recreate the board
        if event_handler.type == KEYDOWN and event_handler.key in (
                K_SPACE,
                K_RETURN,
        ):
            player = init()
            bot.set_num(-1) if player[0] == 0 else bot.set_num(1)

        if not ended and turn < 9 and turn % 2 == player[0]:
            bot.set_board(d)
            m = bot.move()
            i = m // 3
            j = m % 3
            d[i][j] = 1
            put_circle(j + 1, i + 1, GREEN) if turn % 2 == 1 else put_cross(j + 1, i + 1, BLUE)
            check_winner()
            display.update()
            turn += 1

        if (
                event_handler.type == MOUSEBUTTONDOWN
                and mouse.get_pressed() == (1, 0, 0)
                and not ended
                and turn < 9
                and turn % 2 == player[1]
        ):
            get_case = mouse.get_pos()
            x, y = (get_case[0] + CASE) // CASE, (get_case[1] + CASE) // CASE

            if not d[y - 1][x - 1]:
                put_circle(x, y, GREEN) if turn % 2 == 1 else put_cross(x, y, BLUE)
                check_winner()
                display.update()
                turn += 1

    quit()


if __name__ == "__main__":
    game = display.set_mode((WIN, WIN), vsync=1)  # Add VSync to reduce CPU usage
    main()
