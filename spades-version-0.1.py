# SPADES

import random
import time

SPADES = u'\u2660'
CLUBS = u'\u2663'
HEARTS = u'\u2661'
DIAMONDS = u'\u2662'


SUITS = ['D', 'C', 'H', 'S']
CARD_NUMBERS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
BLANK_CARD = '[  ]'

def list_to_string(lst):
	return "".join([str(x) for x in lst])

def generate_all_cards():
	deck = []
	for suit in SUITS:
		for card_number in CARD_NUMBERS:
			deck.append(Card(suit, card_number))
	return deck


def display_instructions():
	print("""

	\t\t\t -----------------------
					SPADES 
	\t\t\t -----------------------

	  To play a card, simply type in the number of the card 
	  followed by the first letter of its suit.

	  For example, to play the Ace of Spades, type in 'as' or 'AS'. 

	  You are Player 3 and your teammate is Player 1. Good luck!
	  \n"""

		)
	

class Card():
	def __init__(self, suit, number):
		self.suit = suit
		self.number = number

	@staticmethod
	def from_code(raw_code):
		code = raw_code.upper()
		return Card(code[-1], code[0:-1])

	def __str__(self):
		if self.suit == 'S':	
			return "[{}{}]".format(self.number, SPADES)
		elif self.suit == 'C':
			return "[{}{}]".format(self.number, CLUBS)
		elif self.suit == 'H':
			return "[{}{}]".format(self.number, HEARTS)
		elif self.suit == 'D':
			return "[{}{}]".format(self.number, DIAMONDS)

	def __eq__(self, other):
		return ((self.suit == other.suit) and (self.number == other.number))

	def __gt__(self, other):
		if self.suit != other.suit:
			return SUITS.index(self.suit) > SUITS.index(other.suit)
		else:
			return CARD_NUMBERS.index(self.number) > CARD_NUMBERS.index(other.number)

	def get_suit(self):
		return self.suit

	def get_number(self):
		return self.number


class Deck():
	def __init__(self):
		self.deck = generate_all_cards()

	def shuffle(self):
		random.shuffle(self.deck)

	def get_cards(self, low, high):
		return self.deck[low:high]

	def __str__(self):
		return "{" + list_to_string(self.deck) + "}"



class Hand():
	def __init__(self, deck, low, high):
		self.hand = sorted(deck.get_cards(low, high))

	def get_card_index(self, card):
		return self.hand.index(card)

	def display(self):
		print("<" + list_to_string(self.hand) + ">")
	
	def update_hand(self, new_hand):
		self.hand = new_hand
		return self.hand

	def get_card(self, index):
		return self.hand[index]

	def remove_card(self, card):
		self.hand.remove(card)

	def highest_card_in_suit(self, suit):
		highest_seen = None
		for card in self.hand:
			if card.suit == suit:
				if not highest_seen:
					highest_seen = card
				elif card > highest_seen:
					highest_seen = card
		return highest_seen

	def has_spade(self):
		has_spade = False
		for card in self.hand:
			if card.suit == 'S':
				has_spade = True
		return has_spade

	def lowest_card_in_suit(self, suit):
		lowest_seen = None
		for card in self.hand:
			if card.suit == suit:
				if not lowest_seen:
					lowest_seen = card
				elif card < lowest_seen:
					lowest_seen = card
		return lowest_seen	

	def has_starting_suit(self, suit):
		has_suit = False
		for card in self.hand:
			if card.suit == suit:
				has_suit = True
		return has_suit

	def __str__(self):
		return "<" + list_to_string(self.hand) + ">"

	def __iter__(self):
		return self.hand.__iter__()

class Bags():

	def __init__(self, team):
		self.bags = 0
		self.team = team

	def __str__(self):
		return str(self.bags)

	def get_bags(self):
		if self.team.made_bid():
			self.bags = self.team.trick - self.team.bid
		else:
			self.bags = 0
		return self.bags

	def raw_bid_count(self):
		old_bags = self.bags
		self.bags = old_bags + self.get_bags()
	
	def update_bags(self, board):
		self.bags = self.bags % 10
		if self.team.number == 1:
			board.team1_bags = self.bags
		else:
			board.team2_bags = self.bags

	def has_gone_over(self):
		self.raw_bid_count()
		return self.bags >= 10


class Trick():
	def __init__(self):
		self.trick = []

	def update_trick(self, card):
		self.trick.append(card)

	def has_spade(self):
		has_spade = False
		for card in self.trick:
			if card.suit == 'S':
				has_spade = True
		return has_spade

	def get_highest_card_in_suit(self, suit):
		highest_seen = None
		for card in self.trick:
			if card.suit == suit:
				if not highest_seen:
					highest_seen = card
				elif card > highest_seen:
					highest_seen = card
		return highest_seen	

	def get_winning_card(self, suit):
		if self.has_spade():
			return self.get_highest_card_in_suit('S')
		else:
			return self.get_highest_card_in_suit(suit)

	def clear_tricks(self):
		self.trick = []


class Player():
	def __init__(self):
		self.is_starting = False
		self.hand = None
		self.bid = 0
		self.trick = 0

	def reset_bid_and_trick(self):
		self.trick = 0
		self.bid = 0

	def gone_nil(self):
		return int(self.bid) == 0

	def is_starting_player(self):
		return self.is_starting

	def make_starting_player(self):
		self.is_starting = True

	def make_not_starting_player(self):
		self.is_starting = False


	def update_hand(self, hand, board):
		self.hand = hand
		board.player_hand = self.hand

	def update_bid(self, bid, board):
		self.bid = bid
		board.player_bid = self.bid

	def increase_trick_count(self, board):
		self.trick += 1
		board.player_trick_count = self.trick

	def update_trick_count(self, board):
		board.player_trick_count = self.trick

	def play_card(self, card, board):
		board.card_south = card

	def get_bid(self):
		while True:
			try:
				bid = int(input("What is your bid? "))
				break
			except ValueError:
				print("Opps! A bid must be a number! ")
		return bid

	def get_move(self):
		while True:
			try:
				code = input("What card do you want to play? ")	
				move = Card.from_code(code)
				break
			except IndexError:
				print("Opps! A card is the number followed by first letter of its suit. ")
		return move

	def display_win(self, card):
		print("You won the trick by playing the {}. ".format(card))

	def is_legal_move(self, card, suit=None):
		if card in self.hand:
			if suit == None:
				return True
			elif self.hand.has_starting_suit(suit):
				if card.suit == suit:
					return True
			else:
				return True





class ComputerPlayer(Player):
	def __init__(self, seat):
		self.seat = seat
		self.is_starting = False
		self.hand = None
		self.bid = 0
		self.trick = 0

	def update_hand(self, hand):
		self.hand = hand

	def get_move(self, suit=None):
		if self.is_starting:
			return self.hand.get_card(0)
		elif self.hand.has_starting_suit(suit):
			return self.hand.highest_card_in_suit(suit)
		elif self.hand.has_spade():
			return self.hand.lowest_card_in_suit('S')
		else:
			return self.hand.get_card(0)

	def get_bid(self):
		bid = 0
		for card in self.hand:
			if card.suit == 'S':
				self.bid += 1
		# if bid == 0:
		# 	self.bid += 1
			# elif card.number == 'A':
			# 	self.bid += 1
			# elif card.number == 'K':
			# 	self.bid += 1
		return bid

	def update_bid(self, bid, board):
		self.bid = bid
		if self.seat == 'north':
			board.c_north_bid = self.bid
		elif self.seat == 'west':
			board.c_west_bid = self.bid
		elif self.seat == 'east':
			board.c_east_bid = self.bid

	def update_trick_count(self, board):
		if self.seat == 'north':
			board.c_north_trick_count = self.trick
		elif self.seat == 'west':
			board.c_west_trick_count = self.trick
		elif self.seat == 'east':
			board.c_east_trick_count = self.trick

	def increase_trick_count(self, board):
		self.trick += 1
		if self.seat == 'north':
			board.c_north_trick_count = self.trick
		elif self.seat == 'west':
			board.c_west_trick_count = self.trick
		elif self.seat == 'east':
			board.c_east_trick_count = self.trick

	def play_card(self, card, board):
		if self.seat == 'north':
			board.card_north = card
		elif self.seat == 'west':
			board.card_west = card
		elif self.seat == 'east':
			board.card_east = card

	def won_trick(self, card):
		return card in self.hand

	def display_win(self, card):
		print("{} won the trick by playing the {}. ".format(self, card))

	def  __str__(self):
		if self.seat == 'north':
			return "Player 1"
		elif self.seat == 'west':
			return "Player 4"
		elif self.seat == 'east':
			return "Player 2"


class Score():
	def __init__(self, team, bags):
		self.score = 0
		self.bags = bags
		self.team = team

	def __str__(self):
		return str(self.score)

	def get_score(self):		
		team_score = self.score
		if self.team.made_nil():
			team_score += 100
		elif self.team.failed_nil():
			team_score -= 100

		if self.team.made_bid():
			team_score += (self.team.bid * 10)
		else:
			team_score -= (self.team.bid * 10)	
		
		if self.bags.has_gone_over():
			team_score -= 100

		self.score = team_score
		return self.score

	def update_score(self, board):
		if self.team.number == 1:
			board.team1_score = self.score
		else:
			board.team2_score = self.score

	def has_winning_score(self, game_score):
		return self.score >= game_score


class Team():
	
	def __init__(self, player_1, player_2, number):
		self.number = number
		self.player_1 = player_1
		self.player_2 = player_2
		self.bid = 0
		self.trick = 0

	def get_bid(self):
		team_bid = int(self.player_1.bid) + int(self.player_2.bid)
		return team_bid

	def update_bid(self):
		self.bid = self.get_bid()

	def failed_nil(self):
		return ((self.player_1.gone_nil() and self.player_1.trick != 0)
		or (self.player_2.gone_nil() and self.player_2.trick != 0))

	def made_nil(self):
		return ((self.player_1.gone_nil() and self.player_1.trick == 0) 
		or (self.player_2.gone_nil() and self.player_2.trick == 0))

	def get_trick_count(self):
		team_trick_count = int(self.player_1.trick) + int(self.player_2.trick)
		return team_trick_count

	def made_bid(self):
		return self.get_bid() <= self.get_trick_count()

	def update_trick(self):
		self.trick = self.get_trick_count()

	def update_bags(self, bags, board):
		if self.number == 1:
			board.team1_bags = bags
		else:
			board.team2_bags = bags

		

class Board():

	def __init__(self, player_hand=None, round_count=1, c_north_bid=0, c_east_bid=0, 
		c_west_bid=0, c_north_trick_count=0, c_east_trick_count=0, c_west_trick_count=0, 
		player_bid=0, player_trick_count=0, team1_score=0, team2_score=0, team1_bags=0, 
		team2_bags=0, card_north=BLANK_CARD, card_south=BLANK_CARD, card_east=BLANK_CARD, 
		card_west=BLANK_CARD):

		self.round_count = round_count
		self.c_north_trick_count = c_north_trick_count
		self.c_east_trick_count = c_east_trick_count
		self.player_trick_count = player_trick_count
		self.c_west_trick_count = c_west_trick_count
		self.c_north_bid = c_north_bid
		self.c_east_bid = c_east_bid
		self.player_bid = player_bid
		self.c_west_bid = c_west_bid
		self.team1_score = team1_score
		self.team2_score = team2_score
		self.team1_bags = team1_bags
		self.team2_bags = team2_bags
		self.player_hand = player_hand
		self.card_north = card_north
		self.card_south = card_south
		self.card_east = card_east
		self.card_west = card_west
		self.score = 0

	def display(self):
		print( 
	"""
	\t\tRound:{}      --Team 1--         --Team 2--
	       \t\t\t  Score:{} Bags:{}     Score:{} Bags:{}
						
						PLAYER 1
						Bid: {}
						Tricks: {}

						    {}
\t\t\t\tPLAYER 4\t\t\tPLAYER 2
\t\t\t\tBid: {}\t\t{}\t{}\tBid: {}
\t\t\t\tTricks: {}\t\t\tTricks: {}
						    {}

						PLAYER 3
						Bid: {}
						Tricks: {}

			  {}

						""".format(self.round_count, self.team1_score, self.team1_bags, 
							self.team2_score, self.team2_bags, self.c_north_bid, 
							self.c_north_trick_count, self.card_north, self.c_west_bid, 
							self.card_west, self.card_east, self.c_east_bid, 
							self.c_west_trick_count, self.c_east_trick_count, 
							self.card_south, self.player_bid, self.player_trick_count, 
							self.player_hand))



	def update_round_count(self):
		self.round_count += 1

	def clear_cards(self):
		self.card_north = BLANK_CARD
		self.card_south = BLANK_CARD
		self.card_east = BLANK_CARD
		self.card_west = BLANK_CARD



class Game():
	
	def __init__(self, score_limit=250):
		self.deck = Deck()
		self.c1 = ComputerPlayer("north")
		self.c2 = ComputerPlayer('east')
		self.c4 = ComputerPlayer('west')
		self.player = Player()
		self.board = Board()
		self.trick = Trick()
		self.c1.make_starting_player()
		self.score_limit = score_limit
		self.team_1 = Team(self.c1, self.player, 1)
		self.team_2 = Team(self.c2, self.c4, 2)
		
		
		self.team_1_bags = Bags(self.team_1)
		self.team_2_bags = Bags(self.team_2)
		
		self.team_1_score = Score(self.team_1, self.team_1_bags)
		self.team_2_score = Score(self.team_2, self.team_2_bags)
		
		old_team_1_score = 0
		old_team_2_score = 0
		
		
		while self.board.score < self.score_limit:
			count = 13
			self.deck.shuffle()
			self.player.update_hand(Hand(self.deck, 0, 13), self.board)
			self.c1.update_hand(Hand(self.deck, 13, 26))
			self.c2.update_hand(Hand(self.deck, 26, 39))
			self.c4.update_hand(Hand(self.deck, 39, 52))
			self.board.display()

			self.c1.get_bid()
			self.c1.update_bid(self.c1.bid, self.board)
			self.board.display()
			
			self.c2.get_bid()
			self.c2.update_bid(self.c2.bid, self.board)
			self.board.display()
			
			player_bid = self.player.get_bid()
			self.player.update_bid(player_bid, self.board)
			self.board.display()

			self.c4.get_bid()
			self.c4.update_bid(self.c4.bid, self.board)
			self.board.display()

			while count > 0:
				if self.c1.is_starting:
					c1_move = self.c1.get_move()
					starting_suit = c1_move.get_suit()
					
					self.c1.play_card(c1_move, self.board)
					self.trick.update_trick(c1_move)
					self.board.display()
					self.c1.make_not_starting_player()

					c2_move = self.c2.get_move(starting_suit)
					self.c2.play_card(c2_move, self.board)
					self.trick.update_trick(c2_move)
					self.board.display()

					while True:
						player_move = self.player.get_move()
						if self.player.is_legal_move(player_move, starting_suit):
							self.player.play_card(player_move, self.board)
							self.trick.update_trick(player_move)
							self.player.hand.remove_card(player_move)
							self.board.display()
							break
						else:
							print("You must play a card in the starting suit, if you have it. ")
							

					c4_move = self.c4.get_move(starting_suit)
					self.c4.play_card(c4_move, self.board)
					self.trick.update_trick(c4_move)
					self.board.display()

				elif self.c2.is_starting:
					c2_move = self.c2.get_move()
					starting_suit = c2_move.get_suit()
					
					self.c2.play_card(c2_move, self.board)
					self.trick.update_trick(c2_move)
					self.board.display()
					self.c2.make_not_starting_player()

					while True: 
						player_move = self.player.get_move()
						if self.player.is_legal_move(player_move, starting_suit):
							self.player.play_card(player_move, self.board)
							self.trick.update_trick(player_move)
							self.player.hand.remove_card(player_move)
							self.board.display()
							break
						else:
							print("You must play a card in the starting suit, if you have it. ")

					c4_move = self.c4.get_move(starting_suit)
					self.c4.play_card(c4_move, self.board)
					self.trick.update_trick(c4_move)
					self.board.display()

					c1_move = self.c1.get_move(starting_suit)
					self.c1.play_card(c1_move, self.board)
					self.trick.update_trick(c1_move)
					self.board.display()


				elif self.player.is_starting:
					while True: 
						player_move = self.player.get_move()
						if self.player.is_legal_move(player_move):
							starting_suit = player_move.get_suit()
							self.player.play_card(player_move, self.board)
							self.trick.update_trick(player_move)
							self.player.hand.remove_card(player_move)
							self.board.display()
							self.player.make_not_starting_player()
							break
						else:
							print("You must play a card in the starting suit, if you have it. ")

					c4_move = self.c4.get_move(starting_suit)
					self.c4.play_card(c4_move, self.board)
					self.trick.update_trick(c4_move)
					self.board.display()

					c1_move = self.c1.get_move(starting_suit)
					self.c1.play_card(c1_move, self.board)
					self.trick.update_trick(c1_move)
					self.board.display()

					c2_move = self.c2.get_move(starting_suit)
					self.c2.play_card(c2_move, self.board)
					self.trick.update_trick(c2_move)
					self.board.display()


				elif self.c4.is_starting:
					c4_move = self.c4.get_move()
					starting_suit = c4_move.get_suit()
					self.c4.play_card(c4_move, self.board)
					self.trick.update_trick(c4_move)
					self.board.display()
					self.c4.make_not_starting_player()

					c1_move = self.c1.get_move(starting_suit)
					self.c1.play_card(c1_move, self.board)
					self.trick.update_trick(c1_move)
					self.board.display()

					c2_move = self.c2.get_move(starting_suit)
					self.c2.play_card(c2_move, self.board)
					self.trick.update_trick(c2_move)
					self.board.display()

					while True:
						player_move = self.player.get_move()
						if self.player.is_legal_move(player_move, starting_suit):
							self.player.play_card(player_move, self.board)
							self.trick.update_trick(player_move)
							self.player.hand.remove_card(player_move)
							self.board.display()
							break
						else:
							print("You must play a card in the starting suit, if you have it. ")

				
				winning_card = self.trick.get_winning_card(starting_suit)

				if self.c1.won_trick(winning_card):
					self.c1.increase_trick_count(self.board)
					self.c1.make_starting_player()
					self.c1.display_win(winning_card)
					input("<<PRESS ENTER>>")

				elif self.c2.won_trick(winning_card):
					self.c2.increase_trick_count(self.board)
					self.c2.display_win(winning_card)
					input("<<PRESS ENTER>>")
					self.c2.make_starting_player()

				elif self.c4.won_trick(winning_card):
					self.c4.display_win(winning_card)
					input("<<PRESS ENTER>>")
					self.c4.increase_trick_count(self.board)
					self.c4.make_starting_player()

				else:
					self.player.increase_trick_count(self.board)
					self.player.make_starting_player()
					self.player.display_win(winning_card)
					input("<<PRESS ENTER>>")
					self.board.clear_cards()
					self.board.display()

				self.c1.hand.remove_card(c1_move)
				self.c2.hand.remove_card(c2_move)
				self.c4.hand.remove_card(c4_move)
				self.trick.clear_tricks()
				self.board.clear_cards()
				count -= 1

			print("ROUND OVER")
			self.team_1.update_bid()
			self.team_1.get_trick_count()
			self.team_1.update_trick()

			self.team_2.update_bid()
			self.team_2.get_trick_count()
			self.team_2.update_trick()

			new_team_1_score = self.team_1_score.get_score()
			self.team_1_score.update_score(self.board)

			new_team_2_score = self.team_2_score.get_score()
			self.team_2_score.update_score(self.board)
			
			round_score_team_1 = new_team_1_score - old_team_1_score
			round_score_team_2 = new_team_2_score - old_team_2_score
			self.team_1_bags.update_bags(self.board)
			self.team_2_bags.update_bags(self.board)
			print('Team 1 scored {} points and gained {} bags. Team 2 scored {} points and gained {} bags. '
				.format(round_score_team_1, self.team_1_bags, round_score_team_2, self.team_2_bags))
			self.board.display()
			
			if ((self.team_1_score.has_winning_score(self.score_limit)) and 
				(self.team_1_score.score > self.team_2_score.score)):
				print("Team 1 wins! ")
				break
			elif ((self.team_2_score.has_winning_score(self.score_limit)) and 
				(self.team_2_score.score > self.team_1_score.score)):
				print("Team 2 wins! ")
				break

			input("<<PRESS ENTER>>")

			old_team_1_score = new_team_1_score
			old_team_2_score = new_team_2_score
			
			self.c1.reset_bid_and_trick()
			self.c1.update_trick_count(self.board)
			self.c1.update_bid(self.c1.bid, self.board)
			
			self.c2.reset_bid_and_trick()
			self.c2.update_trick_count(self.board)
			self.c2.update_bid(self.c2.bid, self.board)
			
			self.c4.reset_bid_and_trick()
			self.c4.update_trick_count(self.board)
			self.c4.update_bid(self.c4.bid, self.board)
			
			self.player.reset_bid_and_trick()
			self.player.update_trick_count(self.board)
			self.player.update_bid(self.player.bid, self.board)

			self.board.update_round_count()


		print("GAME OVER")


display_instructions()
input("Press Enter to get start game. ")
g = Game(250)









