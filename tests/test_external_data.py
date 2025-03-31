from game.external_data import load_saved_game, overwrite_save
import os
import pytest

def test_save_and_load_game():
    data = {'whose_turn': 1,
            'players_hands': 1,
            'board_at_start': [['', ''], ['', '']],
            'tiles_bag': [1, 2, 3],
            'points': [0, 2],
            'passed_twice': 0,
            'accepted_tiles': [],
            'first_turn': True}
    try:
        os.rename('config/save.json', 'config/x.json')
    except FileNotFoundError:
        pass
    assert not os.path.exists('config/save.json')
    overwrite_save(data)
    assert os.path.exists('config/save.json')
    new_data = load_saved_game()
    assert data == new_data
    data['whose_turn'] = 0
    overwrite_save(data)
    new_data = load_saved_game()
    assert data == new_data
    os.remove('config/save.json')
    try:
        os.rename('config/x.json', 'config/save.json')
    except FileNotFoundError:
        pass
