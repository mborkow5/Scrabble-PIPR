import random
from .common_data import full_tile_bag, find_start, word_in_line
from .common_data import format_to_checknscoring, words_to_points
from .external_data import overwrite_save, load_saved_game
from .bot import *


class Game:
    """
    Game class has all the informations about the state of the
    game(whose turn is now, board state, tiles in bag and on players,
    racks, points and created words). Its methods allow to make any
    legal move according to scrabble rules, comunicate with dictionary,
    bot and to save and load the game
    """

    def __init__(self, players: int = 2):
        self._players = players
        self._players_points = []
        self._tile_bag = full_tile_bag.copy()
        random.shuffle(self._tile_bag)
        self._player_hand = [[], [], [], []]
        for player_id in range(players):
            self._whose_turn = player_id
            self._players_points.append(0)
            for tiles_to_draw in range(7):
                self.draw()
        self._whose_turn = 0
        self._board = [["" for j in range(15)] for i in range(15)]
        self._first_turn = True
        self._new_on_board = []
        self._accepted_tiles = []
        self._passed_twice = 0
        self._new_created_words = []
        self.b = Bot()

    def save(self):
        board_at_start = self._board
        for not_accepted_tiles in self._new_on_board:
            board_at_start[not_accepted_tiles[0]][not_accepted_tiles[1]] = ""
        data = {
            "players_hands": self._player_hand,
            "board_at_start": board_at_start,
            "tiles_bag": self._tile_bag,
            "points": self._players_points,
            "passed_twice": self._passed_twice,
            "accepted_tiles": self._accepted_tiles,
            "first_turn": self._first_turn,
        }
        overwrite_save(data)

    def load(self):
        data = load_saved_game()
        self._whose_turn = 0
        self._player_hand = data["players_hands"]
        self._board = data["board_at_start"]
        self._tile_bag = data["tiles_bag"]
        self._players_points = data["points"]
        self._passed_twice = data["passed_twice"]
        lists = data["accepted_tiles"]
        self._first_turn = data["first_turn"]
        self._accepted_tiles = []

        for list in lists:
            self._accepted_tiles.append(tuple(list))

    @property
    def new_on_board(self):
        return self._new_on_board

    def append_new_on_board(self, tile):
        self._new_on_board.append(tile)

    def remove_new_on_board(self, tile):
        self._new_on_board.remove(tile)

    def clear_new_on_board(self):
        self._new_on_board = []

    @property
    def board(self):
        return self._board

    def set_board(self, place_on_board, tile: str):
        self._board[place_on_board[0]][place_on_board[1]] = tile

    @property
    def tile_bag(self):
        return self._tile_bag

    @property
    def accepted_tiles(self):
        return self._accepted_tiles

    def next_turn(self):
        for accepted_tile in self._new_on_board:
            self._accepted_tiles.append(accepted_tile)
        self.fulfil_hand()
        self._new_on_board = []
        self._whose_turn = (self._whose_turn + 1) % self._players

    def bots_decision(self):
        """
        returns if the game ended during bots turn
        decision variable format:
        word found: [int(=points if not first_turn), [[str]] boardafter move, [str] hand after move]
        exchange: [[int] id of tile in hand to exchange]
        pass: [0, None, None]
        ^according to it the atributes are being changed
        """
        if self._whose_turn == 1:
            decision = self.b.bots_turn(
                self.board, self.accepted_tiles, self.hand, self._first_turn
            )
            if len(decision) == 1 and len(self.tile_bag) >= len(decision[0]):
                self.swap(decision[0])
            elif len(decision) == 3 and decision[1] is not None:
                for i in range(15):
                    for j in range(15):
                        if self.board[i][j] != decision[1][i][j]:
                            self.append_new_on_board((i, j))
                            self.set_board((i, j), decision[1][i][j])
                for tile in enumerate(decision[2]):
                    self.set_hand(tile[0], tile[1])
                self.tiles_to_words()
                self.creating_new_words(False)
                self.fulfil_hand()
                if self.end_of_the_game():
                    return True
            else:
                self.passed()
                if self.end_of_the_game():
                    return True
            self.next_turn()
            return False

    def scoreboard(self) -> str:
        output = f"Player's points : {self._players_points[0]}\n"
        output += f"Bot's points : {self._players_points[1]}\n"
        return output

    def add_points(self, words) -> None:
        self._players_points[self._whose_turn] += words_to_points(words)

    def creating_new_words(self, anyone_checks: bool):
        self._passed_twice = 0
        words_for_checking = []
        words_for_scoring = []
        for new_word in self._new_words:
            formated = format_to_checknscoring(new_word)
            words_for_checking.append(formated[0])
            words_for_scoring.append(formated[1])
        if not anyone_checks or self.check(words_for_checking):
            self._new_created_words.extend(words_for_checking)
            self.add_points(words_for_scoring)
            self._first_turn = False

    def check(self, words):
        for word in words:
            if not self.b.check_word(word.lower()):
                return False
        return True

    def is_move_legal(self) -> bool:
        if len(self._new_on_board) == 0:
            return False
        x = [tile_place[0] for tile_place in self._new_on_board]
        y = [tile_place[1] for tile_place in self._new_on_board]
        if min(x) == max(x):
            for tiles_between in range(min(y), max(y) + 1):
                if (
                    self._board[min(x)][tiles_between] == ""
                    or self._board[min(x)][tiles_between] == " "
                ):
                    return False
            if self._first_turn:
                if len(self._new_on_board) == 1:
                    return False
                return self._board[7][7] != ""
            else:
                if min(y) > 0:
                    if self._board[min(x)][min(y) - 1] != "":
                        return True
                if max(y) < 14:
                    if self._board[min(x)][max(y) + 1] != "":
                        return True
                for tiles_connected in range(min(y), max(y) + 1):
                    t = tiles_connected
                    for i in range(-(min(x) > 0), 1 + (max(x) < 14)):
                        if (
                            self._board[min(x) + i][t] != ""
                            and (min(x) + i, t) not in self._new_on_board
                        ):
                            return True

        elif min(y) == max(y):
            for tiles_between in range(min(x), max(x) + 1):
                if (
                    self._board[tiles_between][min(y)] == ""
                    or self._board[tiles_between][min(y)] == " "
                ):
                    return False
            if self._first_turn:
                if len(self._new_on_board) <= 1:
                    return False
                return self._board[7][7] != ""
            else:
                if min(x) > 0:
                    if self._board[min(x) - 1][min(y)] != "":
                        return True
                if max(x) < 14:
                    if self._board[max(x) + 1][min(y)] != "":
                        return True
                for tiles_connected in range(min(x), max(x) + 1):
                    t = tiles_connected
                    for i in range(-(min(y) > 0), 1 + (max(y) < 14)):
                        if (
                            self._board[t][min(y) + i] != ""
                            and (t, min(y) + i) not in self._new_on_board
                        ):
                            return True
        return False

    def tiles_to_words(self):
        """
        'new_words' format is 'Ż₅UK₂' - not prepared to check or change score
        """
        x = [tile_place[0] for tile_place in self._new_on_board]
        y = [tile_place[1] for tile_place in self._new_on_board]
        self._new_words = []
        word = ""
        if min(x) == max(x):
            word_start = find_start(self._board, (min(x), min(y)), True)
            word = word_in_line(self._board, (min(x), word_start), True)
            if len(word) > 2:
                self._new_words.append(word)
            word = ""
            for line in y:
                word_start = find_start(self._board, (min(x), line), False)
                word = word_in_line(self._board, (word_start, line), False)
                if len(word) > 2:
                    self._new_words.append(word)
                word = ""
        else:
            word_start = find_start(self._board, (min(x), min(y)), False)
            word = word_in_line(self._board, (word_start, min(y)), False)
            if len(word) > 2:
                self._new_words.append(word)
            word = ""
            for line in x:
                word_start = find_start(self._board, (line, min(y)), True)
                word = word_in_line(self._board, (line, word_start), True)
                if len(word) > 2:
                    self._new_words.append(word)
                word = ""

    @property
    def hand(self):
        return self._player_hand[self._whose_turn]

    @property
    def whoese_turn(self):
        return self._whose_turn

    def set_hand(self, id, tile):
        self._player_hand[self._whose_turn][id] = tile

    def my_points(self):
        return self._players_points[self._whose_turn]

    def fulfil_hand(self):
        for tile_id in range(len(self.hand)):
            if self.hand[tile_id] == "" and len(self._tile_bag) > 0:
                self.draw()
                self.set_hand(tile_id, self._player_hand[self._whose_turn][7])
                self._player_hand[self._whose_turn].pop()

    def draw(self) -> None:
        self._player_hand[self._whose_turn].append(self._tile_bag.pop())

    def passed(self):
        self._passed_twice += 1

    def swap(self, selected_tiles_id) -> None:
        """selected_tiles = id of objects chosen to swap"""
        self._passed_twice = 0
        to_tile_bag = []
        for selected_tile_id in selected_tiles_id:
            to_tile_bag.append(None)
            wh = self._whose_turn
            st = selected_tile_id
            to_tile_bag[-1], self._player_hand[wh][st] = (
                self._player_hand[wh][st],
                self._tile_bag[-1],
            )
            self._tile_bag.pop()
        for a_tile in to_tile_bag:
            self._tile_bag.append(a_tile)
        random.shuffle(self._tile_bag)

    def end_of_the_game(self):
        empty_rack = True
        for tile in self.hand:
            if tile != "":
                empty_rack = False
        if self._passed_twice >= 2 * self._players or (
            not self._tile_bag and empty_rack
        ):
            has_no_tiles = None
            all_tiles_left = ""
            for player_id in range(self._players):
                tiles_left = ""
                for tile in self.hand:
                    tiles_left += tile
                if tiles_left == "":
                    has_no_tiles = self._whose_turn
                all_tiles_left += tiles_left
                self._new_words = [tiles_left]
                points = self.my_points()
                self.creating_new_words(False)
                self._players_points[self._whose_turn] = 2 * points - self.my_points()
                self.next_turn()
            if has_no_tiles:
                self._whose_turn = has_no_tiles
                self._new_words = [all_tiles_left]
                self.creating_new_words(False)
            return True
        return False
