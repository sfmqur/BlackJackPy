from gameFunctions import *

# User Config
start_money = 100
default_bet = 5
blackjack_rate = 1.5
hit_soft_17 = True

# player configuration
try:
    seat = int(input("Where would you like to sit at the table? Seats 1 through 6\nInput -1 for watching AI play\n").strip())
    if seat > 6 or not seat:
        print("That is not a valid seat. You are sitting at seat 3")
        seat = 3
except ValueError:
    seat = 3

# todo: AI config here

print('Default bet: %g,  Blackjack return: %g' % (default_bet, blackjack_rate))

# game setup
run = True
hands, bets, discard = initialize()
deck = get_shuffled_deck()
bet = default_bet
money = []

for i in range(len(hands)):
    money.append(start_money)

while run:
    print("%g%% of Deck Remaining" % (100*len(deck)/(52*6)))
    command = input('Your current bet is %g, change bet? (y, exit, all other input moves on)\n' % bet).strip()
    if command == 'y':
        try:
            bet = int(input('New Bet: ').strip())
            if bet < 0:
                raise ValueError
        except ValueError:
            print('Invalid Bet')
    elif command == 'exit':
        run = False
        break

    # set bets
    for i in range(len(bets)):
        if i == seat:
            bets[seat] = bet
        else:
            bets[i] = default_bet

    # remove bets from money
    for i in range(len(money)):
        money[i] -= bets[i]

    hands, deck = deal(hands, deck)
    # check for blackjacks
    blackjacks = [False,False,False,False,False,False,False]

    for i in range(len(hands)):
        if get_hand_value(hands[i]) == 21:
            blackjacks[i] = True

    if blackjacks[0]:
        print_board_state(hands, bets, seat, True)
        dealer_blackjack = True
    else:
        dealer_blackjack = False

    # do split here. have seat be array of seats, add one next to current...somehow.
    # ask to hit stay or double (split coming in future)
    if not dealer_blackjack:
        for i in range(len(hands)):
            if i == seat:
                print_board_state(hands, bets, seat)
                stay = False
                value = get_hand_value(hands[i])
                while get_hand_value(hands[i]) < 21 and not stay:
                    command = input("Stay/ Double Down? (s, d, all other input is hit): \n").strip()
                    if command == 's':
                        stay = True
                    elif command == 'd':
                        stay = True
                        money[i] -= bets[i]
                        bets[i] += bets[i] # doubles bet
                        draw = deck.pop()
                        hands[i] += ',' + draw
                        print_board_state(hands, bets, seat)
                        if get_hand_value(hands[i]) > 21:
                            print("Bust!")
                    else:
                        draw = deck.pop()
                        hands[i] += ',' + draw
                        print_board_state(hands, bets, seat)
                        if get_hand_value(hands[i]) > 21:
                            print("Bust!")
            elif i == 0:
                pass
            else:
                value = get_hand_value(hands[i])
                while value < 21 and ai_15(hands[i]):
                    draw = deck.pop()
                    hands[i] += ',' + draw
                    value = get_hand_value(hands[i])

                if i == len(hands) - 1: # does dealer last
                    value = get_hand_value(hands[0])
                    while value < 17:
                        draw = deck.pop()
                        hands[0] += ',' + draw
                        value = get_hand_value(hands[0])
                    if value == 17 and get_num_aces(hands[0]) >= 1 and hit_soft_17:
                        draw = deck.pop()
                        hands[0] += ',' + draw
                        value = get_hand_value(hands[0])
    else:
        print("Dealer Blackjack!! Bummer Dude.")

    # money Cleanup
    dealer_value = get_hand_value(hands[0])
    for i in range(len(hands)):
        if i == 0:
            pass
        else:
            value = get_hand_value(hands[i])
            if 21 >= dealer_value > value or value > 21:
                bets[i] = 0
                if i == seat:
                    print("Loss")
            elif dealer_value > 21 >= value or value > dealer_value:
                if blackjacks[i]:
                    bets[i] += bets[i] * blackjack_rate
                    if i == seat:
                        print ("Blackjack!")
                else:
                    bets[i] += bets[i]
                    if i == seat:
                        print ("Win!")
            money[i] += bets[i]

    print_board_state(hands, bets, seat, True)
    print("Cash:")
    acc = ''
    for i in range(1, len(money)):
        if i == seat:
            acc += '|' + str(money[i]) + '|' + '\t\t'
        else:
            acc += str(money[i]) + '\t\t'
    print(acc + '\n')

    # Card cleanup
    hands, discard = cleanup(hands, discard)
    if len(deck) < 0.15 * 52*6:
        deck, discard = reshuffle(deck, discard)
        print("Shuffle Time!")
