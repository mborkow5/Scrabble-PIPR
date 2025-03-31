from game.common_data import find_start, word_in_line
from game.common_data import words_to_points, format_to_checknscoring


def test_find_start():
    board = [['' for j in range(4)] for i in range(4)]
    board[1][0] = 'A'
    board[2][0] = 'B'
    assert find_start(board, (2, 0), False) == 1


def test_word_in_line():
    board = [['' for j in range(4)] for i in range(4)]
    board[1][0] = 'A'
    board[2][0] = 'B'
    assert word_in_line(board, (1, 0), False) == 'AB'


def test_format_to_checknscoring():
    word = 'Ż₅UK₂'
    assert format_to_checknscoring(word)[0] == 'ŻUK'
    assert format_to_checknscoring(word)[1] == 'ŻK'


def test_words_to_points():
    word_for_scoring = 'ŻUK'
    assert words_to_points(word_for_scoring) == 10
