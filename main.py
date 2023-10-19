import copy
import random


class Card:
    def __init__(self, value, representation):
        self.representation = f"{representation}({value})"

        if value == "A":
            self.value = [11, 1]
        elif value in ['J', 'Q', 'K']:
            self.value = [10]
        else:
            self.value = [int(value)]

    def __str__(self):
        return self.representation

    def __repr__(self):
        return f"{self.representation} {self.value}"

    """
    [
    [2, 3, 7, 11], => 23
    [2, 3, 7, 1], => 13
    [2, 3, 7, 11, 11], => 34
    [2, 3, 7, 1, 11], => 24
    [2, 3, 7, 11, 1], => 24
    [2, 3, 7, 1, 1], => 14 *
    ]
    """


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.score = 0
        self.have5 = False

    def __str__(self):
        return self.name

    def add_to_list(self, base_list, value):
        x = 0

        while x < len(base_list):
            base_list[x].append(value)
            x += 1

    def calculate_score(self):
        results = [[]]

        for card in self.cards:
            if len(card.value) == 2:
                # Se utiliza deepcopy para que haga una copia real y no solamente una referencia
                copylist = copy.deepcopy(results)
                self.add_to_list(copylist, card.value[1])
                self.add_to_list(copylist, card.value[0])
                results = results + copylist

            else:
                self.add_to_list(results, card.value[0])

        best_score = 0

        for list_score in results:
            total = sum(list_score)

            if total <= 21:
                if len(list_score) == 5:
                    self.have5 = True
                if best_score < total:
                    best_score = total
                    if len(list_score) != 5:
                        self.have5 = False

        self.score = best_score

    def receive_card(self, card):
        self.cards.append(card)
        self.calculate_score()

    def other_card(self):
        we_want = False
        if 0 < self.score < 16:
            we_want = True
        elif 16 >= self.score < 19:
            we_want = random.randint(0, 1)
        else:
            we_want = False

        return we_want

    def get_score(self):
        return self.score, self.have5


class Dealer:
    def create_deck(self):
        still = ('C', 'D', 'T', 'P')
        bases = list(range(2, 10)) + ['A', 'J', 'Q', 'K']
        deck = []

        for dstill in still:
            for base in bases:
                deck.append(Card(str(base), dstill))

        return deck

    def shuffle_deck(self):
        self.deck = self.create_deck()
        random.shuffle(self.deck)

        return self.deck

    def parse_int(self, message):
        dev = None

        while dev is None:
            try:
                dev = int(input(message))
            except:
                print("Sorry, value is not a number, try again!")

        return dev

    def create_players(self):
        self.players = []
        num_of_players = self.parse_int("Number of Players: ")

        for x in range(1, num_of_players + 1):
            self.players.append(Player("Player %d" % x))

    def initial_cards(self):
        for player in self.players:
            player.receive_card(self.deck.pop())
            player.receive_card(self.deck.pop())

    def player_want_more_cards(self):
        for player in self.players:
            while player.other_card():
                player.receive_card(self.deck.pop())

    def check_winner(self):
        winners = []
        best_score = 0
        have_5_cards = False

        for player in self.players:
            player_score, player_have5 = player.get_score()

            if  0 < player_score <= 21:
                if player_score > best_score:
                    winners = [player]
                    best_score = player_score
                    have_5_cards = player_have5

                elif player_score == best_score:
                    if player_have5:
                        if have_5_cards:
                            winners.append(player)
                        else:
                            winners = [player]
                    else:
                        if not have_5_cards:
                            winners.append(player)

        if len(winners) > 0:
            print("Congrats!!", winners)
        else:
            print("Home is the Winner")


my_dealer = Dealer()
my_dealer.shuffle_deck()
my_dealer.create_players()
my_dealer.initial_cards()
my_dealer.player_want_more_cards()
my_dealer.check_winner()
