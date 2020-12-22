import fileinput
from itertools import groupby

import numpy as np

input_rows = [line.rstrip() for line in fileinput.input('input.txt')]


def parse_player(player_rows):
    player_name = player_rows[0][:-1]
    card_stack = list(map(int, player_rows[1:]))
    return player_name, card_stack


(player1_name, player1_cards), (player2_name, player2_cards) =\
    list(map(parse_player, [list(rows) for k, rows in groupby(input_rows, bool) if k]))


# Part 1


def combat(player1_cards, player2_cards):

    while not (len(player1_cards) == 0 or len(player2_cards) == 0):
        card1 = player1_cards.pop(0)
        card2 = player2_cards.pop(0)

        if card1 > card2:
            player1_cards.extend((card1, card2))
        else:
            player2_cards.extend((card2, card1))

    winning_deck = player1_cards if player1_cards else player2_cards
    return sum(np.multiply(winning_deck, list(range(len(winning_deck), 0, -1))))


print(combat(player1_cards.copy(), player2_cards.copy()))


# Part 2

def recursive_combat(player1_cards, player2_cards, previous_rounds):
    winner = -1

    while not (len(player1_cards) == 0 or len(player2_cards) == 0):
        if (tuple(player1_cards), tuple(player2_cards)) in previous_rounds:
            winner = 1
            player2_cards = []
            break

        previous_rounds.add((tuple(player1_cards), tuple(player2_cards)))

        card1 = player1_cards.pop(0)
        card2 = player2_cards.pop(0)

        if len(player1_cards) >= card1 and len(player2_cards) >= card2:
            winner, _ = recursive_combat(player1_cards[:card1], player2_cards[:card2], set())
        else:
            winner = 1 if card1 > card2 else 2

        if winner == 1:
            player1_cards.extend((card1, card2))
        else:
            player2_cards.extend((card2, card1))

    winning_deck = player1_cards if player1_cards else player2_cards
    return winner, sum(np.multiply(winning_deck, list(range(len(winning_deck), 0, -1))))


print(recursive_combat(player1_cards.copy(), player2_cards.copy(), set())[1])
