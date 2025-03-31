full_tile_bag = ['A₁', 'A₁', 'A₁', 'A₁', 'A₁', 'A₁', 'A₁', 'A₁', 'A₁', 'Ą₅',
                 'B₃', 'B₃', 'C₂', 'C₂', 'C₂', 'Ć₆', 'D₂', 'D₂', 'D₂', 'E₁',
                 'E₁', 'E₁', 'E₁', 'E₁', 'E₁', 'E₁', 'Ę₅', 'F₅', 'G₃', 'G₃',
                 'H₃', 'H₃', 'I₁', 'I₁', 'I₁', 'I₁', 'I₁', 'I₁', 'I₁', 'I₁',
                 'J₃', 'J₃', 'K₂', 'K₂', 'K₂', 'L₂', 'L₂', 'L₂', 'Ł₃', 'Ł₃',
                 'M₂', 'M₂', 'M₂', 'N₁', 'N₁', 'N₁', 'N₁', 'N₁', 'Ń₇', 'O₁',
                 'O₁', 'O₁', 'O₁', 'O₁', 'O₁', 'Ó₅', 'P₂', 'P₂', 'P₂', 'R₁',
                 'R₁', 'R₁', 'R₁', 'S₁', 'S₁', 'S₁', 'S₁', 'Ś₅', 'T₂', 'T₂',
                 'T₂', 'U₃', 'U₃', 'W₁', 'W₁', 'W₁', 'W₁', 'Y₂', 'Y₂', 'Y₂',
                 'Y₂', 'Z₁', 'Z₁', 'Z₁', 'Z₁', 'Z₁', 'Ź₉', 'Ż₅', ' ', ' ']
scoring = {
                ' ': 0, "A": 1, "E": 1, "I": 1, "N": 1,
                "O": 1, "R": 1, "S": 1, "W": 1, "Z": 1,
                "C": 2, "D": 2, "K": 2, "L": 2, "M": 2,
                "P": 2, "T": 2, "Y": 2, "B": 3, "G": 3,
                "H": 3, "J": 3, "Ł": 3, "U": 3, "Ą": 5,
                "Ę": 5, "F": 5, "Ó": 5, "Ś": 5, "Ż": 5,
                "Ć": 6, "Ń": 7, "Ź": 9
                }


def find_start(board, where, horizontal) -> int:
    if horizontal:
        word_start = where[1]
        while word_start > 0 and board[where[0]][word_start - 1] != "":
            word_start -= 1
    else:
        word_start = where[0]
        while word_start > 0 and board[word_start - 1][where[1]] != "":
            word_start -= 1
    return word_start


def word_in_line(board, where, horizontal) -> str:
    word = ""
    if horizontal:
        y = where[1]
        while y < 15 and board[where[0]][y] != "":
            word += board[where[0]][y]
            y += 1
    else:
        x = where[0]
        while x < 15 and board[x][where[1]] != "":
            word += board[x][where[1]]
            x += 1
    return word


def format_to_checknscoring(new_word: str):
    word_checking = ""
    word_scoring = ""
    for char_id in range(len(new_word)):
        if new_word[char_id] in scoring.keys():
            word_checking += new_word[char_id]
            if (
                char_id + 1 < len(new_word)
                and new_word[char_id + 1] not in scoring.keys()
            ):
                word_scoring += new_word[char_id]
    return (word_checking, word_scoring)


def format_to_checknscoring_partly(new_word: str, lenght: int):
    word_checking = ""
    word_scoring = ""
    for char_id in range(len(new_word)):
        if new_word[char_id] in scoring.keys():
            word_checking += new_word[char_id]
            if (
                char_id + 1 < len(new_word)
                and new_word[char_id + 1] not in scoring.keys()
            ):
                word_scoring += new_word[char_id]
        if len(word_checking) >= lenght:
            break
    return (word_checking, word_scoring)


def words_to_points(words):
    points = 0
    for word in words:
        for char in word:
            points += scoring[char]
    return points
