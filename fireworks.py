import random

def cards_to_text(cards):
    for x in cards:
        c = 0b000111 & x
        n = x >> 3
        print ((_colors_to_text[c], n), end='')
    print('')

def card_color(card):
    return 0b000111 & card

def card_count(card):
    return card >> 3

_players = 4
_colors = [1, 2, 3, 4, 5]
_colors_to_text = {
    1: 'Red',
    2: 'Green',
    3: 'Blue',
    4: 'White',
    5: 'Yellow'
}
_color_abbr_to_index = {
    'r': 1,
    'g': 2,
    'b': 3,
    'w': 4,
    'y': 5
}
_board = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: []
}

deck = []
for n in [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]:
    for c in _colors:
        deck.append(n << 3 | c)
random.shuffle(deck)

_player_cards = {}
for n in range(5 if _players < 3 else 4):
    for p in range(_players):
        if p not in _player_cards:
            _player_cards[p] = []
        c = [deck.pop()]
        c.append(0)
        _player_cards[p].append(c)

print(_player_cards[1])
_explosions = 0
_hints = 8
_discard = []
while (True):
    for p in range(_players):
        print("Deck:", len(deck), "\tDiscarded:", len(_discard))
        print("Hints:", _hints, "\tExplosions:", _explosions)
        print("Board", _board, end='\n\n')
        for key, value in _player_cards.items():
            if key == p:
                print(key, end='')
                for i, c in enumerate(value):
                    print ('\t', i, end=' ')
                    if 0b000111 & c[1] in _colors_to_text:
                        print(_colors_to_text[0b000111 & c[1]], end=' ')
                    else:
                        print('?', end=' ')

                    if c[1] >> 3 > 0:
                        print(c[1] >> 3, end=' ')
                    else:
                        print('#', end='')
                print('')
                #print(key, [(_colors_to_text[0b000111 & x[0]], x[0] >> 3, x[1]) for x in value])
            else:
                print(key, [(_colors_to_text[0b000111 & x[0]], x[0] >> 3, x[1]) for x in value])

        g = input('P_lay, H_int, D_iscard?')
        if g[0] == 'p':
            index = int(g[1])
            c = _player_cards[p].pop(index)
            print("you play ", end='')
            cards_to_text([c[0]])
            color_board = _board[card_color(c[0])]
            card_num = card_count(c[0])
            if not len(color_board):
                if card_num == 1:
                    color_board.append(c[0])
                else:
                    print("BAD PLAY!")
                    _explosions = _explosions + 1
                    _discard.append(c[0])
            elif color_board[-1] == card_num - 1:
                color_board.append(c[0])
            else:
                print("BAD PLAY!")
                _explosions = _explosions + 1
                _discard.append(c[0])
            if len(deck):
                _player_cards[p].insert(0, deck.pop())

            if _explosions == 3:
                raise Exception("YOU LOSE")

            if sum([len(b) for b in _board.values()]) == len(_board) * 5:
                raise Exception("YOU WIN")
        elif g[0] == 'd' and _hints < 8:
            _hints = _hints + 1
            index = int(g[1])
            _discard.append(_player_cards[p].pop(index))
            if len(deck):
                _player_cards[p].insert(0, deck.pop())
        elif g[0] == 'h' and _hints > 0:
            _hints = _hints - 1
            player = int(g[1])
            color = 0
            number = 0
            if g[2] in _color_abbr_to_index:
                color = _color_abbr_to_index[g[2]]
            else:
                number = int(g[2])

            for c in _player_cards[player]:
                if card_color(c[0]) == color:
                    c[1] = c[1] | color
                elif card_count(c[0]) == number:
                    c[1] = number << 3 | c[1]

























