import pytest
import main


@pytest.mark.parametrize(
    "board_state,expected",
    [
        ([0, 0, 0, 0, 0, 0, 0, 0, 0], False),
        ([1, 1, 1, 0, 0, 0, 0, 0, 0], True),
        ([2, 1, 0, 0, 2, 1, 0, 0, 0], False),
        ([2, 1, 0, 0, 2, 1, 2, 0, 0], False),
        ([0, 0, 0, 1, 1, 1, 0, 0, 0], True),
        ([0, 0, 0, 0, 0, 0, 1, 1, 1], True),
        ([2, 0, 0, 1, 1, 2, 2, 0, 0], False),
        ([1, 2, 0, 0, 1, 0, 1, 0, 2], False),
        ([1, 0, 0, 1, 0, 0, 1, 0, 0], True),
        ([0, 1, 0, 0, 1, 0, 0, 1, 0], True),
        ([0, 0, 1, 0, 0, 1, 0, 0, 1], True),
        ([2, 2, 2, 1, 1, 2, 2, 1, 1], True),
        ([1, 0, 2, 2, 1, 1, 0, 0, 2], False),
        ([1, 0, 0, 0, 1, 0, 0, 0, 1], True),
        ([0, 0, 1, 0, 1, 0, 1, 0, 0], True)
    ]
)
def test_tictactoe_check_win(board_state, expected):
    def do_nothing(*args):
        pass

    app = main.PartyPlaytime()
    main.PartyPlaytime.tictactoe_board = board_state
    app.animate_win = do_nothing
    assert app.check_win_tictactoe() == expected


@pytest.mark.parametrize(
    "board_state,expected",
    [
        ([0, 0, 0, 0, 0, 0, 0, 0, 0], [-1]),
        ([2, 1, 0, 0, 2, 1, 0, 0, 0], [8]),
        ([2, 1, 0, 0, 2, 1, 2, 0, 0], [2, 3, 8]),
        ([2, 0, 0, 1, 1, 2, 2, 0, 0], [-1]),
        ([1, 2, 0, 0, 1, 0, 1, 0, 2], [2, 3]),
        ([1, 0, 2, 2, 1, 1, 0, 0, 2], [-1]),
        ([1, 0, 0, 1, 2, 2, 0, 0, 1], [6]),
        ([0, 2, 1, 0, 1, 0, 0, 0, 0], [6]),
    ]
)
def test_predict_next_move(board_state, expected):
    app = main.PartyPlaytime()

    main.PartyPlaytime.tictactoe_board = board_state
    main.PartyPlaytime.tictactoe_difficulty = "hard"
    assert app.predict_next_move() in expected


@pytest.mark.parametrize(
    "move_input,expected",
    [
        (["red_alien_1", "red", 5,
          {
              "red_alien_1": 3,
              "red_alien_2": 0,
              "red_alien_3": 0,
              "red_alien_4": 0,

              "yellow_alien_1": 0,
              "yellow_alien_2": 0,
              "yellow_alien_3": 0,
              "yellow_alien_4": 0,

              "green_alien_1": 0,
              "green_alien_2": 0,
              "green_alien_3": 0,
              "green_alien_4": 0,

              "blue_alien_1": 0,
              "blue_alien_2": 0,
              "blue_alien_3": 0,
              "blue_alien_4": 0
          }], False),
        (["red_alien_2", "red", 6,
          {
              "red_alien_1": 3,
              "red_alien_2": 0,
              "red_alien_3": 1,
              "red_alien_4": 0,

              "yellow_alien_1": 0,
              "yellow_alien_2": 0,
              "yellow_alien_3": 7,
              "yellow_alien_4": 7,

              "green_alien_1": 0,
              "green_alien_2": 0,
              "green_alien_3": 0,
              "green_alien_4": 0,

              "blue_alien_1": 0,
              "blue_alien_2": 0,
              "blue_alien_3": 0,
              "blue_alien_4": 0
          }], True),
        (["blue_alien_1", "blue", 2,
          {
              "red_alien_1": 3,
              "red_alien_2": 0,
              "red_alien_3": 0,
              "red_alien_4": 0,

              "yellow_alien_1": 0,
              "yellow_alien_2": 0,
              "yellow_alien_3": 0,
              "yellow_alien_4": 0,

              "green_alien_1": 0,
              "green_alien_2": 0,
              "green_alien_3": 0,
              "green_alien_4": 0,

              "blue_alien_1": 8,
              "blue_alien_2": 10,
              "blue_alien_3": 10,
              "blue_alien_4": 0
          }], False),
        (["green_alien_1", "green", 3,
          {
              "red_alien_1": 3,
              "red_alien_2": 0,
              "red_alien_3": 0,
              "red_alien_4": 0,

              "yellow_alien_1": 23,
              "yellow_alien_2": 23,
              "yellow_alien_3": 0,
              "yellow_alien_4": 0,

              "green_alien_1": 20,
              "green_alien_2": 0,
              "green_alien_3": 0,
              "green_alien_4": 0,

              "blue_alien_1": 8,
              "blue_alien_2": 10,
              "blue_alien_3": 10,
              "blue_alien_4": 0
          }], True),
        (["yellow_alien_4", "yellow", 6,
          {
              "red_alien_1": 3,
              "red_alien_2": 0,
              "red_alien_3": 0,
              "red_alien_4": 0,

              "yellow_alien_1": 23,
              "yellow_alien_2": 23,
              "yellow_alien_3": 0,
              "yellow_alien_4": 0,

              "green_alien_1": 20,
              "green_alien_2": 33,
              "green_alien_3": 33,
              "green_alien_4": 0,

              "blue_alien_1": 8,
              "blue_alien_2": 10,
              "blue_alien_3": 10,
              "blue_alien_4": 0
          }], True),
        (["yellow_alien_4", "yellow", 6,
          {
              "red_alien_1": 3,
              "red_alien_2": 7,
              "red_alien_3": 7,
              "red_alien_4": 0,

              "yellow_alien_1": 23,
              "yellow_alien_2": 23,
              "yellow_alien_3": 0,
              "yellow_alien_4": 1,

              "green_alien_1": 20,
              "green_alien_2": 33,
              "green_alien_3": 33,
              "green_alien_4": 0,

              "blue_alien_1": 8,
              "blue_alien_2": 10,
              "blue_alien_3": 10,
              "blue_alien_4": 0
          }], True),

    ]
)
def test_alien_blockage(move_input, expected):
    app = main.PartyPlaytime()
    main.aliens_state = move_input[3]

    assert app.blockage(move_input[0], move_input[1], move_input[2]) == expected


@pytest.mark.parametrize(
    "move_input,expected",
    [
        ([4, 6,
          {
              "red_alien_1": 3,
              "red_alien_2": 7,
              "red_alien_3": 7,
              "red_alien_4": 0,

              "yellow_alien_1": 23,
              "yellow_alien_2": 23,
              "yellow_alien_3": 0,
              "yellow_alien_4": 1,

              "green_alien_1": 20,
              "green_alien_2": 33,
              "green_alien_3": 33,
              "green_alien_4": 0,

              "blue_alien_1": 8,
              "blue_alien_2": 10,
              "blue_alien_3": 10,
              "blue_alien_4": 0
          }], ["yellow_alien_1", "yellow_alien_2"]),
        ([2, 6,
          {
              "red_alien_1": 3,
              "red_alien_2": 7,
              "red_alien_3": 7,
              "red_alien_4": 0,

              "yellow_alien_1": 23,
              "yellow_alien_2": 23,
              "yellow_alien_3": 0,
              "yellow_alien_4": 1,

              "green_alien_1": 20,
              "green_alien_2": 33,
              "green_alien_3": 33,
              "green_alien_4": 0,

              "blue_alien_1": 8,
              "blue_alien_2": 10,
              "blue_alien_3": 10,
              "blue_alien_4": 0
          }], ['blue_alien_1', 'blue_alien_2', 'blue_alien_3', 'blue_alien_4']),
        ([1, 3,
          {
              "red_alien_1": 3,
              "red_alien_2": 7,
              "red_alien_3": 7,
              "red_alien_4": 0,

              "yellow_alien_1": 23,
              "yellow_alien_2": 23,
              "yellow_alien_3": 0,
              "yellow_alien_4": 1,

              "green_alien_1": 20,
              "green_alien_2": 33,
              "green_alien_3": 33,
              "green_alien_4": 0,

              "blue_alien_1": 8,
              "blue_alien_2": 10,
              "blue_alien_3": 10,
              "blue_alien_4": 0
          }], ['red_alien_1']),
        ([3, 3,
          {
              "red_alien_1": 3,
              "red_alien_2": 7,
              "red_alien_3": 7,
              "red_alien_4": 0,

              "yellow_alien_1": 23,
              "yellow_alien_2": 23,
              "yellow_alien_3": 0,
              "yellow_alien_4": 1,

              "green_alien_1": 20,
              "green_alien_2": 0,
              "green_alien_3": 7,
              "green_alien_4": 0,

              "blue_alien_1": 8,
              "blue_alien_2": 10,
              "blue_alien_3": 10,
              "blue_alien_4": 0
          }], []),
    ]
)
def test_find_alien_moves(move_input, expected):
    app = main.PartyPlaytime()
    main.aliens_state = move_input[2]

    assert app.find_alien_moves(move_input[0], move_input[1]) == expected
