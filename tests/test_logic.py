import copy
from game.logic import Game
from game.common_data import scoring

def test_Game_draw():
    g = Game()
    assert len(g.hand) == 7
    g.draw()
    assert len(g.hand) == 8


def test_Game_hand():
    g = Game()
    assert g.hand[0][0] in scoring.keys()
    assert g.hand == g._player_hand[0]


def test_set_hand():
    g = Game()
    g.set_hand(0, 'L₂')
    assert g.hand[0] == 'L₂'


def test_Game_swap():
    g = Game()
    g.set_hand(0, 'test')
    g.swap([0])
    assert 'test' != g.hand[0]
    assert 'test' in g.tile_bag


def test_Game_next_turn():
    g = Game()
    assert g._whose_turn == 0
    g.next_turn()
    assert g._whose_turn == 1
    g.next_turn()
    assert g._whose_turn == 0


def test_Game_scoreboard():
    g = Game()
    assert g.scoreboard() == "Player's points : 0\nBot's points : 0\n"


def test_Game_add_points():
    g = Game()
    assert g.scoreboard() == "Player's points : 0\nBot's points : 0\n"
    g.add_points(['AA'])
    assert g.scoreboard() == "Player's points : 2\nBot's points : 0\n"


def test_Game_check():
    g = Game()
    assert g.check(['QQQ', 'ALFABET']) is False
    assert g.check(['COŚ'])


def test_Game_creating_new_words_with_checking():
    g = Game()
    g._new_words = ['Ż₅U₃K₂']
    g.creating_new_words(True)
    g.next_turn()
    points = scoring['Ż'] + scoring['U'] + scoring['K']
    assert g.scoreboard() == f"Player's points : {points}\nBot's points : 0\n"
    g._new_words = ['W₁W₁W₁W₁']
    g.creating_new_words(True)
    g.next_turn()
    assert g.scoreboard() == f"Player's points : {points}\nBot's points : 0\n"


def test_Game_creating_new_words_without_checking():
    g = Game()
    g._new_words = ['Ż₅U₃K₂']
    g.creating_new_words(False)
    g.next_turn()
    points = scoring['Ż'] + scoring['U'] + scoring['K']
    assert g.scoreboard() == f"Player's points : {points}\nBot's points : 0\n"
    g._new_words = ['W₁W₁W₁W₁']
    g.creating_new_words(False)
    g.next_turn()
    points2 = 4 * int(scoring['W'])
    assert g.scoreboard() == f"Player's points : {points}\nBot's points : {points2}\n"
    g._new_words = ['W₁W₁W₁W']
    g.creating_new_words(False)
    g.next_turn()
    points += 3 * int(scoring['W'])
    assert g.scoreboard() == f"Player's points : {points}\nBot's points : {points2}\n"


def test_is_move_legal_first_false_correct_but_not_in_the_center():
    g = Game()
    assert not g.is_move_legal()
    g.set_board((3, 3), 'Ż₅')
    g.append_new_on_board((3, 3))
    assert not g.is_move_legal()
    g.set_board((4, 3), 'U₃')
    g.append_new_on_board((4, 3))
    assert not g.is_move_legal()
    g.set_board((5, 3), 'K₂')
    g.append_new_on_board((5, 3))
    assert not g.is_move_legal()


def test_is_move_legal_first_false_single_in_the_center():
    g = Game()
    g.set_board((7, 7), 'W₁')
    g.append_new_on_board((7, 7))
    assert not g.is_move_legal()


def test_is_move_legal_first_true():
    g = Game()
    g.set_board((7, 7), 'W₁')
    g.append_new_on_board((7, 7))
    g.set_board((7, 8), 'W₁')
    g.append_new_on_board((7, 8))
    assert g.is_move_legal()
    g.set_board((7, 6), 'W₁')
    g.append_new_on_board((7, 6))
    assert g.is_move_legal()


def test_is_move_legal_typical_false():
    g = Game()
    g.set_board((6, 7), 'L₂')
    g.append_new_on_board((6, 7))
    g.set_board((7, 7), 'I')
    g.append_new_on_board((7, 7))
    g.set_board((8, 7), 'Ś₅')
    g.append_new_on_board((8, 7))
    g.set_board((9, 7), 'Ć₆')
    g.append_new_on_board((9, 7))
    g.next_turn()
    g._first_turn = False
    assert not g.is_move_legal()
    g.set_board((6, 9), 'N₁')
    g.append_new_on_board((6, 9))
    assert not g.is_move_legal()
    g.set_board((7, 9), 'A₁')
    g.append_new_on_board((7, 9))
    assert not g.is_move_legal()
    g.set_board((6, 8), 'I₁')
    g.append_new_on_board((6, 8))
    assert not g.is_move_legal()


def test_is_move_legal_typical_true():
    g = Game()
    g.set_board((7, 7), 'I₁')
    g.set_board((6, 7), 'M')
    g._first_turn = False
    g.set_board((7, 6), 'K₂')
    g.append_new_on_board((7, 6))
    assert g.is_move_legal()
    g.set_board((7, 5), 'U₃')
    g.append_new_on_board((7, 5))
    assert g.is_move_legal()
    g.set_board((7, 4), 'Ż₅')
    g.append_new_on_board((7, 4))
    assert g.is_move_legal()
    g.next_turn()
    g.set_board((6, 6), 'I₁')
    g.append_new_on_board((6, 6))
    assert g.is_move_legal()


def test_tiles_to_words_linear():
    g = Game()
    g.set_board((7, 7), 'W₁')
    g.append_new_on_board((7, 7))
    g.set_board((7, 8), 'W₁')
    g.append_new_on_board((7, 8))
    g.set_board((7, 6), 'W₁')
    g.append_new_on_board((7, 6))
    g.tiles_to_words()
    assert g._new_words == ['W₁W₁W₁']


def test_tiles_to_words_crossed():
    g = Game()
    g.set_board((7, 7), 'W₁')
    g.append_new_on_board((7, 7))
    g.set_board((7, 8), 'W₁')
    g.append_new_on_board((7, 8))
    g.set_board((7, 6), 'W₁')
    g.append_new_on_board((7, 6))
    g.tiles_to_words()
    g.next_turn()
    g.set_board((8, 7), 'I₁')
    g.append_new_on_board((8, 7))
    g.set_board((9, 7), 'D₂')
    g.append_new_on_board((9, 7))
    g.set_board((10, 7), 'Z₁')
    g.append_new_on_board((10, 7))
    g.tiles_to_words()
    assert g._new_words == ['W₁I₁D₂Z₁']
    g.next_turn()
    g.set_board((8, 6), 'U₃')
    g.append_new_on_board((8, 6))
    g.tiles_to_words()
    assert g._new_words == ['W₁U₃', 'U₃I₁'] or g._new_words == ['U₃I₁', 'W₁U₃']


def test_fulfil_hand():
    g = Game()
    g.set_hand(0, '')
    g.set_hand(3, '')
    tile_bag_len = len(g._tile_bag)
    g.fulfil_hand()
    assert g.hand[0] != ''
    assert g.hand[3] != ''
    assert tile_bag_len - 2 == len(g._tile_bag)


def test_passed():
    g = Game()
    assert g._passed_twice == 0
    g.passed()
    g.next_turn()
    assert g._passed_twice == 1
    g.passed()
    g.next_turn()
    assert g._passed_twice == 2
    g.swap([0, 1])
    g.next_turn()
    assert g._passed_twice == 0
    g.passed()
    g.next_turn()
    assert g._passed_twice == 1
    g.set_board((6, 7), 'L₂')
    g.append_new_on_board((6, 7))
    g.set_board((7, 7), 'I')
    g.append_new_on_board((7, 7))
    g.set_board((8, 7), 'Ś₅')
    g.append_new_on_board((8, 7))
    g.set_board((9, 7), 'Ć₆')
    g.append_new_on_board((9, 7))
    g.tiles_to_words()
    g.creating_new_words(True)
    g.next_turn()
    assert g._passed_twice == 0


def test_bots_decision_first_turn():
    g = Game()
    g._player_hand[1] = ['T₂', 'L₂', 'A₁', 'M₂', 'A₁', 'Ą₅', 'T₂', 'B₃']
    g.passed()
    g.next_turn()
    g.bots_decision()
    # TABATĄ
    assert [row[7] for row in g.board[6:12]] == ['T₂','A₁','B₃','A₁','T₂','Ą₅']
    assert g._players_points[1] == 14


def test_bots_decision_exchange():
    g = Game()
    g._player_hand[1] = ['T₂', ' ', 'A₁', ' ', 'Ó₅', 'Ą₅', 'T₂', 'B₃']
    g.passed()
    g.next_turn()
    g.bots_decision()
    assert g._players_points[1] == 0
    assert g._player_hand[1][1] != ' '
    assert g.whoese_turn == 0


def test_end_of_the_game_False():
    g = Game()
    assert not g.end_of_the_game()
    g.passed()
    assert not g.end_of_the_game()
    g._tile_bag = []
    assert not g.end_of_the_game()


def test_end_of_the_game_True_passed_twice():
    g = Game()
    g.passed()
    points1 = 0
    for tile in g.hand:
        if tile[0] in scoring.keys():
            points1 += scoring[tile[0]]
    g.next_turn()
    g.passed()
    points2 = 0
    for tile in g.hand:
        if tile[0] in scoring.keys():
            points2 += scoring[tile[0]]
    g.passed()
    g.passed()
    assert g.end_of_the_game()
    g._whose_turn = 0
    assert g.my_points() == -points1
    g.next_turn()
    assert g.my_points() == -points2


def test_end_of_the_game_True_no_more_tiles():
    g = Game()
    points1 = 0
    for tile in g.hand:
        if tile[0] in scoring.keys():
            points1 += scoring[tile[0]]
    g.next_turn()
    for i in range(7):
        g.set_hand(i, '')
    g._tile_bag = []
    assert g.end_of_the_game()
    g._whose_turn = 0
    assert g.my_points() == -points1
    g.next_turn()
    assert g.my_points() == points1
