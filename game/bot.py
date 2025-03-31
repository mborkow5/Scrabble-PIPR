from functools import lru_cache
import string
import datrie
from .common_data import (
    format_to_checknscoring,
    words_to_points,
    format_to_checknscoring_partly,
)
import copy
from itertools import permutations
from multiprocessing import Pool, Manager
import os


class Bot:
    def __init__(self):
        try:
            self._trie = datrie.Trie.load("config/words.trie")
        except FileNotFoundError:
            self.reconfigure_bots_wordlist()

    def reconfigure_bots_wordlist(self):
        alphabet = string.ascii_lowercase + "ąćęłńóśźż"
        self._trie = datrie.Trie(alphabet)
        with open("config/words.txt") as f:
            for line in f:
                self._trie[line.strip()] = True
        self._trie.save("config/words.trie")

    def check_word(self, word):
        if self._trie.get(word):  # None->False
            return True
        return False

    def exchange_duplicates(self, hand):
        to_exchange = []
        for tile_id in range(len(hand)):
            if (hand[tile_id] != "" and hand[tile_id] in hand[tile_id + 1 : 7]) or hand[
                tile_id
            ] == " ":
                to_exchange.append(tile_id)
        return to_exchange

    def can_tile_be_placed_here(self, board, x, y):
        if board[x][y]:
            return False
        if x > 0 and board[x - 1][y]:
            return True
        if x < 14 and board[x + 1][y]:
            return True
        if y > 0 and board[x][y - 1]:
            return True
        if y < 14 and board[x][y + 1]:
            return True
        return False

    def check_word_in_row(self, board, tile, row, column):
        word = tile
        for i in range(column - 1, -1, -1):
            if board[row][i]:
                word = board[row][i] + word
            else:
                break
        for i in range(column + 1, 15):
            if board[row][i]:
                word = word + board[row][i]
            else:
                break
        formatted = format_to_checknscoring(word)
        if len(formatted[0]) == 1:
            return 0
        if self.check_word(formatted[0]):
            return words_to_points(formatted[1])
        return -1

    def check_word_in_column(self, board, tile, row, column):
        word = tile
        for i in range(row - 1, -1, -1):
            if board[i][column]:
                word = board[i][column] + word
            else:
                break
        for i in range(row + 1, 15):
            if board[i][column]:
                word = word + board[i][column]
            else:
                break
        formatted = format_to_checknscoring(word)
        if len(formatted[0]) == 1:
            return 0
        if self.check_word(formatted[0]):
            return words_to_points(formatted[1])
        return -1

    def exploration(self, board, hand, i):
        row = self.best_word_in_row(board, hand, i)
        column = self.best_word_in_column(board, hand, i)
        if row[0] > column[0]:
            return row
        else:
            return column

    @lru_cache
    def best_word_in_row(self, board, hand, row):
        possible_places = [
            self.can_tile_be_placed_here(board, row, i) for i in range(0, 15)
        ]
        best_move = [0, None, None]
        if not any(possible_places):
            return best_move
        for combination in list(permutations(hand, 7)):
            word = ""
            prefix_len = 0
            for i in range(0, 15):
                m = [[copy.copy(prefix_len) + 1]]
                min_word_len = 1
                while (
                    min_word_len < 8
                    and i + min_word_len < 15
                    and not possible_places[i + min_word_len - 1]
                ):
                    min_word_len += 1
                if min_word_len != 8 and i + min_word_len < 15:
                    if board[row][i]:
                        word = word + board[row][i]
                        prefix_len += 1
                    else:
                        points = 0
                        tile_id = 0
                        j = 0
                        while tile_id < 7 and i + j < 15:
                            if board[row][i + j]:
                                word = word + board[row][i + j]
                                j += 1
                                if m[-1][-1] == prefix_len + j - 1:
                                    m[-1][-1] = prefix_len + j
                                else:
                                    m.append([prefix_len + j, prefix_len + j])
                            else:
                                column_check = self.check_word_in_column(
                                    board, combination[tile_id], row, i + j
                                )
                                if column_check >= 0:
                                    points += column_check
                                    word = word + combination[tile_id]
                                    tile_id += 1
                                    j += 1
                                else:
                                    break
                        while i + j < 15 and board[row][i + j]:
                            word = word + board[row][i + j]
                            j += 1
                            if m[-1][-1] == prefix_len + j - 1:
                                m[-1][-1] = prefix_len + j
                            else:
                                m.append([prefix_len + j, prefix_len + j])
                        m.append([15])
                        formatted = format_to_checknscoring(word)
                        words = self._trie.prefixes(formatted[0].lower())
                        if words:
                            for w in reversed(words):
                                npoints = copy.copy(points)
                                for k in range(len(m) - 1):
                                    if (
                                        m[k][-1] <= len(w) < m[k + 1][0]
                                        and len(w) > min_word_len
                                    ):
                                        new_word = format_to_checknscoring_partly(
                                            word, len(w)
                                        )
                                        npoints += words_to_points(new_word[1])
                                        if npoints > best_move[0]:
                                            best_move[0] = npoints
                                            best_move[1] = [
                                                len(w) - prefix_len,
                                                copy.copy(i),
                                                copy.copy(row),
                                                True,
                                            ]
                                            best_move[2] = list(combination[:])
                                            break
                        prefix_len = 0
                        word = ""
        return best_move

    @lru_cache
    def best_word_in_column(self, board, hand, column):
        possible_places = [
            self.can_tile_be_placed_here(board, i, column) for i in range(0, 15)
        ]
        best_move = [0, None, None]
        if not any(possible_places):
            return best_move
        for combination in list(permutations(hand, 7)):
            word = ""
            prefix_len = 0
            for i in range(0, 15):
                m = [[copy.copy(prefix_len) + 1]]
                min_word_len = 1
                while (
                    min_word_len < 8
                    and i + min_word_len < 15
                    and not possible_places[i + min_word_len - 1]
                ):
                    min_word_len += 1
                if min_word_len != 8 and i + min_word_len < 15:
                    if board[i][column]:
                        word = word + board[i][column]
                        prefix_len += 1
                    else:
                        points = 0
                        tile_id = 0
                        j = 0
                        while tile_id < 7 and i + j < 15:
                            if board[i + j][column]:
                                word = word + board[i + j][column]
                                j += 1
                                if m[-1][-1] == prefix_len + j - 1:
                                    m[-1][-1] = prefix_len + j
                                else:
                                    m.append([prefix_len + j - 1, prefix_len + j])
                            else:
                                row_check = self.check_word_in_row(
                                    board, combination[tile_id], i + j, column
                                )
                                if row_check >= 0:
                                    points += row_check
                                    word = word + combination[tile_id]
                                    tile_id += 1
                                    j += 1
                                else:
                                    break
                        while i + j < 15 and board[i + j][column]:
                            word = word + board[i + j][column]
                            j += 1
                            if m[-1][-1] == prefix_len + j - 1:
                                m[-1][-1] = prefix_len + j
                            else:
                                m.append([prefix_len + j, prefix_len + j])
                        m.append([15])
                        formatted = format_to_checknscoring(word)
                        words = self._trie.prefixes(formatted[0].lower())
                        if words:
                            for w in reversed(words):
                                npoints = copy.copy(points)
                                for k in range(len(m) - 1):
                                    if (
                                        m[k][-1] <= len(w) < m[k + 1][0]
                                        and len(w) > min_word_len
                                    ):
                                        new_word = format_to_checknscoring_partly(
                                            word, len(w)
                                        )
                                        npoints += words_to_points(new_word[1])
                                        if npoints > best_move[0]:
                                            best_move[0] = npoints
                                            best_move[1] = [
                                                len(w) - prefix_len,
                                                copy.copy(column),
                                                copy.copy(i),
                                                False,
                                            ]
                                            best_move[2] = list(combination[:])
                                            break
                        prefix_len = 0
                        word = ""
        return best_move

    def bots_turn(self, oboard, accepted_tiles, hand, first_turn):
        board = copy.deepcopy(oboard)
        if " " in hand:
            return [self.exchange_duplicates(hand)]
        else:
            best_move = [0, None, None]
            best_combination = None
            best_word = None
            if first_turn:
                for combination in list(permutations(hand, 7)):
                    combination = "".join(combination)
                    words = self._trie.prefixes(
                        format_to_checknscoring(combination)[0].lower()
                    )

                    if words:
                        points = words_to_points(words[-1].upper())
                        if points > best_move[0]:
                            best_move[0], best_word, best_combination = (
                                points,
                                words[-1],
                                combination,
                            )
                if best_move[0] > 0:
                    best_move[1] = copy.deepcopy(board)
                    best_move[2] = [
                        best_combination[i : i + 2]
                        for i in range(0, len(best_combination), 2)
                    ]
                    for i in range(len(best_word)):

                        best_move[1][6 + i][7] = best_move[2][i]
                        best_move[2][i] = ""
                    return best_move
                return [self.exchange_duplicates(hand)]

            ids = [i for i in range(15)]
            with Manager() as manager:
                results = manager.list()
                with Pool(processes=os.cpu_count() - 1) as pool:
                    board_tuple = tuple(tuple(row) for row in board)

                    results = pool.starmap(
                        self.exploration, [(board_tuple, tuple(hand), i) for i in ids]
                    )
                for r in results:
                    if r[0] > best_move[0]:
                        best_move = r if best_move[0] < r[0] else best_move
                    best_move = r if best_move[0] < r[0] else best_move
            if best_move[0] == 0:
                return [self.exchange_duplicates(hand)]
            j = 0
            column = best_move[1][1]
            row = best_move[1][2]
            if best_move[1][3]:
                while j < best_move[1][0]:
                    if not board[row][column + j]:
                        board[row][column + j] = best_move[2].pop(0)
                        best_move[2].append("")
                    j += 1
            else:
                while j < best_move[1][0]:
                    if not board[row + j][column]:
                        board[row + j][column] = best_move[2].pop(0)
                        best_move[2].append("")
                    j += 1
            best_move[1] = board
            return best_move
