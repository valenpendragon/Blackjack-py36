# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 07:17:53 2018

This is the principal Class library for Blackjack Games. These classes include:

    Class Card: Stores a card, along with its value in Blackjack.
        SubClass Ace: Stores aces, which have two possible values in game.

    Class Deck: 52 card object
        SubClass CardShoe: A multideck (1 to 8 decks) object fully shuffled
            with additional entropy added to improve randomness.

    Class Hand: A grouping of cards dealt to players.
        SubClass SplitHand: Handles the special methods unique to split hands.
        SubClass DealerHand: A hand specifically designed for the dealer.

    Class Player: Stores the hand(s), bet(s), and bank status of each player
        SubClass Dealer: Stores the hand of the dealer and the dealer's bank.'

    Class CasinoTable: Object stores blackjack multipliers, players, the deck
        and the Dealer. It hands the actual play of rounds of Blackjack.

    Class Casino:  Store CasinoTable objects of various kinds. Methods
        arbitrate which tables players can play at and controls special events.

    Class Game: This object stores the attributes of the players between games.

@author: Jeffrey Scott
"""

import random as rd

# Constants:
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
SUITS = ( 'S', 'D', 'H', 'C')

class Card(object):
    '''
    This class is used to simulate a playing card. It is composed of a
    three attributes: rank, suit, and value, where rank is taken from 2 through
    king, suit (also found below), and value is based on the rank, being
    equal to numerical value appearing in the rank. All "face" cards, Jack,
    Queen, and King, have a value of 10 as well.
    Note: Aces are dealt with in a subclass.

    Methods:
        __init__: creates a card tuple using provided rank and suit.
        __str__: returns the card in Rank-Suit format.

    Attributes:
        self.rank: This is the rank of the card. Valid values are: '2', '3',
            '4', '5', '6', '7','8', '9', '10', 'J', 'Q', 'K'.
            Note: The rank of this base class does not include Aces.
        self.suit: This is the card suit (Spades, Diamonds, Hearts, Clubs),
            represented by the first character of the name of the suit.
        self.value: This is the integer value of the rank (2 - 10).
    '''

    # Methods
    def __init__(self, rank, suit):
        """
        This method creates a card object from two arguments, rank and suit.
        If a rank appears that is not in ranks, it will raise a ValueError.
        INPUTS: rank, suit, both strings
        OUTPUT: None
        """
        # First we need to check the rank. If is not in a specific set of
        # values, we need to raise an error. We have to explicitly create
        # a local copy of ranks and suits since they do not exist yet.
        ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
        suits = ('S', 'D', 'H', 'C')
        if rank not in ranks:
            print(f"Card: An invalid rank was supplied {rank}.")
            raise ValueError("Card objects must have a valid rank.") from None
            return None

        if suit not in suits:
            print(f"Card: An invalid suit was supplied {suit}.")
            raise ValueError("Card objects must have a valid suit.") from None
            return None

        # If we get to this point, the rank and suit are valid choices.
        self.rank = rank
        self.suit = suit
        # Now, we need to check the value. We will try to convert the rank to
        # an integer. If successful, we know that the card is 2 to 10. If not,
        # we know that it is a face card (Aces are dealt with in a subclass).
        try:
            value = int(self.rank)
        except ValueError:
            # This is a face card.
            value = 10
        self.value = value

    def __str__(self):
        """
        This method returns the card in the format Rank-Suit. It suppresses
        the newline very specifically. It takes no arguments.
        """
        return "{0}-{1} ".format(self.rank, self.suit)


class Ace(Card):
    """
    This class deals with the special case that a card is an Ace. Aces have two
    possible values in Blackjack, 1 or 11. The value depends on whether or not
    the dealer or player would bust if the Ace is considered an 11. This class
    inherits __str__, but needs a separate __init__() method. In usage in game
    programming, use an if statement like this one:
        if type(card) == Ace:
    to separate Aces from the other cards when scoring hands, etc.

    Unique Methods:
        __init__: Adds an extra attribute reflecting an ace's second value.
            Takes only suit as an argument.

    Inherited Methods:
        __str__: Returns a value string in Rank-Suit format.

    Unique Attributes:
        self.additional_value: This is the higher value of a Ace, 11.

    Inherited Attributes:
        self.rank: This is the rank of the card. Valid values are: '2', '3',
            '4', '5', '6', '7','8', '9', '10', 'J', 'Q', 'K'.
            Note: The rank of this base class does not include Aces.
        self.suit: This is the card suit (Spades, Diamonds, Hearts, Clubs),
            represented by the first character of the name of the suit.
        self.value: This is the integer value of the rank (2 - 10).

    """

    # Methods:
    def __init__(self, suit):
        """
        Aces only take a str value for suit. They take no other arguments.
        INPUT: suit, string
        OUTPUT: None
        """
        suits = ('S', 'D', 'H', 'C')
        if suit not in suits:
            print(f"Card: An invalid suit was supplied {suit}.")
            raise ValueError("Card objects must have a valid suit.") from None
            return None

        # A valid suit was supplied.
        self.rank = 'A'
        self.suit = suit
        self.value = 1
        self.additional_value = 11


class Deck(object):
    '''
    This class returns a 52-card shuffled deck consisting of 4 suits, and 13
    cards per suit, Ace through King.

    Methods:
        __init__: returns a shuffled deck of 52 cards. Takes no arguments.
        __str__: returns the string "A shuffled deck of {length} cards", where
            length is the length determined by the __len__ function below.
            When invoked with diagnostic=True, prints the CardShoe.
        __len__: returns the number of cards remaining in the deck.
        remove_top: removes the card at index 0 and shifts the cards up one
            accordingly. This method takes no arguments.
    Attributes:
        shuffled_deck: the contents of the deck (a list of card objects
        length: The number of cards in the original deck.

    '''
    def __init__(self):
        """
        This method generates a 52-card fully shuffled deck. It uses calls to
        rd.randint and rd.shuffle to create additional chaos in the shuffling
        process.

        NOTE: This randomization is good enough for a video game, but it is not
        random enough for gambling purposes.

        """
        # This is a single standard deck of 52 cards.
        self.length = 52

        # Next, we need to create an unshuffled deck to move cards from.
        deck = []
        for rank in RANKS:
            for suit in SUITS:
                # Create the card.
                if rank == 'A':
                    card = Ace(suit)
                else:
                    card = Card(rank, suit)
                deck.append(card)

        # Next, we shuffle it using the rd.shuffle.
        rd.shuffle(deck)

        # To add some additional entropy, we take this shuffled set of cards
        # and randomly remove them one at a time and put them in the actual
        # shuffled deck, self.shuffled_deck.
        self.shuffled_deck = []
        while len(deck) > 0:
            next_card = deck.pop(rd.randint(0, len(deck) - 1))
            self.shuffled_deck.append(next_card)
        del deck

    def __len__(self):
        """
        This method prints out the number of cards remaining in the Deck.
        object. It takes no arguments.
        INPUTS: None
        OUTPUTS: length, integer
        """
        return len(self.shuffled_deck)

    def __str__(self, diagnostic=False):
        """
        This method prints out the deck. In normal mode, it prints a string
        with the number of cards reamining in the deck. When diagnostic is
        True, it will print cards listed in the deck.
        INPUTS: diagnostic, boolean, defaults to False
        OUTPUTS: a string indicating remaining cards or an actual printout of
            the deck to the terminal screen.
        NOTE: To use the diagnostic option, use the Deck.__str__(**kwargs) form
            not the print(Deck) or str(Deck) methods.
        """
        if not diagnostic:
            return "The deck has {0} cards remaining.".format(len(self))
        else:
            for card in self.shuffled_deck:
                print(card)

    def remove_top(self):
        """
        This mechod removes the card at index zero of the Deck object. This is
        used when dealing cards from the deck.
        INPUTS: None
        OUTPUTS: card, Card type object
        """
        return self.shuffled_deck.pop(0)


class CardShoe(Deck):
    '''
    This class uses the Deck class to create a CardShoe of up to 1 to 8 52 card
    decks.

    Unique Methods:
        __init__: The creation method requires an argument indicating the
            number of 52 card decks that will make up the CardShoe.

    Inherited Methods:
        __str__: returns the string "A shuffled deck of {length} cards", where
            length is the length determined by the __len__ function below.
            When invoked with diagnostic=True, prints the CardShoe.
        __len__: returns the number of cards remaining in the deck.
        remove_top: removes the card at index 0 and shifts the cards up one
            accordingly. This method takes no arguments.

    Unique Attributes: None

    Inherited Attributes:
        shuffled_deck: the contents of the deck (a list of card objects
        length: The number of cards in the original deck.
    '''
    def __init__(self, cs_size):
        """
        This method creates a CardShoe object that contains cs_size 52 card
        Deck objects. It will check cs_size for a valid integer between 1 and
        8, raising a TypeError if it is not an integer or a ValueError if
        cs_size is not in the correct range.
        INPUTS: cs_size, integer
        OUTPUTS: CardShoe object
        """
        # Handling problems with cs_size that could break this method.
        if type(cs_size) != int:
            raise TypeError("CardShoe: cs_size must be an integer")
        elif not 1 <= cs_size <= 8:
            raise ValueError("""CardShoe: cs_size must be type int
                             within [1, 8].""")

        self.length = 52 * cs_size
        self.shuffled_deck = []
        for i in range(cs_size):
            self.shuffled_deck.extend(Deck().shuffled_deck)


class Hand(object):
    '''
    This class stores cards for a normal blackjack hand. The receive_card
    method handles maintaining attributes for the Hand object as it receives
    Cards.

    Class Order Attributes:
        hand_type = 'regular' (string)
        Note: The subclasses use a different value for this constant.

    Methods:
        __init__: Creates an empty player's hand. Initializes all of the Hand's
            attributes.
        __str__: Prints out the Hand.
        __len__: Returns the number of cards in the Hand.
        receive_card(card): Requires a Card object. Adds it to the Hand, then
            updates all of the Hand's attributes (listed below) accordingly.

    Attributes:
        cards: list of Card objects. Starts empty.
        has_ace: Boolean. Starts False.
        soft_score: integer, highest possible hand score less than 22 derivable
            from the cards (differs from hard_score if an ace is present).
            Starts 0.
        hard_score: integer, score of the hand if all Aces are scored as rank 1
            (differs from soft_score only if an ace is present). Starts 0.
        blackjack: Boolean. Starts False.
        has_pair: Boolean. Starts False.
        busted: Boolean. Starts False.

    '''
    hand_type = 'regular'

    def __init__(self):
        """
        This method creates an empty player's Hand and initializes the Hand's
        attributes.
        INPUTS: None
        OUTPUTS: Hand object
        """
        self.cards = []
        self.has_ace = False
        self.soft_score = 0
        self.hard_score = 0
        self.blackjack = False
        self.has_pair = False
        self.busted = False

    def __len__(self):
        """
        This method returns the number of cards in the Hand object.
        INPUTS: None
        OUTPUTS: length, integer
        """
        return len(self.cards)

    def __str__(self, diagnostic=False):
        """
        This method prints out the cards contained in the Card object and the
        possible scores for this hand. If this method is invoked using the form
        Hand.__str__(diagnostic=True), it will print out all of the Hand
        attributes.
        """
        # This code checks to see which Hand types have been loaded along with
        # the Hand base class.
        if diagnostic:
            print("Type of hand: {0}".format(self.hand_type))
            if len(self) == 0:
                print("No cards in the hand currently.".format(end=''))
            else:
                print("Cards in player's hand: ".format(end=''))
                for card in self.cards:
                    card_str = print(card)
                    print("{0}".format(card_str, end=''))
            print("\nRemaining Attributes:")

            # These attributes exist in all classes and subclasses of Hand.
            print("\thas_ace = {0}".format(self.has_ace))
            print("\tsoft_score = {0}".format(self.soft_score))
            print("\thard_score = {0}".format(self.hard_score))

            # The following code makes this method work for all subclasses:
            # self.blackjack does not exist for split hands.
            if self.hand_type != 'split':
                print("\tblackjack = {0}".format(self.blackjack))
            # self.has_pair only exists for a player's regular hand.
            if self.hand_type == 'regular':
                print("\thas_pair = {0}".format(self.has_pair))

            # self.busted exists in all classes and subclasses
            print("\tbusted = {0}".format(self.busted))
        else:
            if len(self) == 0:
                print("No cards have been dealt to the {0} hand yet.".format(
                        self.hand_type))
            else:
                print("Player's {0} hand: ".format(self.hand_type, end=''))
                for card in self.cards:
                    card_str = print(card)
                    print("{0}".format(card_str, end=''))
                print("\n\tSoft Score: {0}".format(self.soft_score))
                print("\tHard Score: {0}".format(self.hard_score))

                # This code may seem a little cumbersome, but SplitHand does
                # not have a blackjack attribute.  This makes the code fully
                # inheritable for all classes. A try block is not as much of a
                # problem here.
                try:
                    if self.hand_type != 'split' and self.blackjack:
                        print("This player has blackjack.")
                except NameError:
                    # This pass command traps the NameError split hands.
                    pass

                # All Hand classes have a busted attribute.
                if self.busted:
                    print("This hand has busted.")
                else:
                    print("This hand is still solvent.")
            # Note: The attributes self.has_ace and self.has_pair (if they
            # exist for this object) are used behind the scenes.
        return ""

    def receive_card(self, top_card):
        """
        This method adds a card to the Hand. This card should have been the top
        card from the CardShoe or Deck object in the game.
        INPUTS: top_card, a Card class object
        OUTPUTS: None. All changes are made to attributes.
        """
        # First, we check for to see if the new card is an ace. If an ace was
        # already added, self.has_ace is already True.
        if type(top_card) == Ace:
            self.has_ace = True
        # Next, we check for pairs. Only the base (regular) Hand class cares
        # about pairs.
        if self.type == 'regular':
            for card in self.cards:
                if card.rank == top_card.rank:
                    self.has_pair = True
        # Next, we need check to see if the second card in the hand is an Ace
        # or a 10 value card. The DealerHand is the only class that cares about
        # this condition. This only matters for the face up card (2nd dealt) as
        # well.
        if self.type == 'dealer' and len(self) == 1:
            if top_card.value == 1 or top_card.value == 10:
                self.insurance = True
        # Next, we need to add the card to the cards list.
        self.cards.append(top_card)
        # Next, we need to rescore the hand.  All hands are scored using the
        # same formulas. The scores will be the same if there are no Aces in
        # the hand. The hard score is always the lower of the two scores. It
        # treats all Aces as a value of 11.
        hard_score = 0
        for card in self.cards:
            hard_score += card.value
        if self.has_ace:
            # So, we detected at least one Ace. We can only score one Ace as a
            # 11 since 22 is an automatic bust. So, we only need to add 10 to
            # the hard score to see if it busts.
            soft_score = hard_score + 10
        # We check the new soft_score. If it busts, we adjust it down. If not,
        # then both scores are solvent. Note, we have not tested the hard score
        # but it is lowest possible score the hand can have. So, we have to
        # record the score now, even if it is a bust and check for a bust.
        if soft_score > 21:
            self.soft_score = hard_score
            self.hard_score = hard_score
            # This is the bust check. Any type of Hand can bust.
            if hard_score > 21:
                self.busted = True
        else:  # both scores are solvent
            self.soft_score = soft_score
            self.hard_score = hard_score
        # For regular and dealer Hands, we have to check for a blackjack.
        if self.type != 'split' and len(self) == 2:
            # A blackjack requires 1 Ace and 1 10 value card.
            if self.cards[0].value == 1 and self.cards[1].value == 10:
                self.blackjack = True
            if self.cards[1].value == 1 and self.cards[0].value == 10:
                self.blackjack = True
