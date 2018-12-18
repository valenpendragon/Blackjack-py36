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
SUITS = ('S', 'D', 'H', 'C')


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
        This method removes the card at index zero of the Deck object. This is
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
            raise ValueError("CardShoe: cs_size must be within interval [1, 8].")

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
        __init__(ante): Creates an empty player's hand. Initializes all of the
            Hand's attributes. Raises a TypeError if the ante is not an
            integer.
        __str__: Prints out the Hand.
        __len__: Returns the number of cards in the Hand.
        receive_card(card): Requires a Card object. Adds it to the Hand, then
            updates all of the Hand's attributes (listed below) accordingly.

    Attributes:
        cards: list of Card or Ace objects. Starts empty.
        has_ace: Boolean. Starts False.
        soft_score: integer, highest possible hand score less than 22 derivable
            from the cards (differs from hard_score if an ace is present).
            Starts 0.
        hard_score: integer, score of the hand if all Aces are scored as rank 1
            (differs from soft_score only if an ace is present). Starts 0.
        blackjack: Boolean. Starts False.
        has_pair: Boolean. Starts False.
        busted: Boolean. Starts False.
        bet_amt: integer. Must be supplied when instantiated.

    '''
    hand_type = 'regular'

    def __init__(self, ante):
        """
        This method creates an empty player's Hand and initializes the Hand's
        attributes. Raises a TypeError if ante is not an integer.
        INPUTS: ante (integer)
        OUTPUTS: Hand object
        """
        if type(ante) != int:
            raise TypeError("Hand.__init__:A bet must be an integer.")
        self.cards = []
        self.has_ace = False
        self.soft_score = 0
        self.hard_score = 0
        self.blackjack = False
        self.has_pair = False
        self.busted = False
        self.bet_amt = ante

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
                print("No cards in the hand currently.", end='')
            else:
                print("Cards in player's hand: ", end='')
                for card in self.cards:
                    print(card, end='')
            print("\nRemaining Attributes:")

            # These attributes exist in all classes and subclasses of Hand.
            print("\thas_ace = {0}".format(self.has_ace))
            print("\tsoft_score = {0}".format(self.soft_score))
            print("\thard_score = {0}".format(self.hard_score))
            # This is Dealer only attribute.
            if self.hand_type == 'dealer':
                print("\tinsurance = {0}".format(self.insurance))
            # Only the Dealer has no bet_amt attribute.
            if self.hand_type != 'dealer':
                print("\tbet_amt = {0}".format(self.bet_amt))

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
                if self.hand_type != 'dealer':
                    print("Initial bet = {0}".format(self.bet_amt))
            else:
                if self.hand_type == 'dealer':
                    print("Dealer's hand: ".format(self.hand_type), end='')
                else:
                    print("Player's {0} hand: ".format(self.hand_type), end='')
                for card in self.cards:
                    print(card, end='')
                print("\n\tSoft Score: {0}".format(self.soft_score))
                print("\tHard Score: {0}".format(self.hard_score))
                if self.hand_type != 'dealer':
                    print("Current bet = {0}".format(self.bet_amt))

                # This code may seem a little cumbersome, but SplitHand does
                # not have a blackjack attribute.  This makes the code fully
                # inheritable for all classes. A try block is not as much of a
                # problem here.
                try:
                    if self.hand_type != 'split' and self.blackjack:
                        print("This player has blackjack.")
                except NameError:
                    # This pass command traps the NameError on split hands.
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
        if self.hand_type == 'regular' and len(self) == 1:
            if self.cards[0].rank == top_card.rank:
                self.has_pair = True
        # Next, we need check to see if the second card in the hand is an Ace
        # or a 10 value card. The DealerHand is the only class that cares about
        # this condition. This only matters for the face up card (2nd dealt) as
        # well.
        if self.hand_type == 'dealer' and len(self) == 1:
            if top_card.value == 1 or top_card.value == 10:
                self.insurance = True
        # Next, we need to add the card to the cards list.
        self.cards.append(top_card)
        # Next, we need to rescore the hand.  All hands are scored using the
        # same formulas. The scores will be the same if there are no Aces in
        # the hand. The hard score is always the lower of the two scores. It
        # treats all Aces as a value of 11.
        hard_score = soft_score = 0
        for card in self.cards:
            hard_score += card.value
        if self.has_ace:
            # So, we detected at least one Ace. We can only score one Ace as a
            # 11 since 22 is an automatic bust. So, we only need to add 10 to
            # the hard score to see if it busts.
            soft_score = hard_score + 10
        else:
            soft_score = hard_score
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
        if self.hand_type != 'split' and len(self) == 2:
            # A blackjack requires 1 Ace and 1 10 value card.
            if self.cards[0].value == 1 and self.cards[1].value == 10:
                self.blackjack = True
            if self.cards[1].value == 1 and self.cards[0].value == 10:
                self.blackjack = True


class SplitHand(Hand):
    '''
    Class SplitHand is a subclass of class Hand. Like Hand, it stores cards and
    attributes for blackjack split hands. When a player has a pair of cards,
    they have the option of splitting up the pair, creating two new hand. This
    new type of hand, the "split hand", is more restricted than a regular hand.
    It cannot have a blackjack, nor can it split off another hand if the player
    draws a pair for it. The original regular Hand is deleted after the cards
    and bets are moved.

    Class Order Attributes:
        hand_type = 'split' (string)

    Unique Methods:
        __init__(card, bet): This subclass requires a card and a bet amount as
            arguments. Raises a TypeError if card is not Card type or bet is
            not an integer.

    Inherited Methods:
        __str__: Prints out the SplitHand.
        __len__: Returns the number of cards in the SplitHand.
        receive_card(card): Requires a Card object. Adds it to the SplitHand,
            then updates all of the Hand's attributes (listed below)
            accordingly.

    Unique Attributes: None

    Inherited Attributes:
        cards: list of Card or Ace objects. Starts empty, then adds Card or Ace
            object supplied as an argument to the new SplitHand.
        has_ace: Boolean. Starts False.
        soft_score: integer, highest possible hand score less than 22 derivable
            from the cards (differs from hard_score if an ace is present).
            Starts 0.
        hard_score: integer, score of the hand if all Aces are scored as rank 1
            (differs from soft_score only if an ace is present). Starts 0.
        busted: Boolean. Starts False.
        bet_amt: integer. Must be supplied when instantiated.

    Note: SplitHand has no blackjack or has_pair attribute because it is formed
        after 2 cards have already been dealt to the player.

    '''
    hand_type = 'split'

    def __init__(self, card, bet):
        """
        This method initializes the SplitHand. It requires two arguments, a
        card to start off the hand, and bet amount for this hand. SplitHands
        are created from a pair of cards of the same rank.
        INPUTS: card (a Card or Ace object), bet (integer)
        OUTPUTS: a new SplitHand object
        """
        # First, we need to make sure the inputs are correct.
        if type(card) != Card and type(card) != Ace:
            raise TypeError("SplitHand.__init__: First argument is not a Card or Ace")
        if type(bet) != int:
            raise TypeError("SplitHand.__init__:A bet must be an integer.")
        self.cards = []
        self.has_ace = False
        self.soft_score = 0
        self.hard_score = 0
        self.busted = False
        self.bet_amt = bet
        self.receive_card(card)


class DealerHand(Hand):
    '''
    Class DealerHand is a subclass of Class Hand. Like Hand, it stores cards
    and attributes for the blackjack Dealer. As such, pairs have no meaning
    because the Dealer cannot have split hands. The condition of Blackjack does
    have meanning for the Dealer, however. The Dealer scores Aces the same way
    players do, although the Dealer has more restricted choices about how they
    play their Hand. The Dealer can bust, like any other player. The Dealer
    makes no bets. So, their hand has no bet_amt attribute.

    There is a unique attribute for the Dealer. When the Dealer has a card that
    is has a value of ten or an Ace showing, player's have the option to place
    an "insurance bet" on whether or not the Dealer has blackjack. The Dealer
    keeps their first card unexposed until the Dealer's turn arrives.

    Class Order Attribute:
        hand_type = 'dealer' (split)

    Unique Methods:
        __init__: Initializes the values for the Dealer's Hand. It takes no
            argument, unlike the other Hand objects.
        dealer_prin(diagnostic)t: Prints out the Dealer's Hand, while keeping
            the hold card "face down".

    Inherited Methods:
        __str__: Prints out the SplitHand.
        __len__: Returns the number of cards in the SplitHand.
        receive_card(card): Requires a Card object. Adds it to the SplitHand,
            then updates all of the Hand's attributes (listed below)
            accordingly.

    Unique Attributes:
        insurance: Boolean. Starts False. Indicates that the Dealer's visible
            card had a value of ten or is an Ace.

    Inherited Attributes:
        cards: list of Card or Ace objects. Starts empty.
        has_ace: Boolean. Starts False.
        soft_score: integer, highest possible hand score less than 22 derivable
            from the cards (differs from hard_score if an ace is present).
            Starts 0.
        hard_score: integer, score of the hand if all Aces are scored as rank 1
            (differs from soft_score only if an ace is present). Starts 0.
        blackjack: Boolean. Starts False.
        busted: Boolean. Starts False.

    Note: DealerHand has no bet_amt because bets are determined by the Players
        not by the Dealer. It also does not have a has_pair attribute because
        the Dealer cannot split their hands.
    '''
    hand_type = 'dealer'

    def __init__(self):
        """
        This method initializes the Dealer's Hand. It takes no arguments
        because the Dealer makes no bets.
        INPUTS: None
        OUTPUTS: A new DealerHand object
        """
        self.cards = []
        self.has_ace = False
        self.soft_score = 0
        self.hard_score = 0
        self.blackjack = False
        self.busted = False
        self.insurance = False

    def dealer_print(self, diagnostic=False):
        """
        This method prints out the dealer's hand, while keeping the hold card
        concealed. This is used during the player's turns and while hands are
        being dealt to everyone at the table.
        INPUTS: diagnostic (boolean), optional argument
        OUTPUTS: None. All output is to the screen.
        """
        # This code prints out a diagnostic version of the card con
        if diagnostic:
            print("Type of hand: {0}".format(self.hand_type))
            if len(self) == 0:
                print("No cards in the hand currently.", end='')
            else:
                print("Cards in Dealer's hand: ", end='')
                for card in self.cards:
                    print(card, end='')
            print("\nRemaining Attributes:")

            # These attributes exist in all classes and subclasses of Hand.
            print("\thas_ace = {0}".format(self.has_ace))
            print("\tsoft_score = {0}".format(self.soft_score))
            print("\thard_score = {0}".format(self.hard_score))

            # self.insurance is unique to Dealer's.
            print("\tinsurance = {0}".format(self.insurance))

            # self.busted exists in all classes and subclasses
            print("\tbusted = {0}".format(self.busted))
        else:
            if len(self) == 0:
                print("No cards have been dealt to the Dealer's hand yet.")
            else:
                print("Dealer's {0} hand: ".format(self.hand_type), end='')
                for card in self.cards:
                    if card == self.cards[0]:
                        print("hold ", end='')
                    else:
                        print(card, end='')
                # All Hand classes have a busted attribute.
                print("\n")
                if self.busted:
                    print("This hand has busted.")
                else:
                    print("This hand is still solvent.")
        return


class Player(object):
    '''
    The Player object is a computer player controlled by the Human Player. A
    player object is used to track the stake (money) this computer player has,
    the hands, if any, that this player is playing, and current total of all
    outstanding bets this player has, including insurance bets. It also tracks
    the relattve skill level of this computer player, as that controls which
    tables it can challenge. Player.hands is a dictionary of up to two Hands.

    Note: Bets on individual hands are attributes of class Hand and SplitHand.
    NOte: Player objects start with no Hand objects. All hands are removed at
    the end of each round. During a round, a Player can will have either one
    regular Hand or two Split Hands.

    Class Order Attributes:
        SKILL_TYPES = ('starter', 'adept', 'professional', 'master',
                       'high roller')

    Methods:
        __init__(name, skill, bank, reserve, table_min): This method requires
            a name, a string). For the other four arguments, there are default
            values. It uses these values to initialize the computer player.
        __str__(diagnostic): The argument defaults to False. This prints out
            the information on this computer player. Diagnostic mode prints
            out additional information.
        __len__: Returns the number of valid hands this Player still has.
        __del__(diagnostic): The argument defaults to False. Prints o message
            when a player breaks their bank with no reserve. Diagnostic movde
            prints more information.
        create_hand(type, ante, which_hand, start_card): This method creates
            an empty regular hand by default (type = 'regular', which_hand =
            'one', start_card = None). It can create a DealerHand if type =
            'deealer' is specified. In that case, all other arguments are set
            to None. If a SplitHand is required, which_hand and start_card
            MUST be specified. For Hand and SplitHand objects, ante is a
            required argument.
        add_card_to_hand(card, which_hand): card must be a Card or Ace object.
            which_hand defaults to 'one'. This method returns True if the hand
            remains solvent, False if it busts.
        split_check(): Returns the value of hands['one'].has_pair.
        split_hand(hands['one]): This method takes the original hand (a pair)
            and splits it up into two SplitHand objects. It prompts the human
            player for an ante for this new hand. It removes the original hand
            frorm the game.
        update_bet(amt, which_hand,table_max): amt is a required value.
            which_hand defaults to 'one', table_max to 0. table_max is the
            maximum value allowed for any final bet. It also checks the bet
            on the Hand since bets cannot be raised to more than double the
            original ante. Sometables hove no max. So, table_max=0 means the
            max will be ignored.

    Attributes:
        name: a string. There is no default valur for it. It must be supplied
            to __init__().
        skill_level: string, restricted to values in SKILL_TYPES. Default is
            'starter'.
        reserve: integer. This is the money the human player opted to have
            this computer player hold in reserve to avoid removal from the
            game. Default is 0.
        bank: integer. This is the amount of money this computer player can use
            to plave bets. No default or starting value.
        insurance_bet: integer. Normally set to None unless the player decides
            to place an insurance bet, if one could be made during the current
            round. Default None,.
        total_bets: integer. Total of all bets places, including insurance
            bets. Starts each round as None and returns to None once all bets
            have been resolved. Cannot exceed the computer player's bank.
        hands: A dictionary of Hand objects. Can consist of one regular Hand,
            addressed as hands['one'] or two SplitHand objects, addressed as
            hands['one'] or hands['two']. Starts with each Hand set to None.
            Each hand is reset to None.
    '''

    # Class Order Attributes:
    SKILL_TYPES = ('starter', 'adept', 'professional', 'master', 'high roller')

    def __init__(self, name, skill='starter', bank=10000, reserve=0, table_min=10):
        """
        This method initializes the Player object's at attributes using the
        values supplied in the arguments. For a starting player, all of the
        defaults are used. Only a player name is required.
        INPUTS: name, string (required). skill. string that must match a value
            in SKILL_TYPES (optional, defaults to 'starter'). bank, integer
            (optional, default is 10000). reserve, integer (optional default
            is 0). table_min, integer (optional, default is 10).
        OUTPUTS: a Player object
        """

        # The name is a required argument, but we can render it a string.
        self.name = str(name)
        # skill_level must be a choice in SKILL_TYPES. If not, we raise a
        # ValueError. Since this constant does not exist yet, we need to create
        # a local copy for the purpose of instantiating the object.
        skills = ('starter', 'adept', 'professional', 'master', 'high roller')
        if skill in skills:
            self.skill_level = skill
        else:
            raise ValueError("Pleyer.__init__(): {0} is an invalid choice".format(skill))
        # Reserve must be less than the bank or the player cannot play. In
        # reality, it also needs to be small enough to allow the player to ante
        # up at the start of their turn.
        if reserve > bank - table_min:
            raise ValueError("Player.__init__(): reserve is too large.")
        else:
            self.bank = bank - reserve
            self.reserve = reserve
        self.total_bets = None
        self.insurance_bet = None
        self.hands = {'one': None, 'two': None}

    def __str__(self, diagnostic=False):
        """
        This method prints out the player's name, bank, reserve, hand, and
        insurance bets. In diagnoistic mode, adds a diagnostic header to the
        output and requests diagnostic output from the Hands. This method can
        tell if it is called for a regular player or a dealer.
        INTPUTS: diagnostic, boolean (optiona, default is False).
        OUTPUTS: None, All output is to the terminal screen.
        """
        if type(self) == Player:
            if not diagnostic:
                print(f"Player: {self.name}")
                print("Remaining Bank: ${:,}".format(self.bank))
                print("Cash Reserve: ${:,}".format(self.reserve))
                print(f"Skill Level: {self.skill_level}")
                if self.hands['one'] is not None:
                    print(self.hands['one'])
                if self.hands['two'] is not None:
                    print(self.hands['two'])
            else:  # This is a diagnostic printout.
                print(f"Diagnostic printout for {self.name}")
                print("Bank contains ${:,}, with a cash reserve of ${:,}.".format(self.bank, self.reserve))
                print(f"Skill level is {self.skill_level}.")
                print("Players hands are:")
                if self.hands['one'] is not None:
                    self.hands['one'].__str__(diagnostic=True)
                else:
                    print("First hand does not exist.")
                if self.hands['two'] is not None:
                    self.hands['two'].__str__(diagnostic=True)
                else:
                    print("Second hand does not exist.")
        else:  # This is a dealer.
            pass
        return ""

    def __len__(self):
        """
        This method returns the number of remaining valid Hand objects that the
        Player object still has.
        INPUTS: None
        OUTPUTS: nunber of valid Hand objects, integer [0,2]
        """
        # Initialize the counter.
        hand_ctr = 0
        # Increment the counter if the Hand exist and is not busted.
        if self.hands['one'] is not None:
            if not self.hands['one'].busted:
                hand_ctr += 1
        if self.hands['two'] is not None:
            if not self.hands['two'].busted:
                hand_ctr += 1
        # Return the value in the counter.
        return hand_ctr
