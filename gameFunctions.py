import random as rand


# input: array, int
# output: shuffled array
def shuffle(arr, bunch=5):
    # bunch: this is the max number of elements that can be bunched during the shuffle.

    half_index = round(len(arr)/2)
    first = arr[0:half_index]
    second = arr[half_index:len(arr)]
    first_index = 0
    second_index = 0
    acc = [] # output array

    # check bunch compared to array size.
    if bunch > 0.1 * len(arr) > 1 or bunch == 1:
        print("Bad Shuffle: bunch needs to be less than %g and greater than 1" % 0.1*len(arr))

    while first_index < len(first) or second_index < len(second):
        first_chunk = rand.randint(1, bunch)  # generate how many cards are bunched at a time.
        second_chunk = rand.randint(1, bunch)

        # ensure chunk grabbed is smaller then the length of the half.
        if first_index + first_chunk > len(first):
            first_chunk = len(first) - first_index
        if second_index + second_chunk > len(second):
            second_chunk = len(second) - second_index

        first_bunch = first[first_index:first_index+first_chunk]
        second_bunch = second[second_index:second_index+second_chunk]

        while len(first_bunch) > 0:
            acc.append(first_bunch.pop())
        while len(second_bunch) > 0:
            acc.append(second_bunch.pop())

        first_index = first_index + first_chunk
        second_index = second_index + second_chunk
    return acc


# shuffles number of specified decks with a specified bunch size for shuffling.
# inputs: int decks used, int clumping for shuffling, int num shufles
# outputs: str arr deck
def get_shuffled_deck(num_decks=6, bunch=5, num_shuffles=10):
    base = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck = base * 4 * num_decks
    for i in range(num_shuffles):
        deck = shuffle(deck, bunch)
    return deck


# use when the hands are clean, reshuffles discard and remainder of deck
# inputs: str arr deck, str arr discard pile
# outputs: str arr deck, str arr discard pile
def reshuffle(deck, discard):
    while len(deck) > 0:
        discard.append(deck.pop())

    deck = shuffle(discard)
    discard = []
    return deck, discard


# inputs: int number of players
# outputs: str game array of players hands, int bet array,, str arr discard pile.  These will be empty.
def initialize(num_players=6):
    hands = []
    bets = []
    discard = []
    for i in range(num_players+1): # note hand 0 is dealer.
        hands.append('')
        bets.append(0)

    return hands, bets, discard


# inputs: str hands array, str deck array
# outputs: str hands array , str deck array remaining
def deal(hands, deck): # attempting to deal similarly to casino style, even if that is slightly slower
    for i in range(len(hands)):
        hands[i] = deck.pop() + ','
    for i in range(len(hands)):
        hands[i] = hands[i] + deck.pop()
    return hands, deck


# empties hands onto discard pile
# inputs: str arr hands, str arr discard pile
# outputs: str arr hands, str arr discard pile
def cleanup(hands, discard, num_players=6):
    for i in range(len(hands)):
        cards_in_hand = hands[i].split(',')
        for j in range(len(cards_in_hand)):
            discard.append(cards_in_hand.pop())
    hands = []
    for i in range(num_players+1):
        hands.append('')
    return hands, discard


# returns the soft hand value used by dealer.
# inputs: str hand
# outputs: int hand value
def get_hand_value(hand):  # aak does not read right.
    if hand == '':  # hand is empty
        raise ValueError

    aces = 0 # num aces in hand
    val_non_ace = 0
    cards = hand.split(',')

    for card in cards:
        if card != 'A':
            if card != 'J' and card != 'Q' and card != 'K':
                val_non_ace += int(card)
            else:
                val_non_ace += 10
        else:
            aces += 1

    if aces == 0:
        value = val_non_ace
    elif aces == 1:
        value = val_non_ace + 11
        if value > 21:
            value = val_non_ace + 1
    else:
        value = val_non_ace + 11
        if value > 21:
            value = val_non_ace + 1
        value += (aces-1) * 1
    return value


# ai code to decide wheather to hit, true, or not. hits if below 15
# inputs: str hand
# outputs: bool
def ai_15(hand):
    value = get_hand_value(hand)
    return value < 15


# prints hand output to console
# inputs: str arr hands, arr int bets, int seat, bool show dealer cards.
# ouputs: void
def print_board_state(hands, bets, seat=3, show_dealer=False):
    if show_dealer:
        print('\t\t\t\t' + hands[0])
    else:
        print('\t\t\t\t' + hands[0].split(',')[0] + ','+ '-')

    acc = ''
    for i in range(len(hands)):
        if i != 0:
            if i == seat:
                acc += '|' + hands[i] + '|' + '\t\t'
            else:
                acc += hands[i] + '\t\t'
    acc += '\n'
    for i in range(len(bets)):
        if i != 0:
            if i == seat:
                acc += '|' + str(bets[i]) + '|' + '\t\t'
            else:
                acc += str(bets[i]) + '\t\t'
    print(acc + '\n')



if __name__ == "__main__":
    hands, bets, discard = initialize()
    deck = get_shuffled_deck()
    hands, deck = deal(hands, deck)
    print_board_state(hands, bets)
