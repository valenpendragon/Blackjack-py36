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
        SubClass DealerHand: A hand specifically designed for the dealer.
        
    Class Player: Stores the hand(sd), bet(s), and bank status of each player
        SubClass Dealer: Stores the hand of the dealer.

@author: Jeffrey Scott
"""

