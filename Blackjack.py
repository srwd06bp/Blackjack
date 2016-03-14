from __future__ import division
import numpy as np 
import random
import math


class Game:
	def _new_card(self):
		possibilities = np.array([2,3,4,5,6,7,8,9,10,10,10,11])
		random_choice = int(math.ceil(random.random()*(len(possibilities)-1)))

		return(possibilities[random_choice])

class Dealer(Game):
	def __init__(self):
		self.number_aces = 0
		self.first_card = self._new_card()
		self._set_number_aces(self.first_card)
		self.sum_cards = self.first_card
		self.score = self._extra_cards(self.sum_cards)

	def get_first_card(self):
		return self.first_card

	def get_all_cards(self):
		return self.score

	def set_first_card(self,score):
		self.first_card = score
		self._set_number_aces(self.first_card)
		self.sum_cards = self.first_card
		self.score = self._extra_cards(self.sum_cards)

	def _set_number_aces(self,card):
		if card == 11:
			self.number_aces += 1

	def _extra_cards(self,first_cards):

		if first_cards >= 17:
			if first_cards <= 21:
				return first_cards
			else:
				if(first_cards<21 and self.number_aces>0):
					self.number_aces -= 1

					# Call the function again	
					return self_extra_cards(first_cards-10)
				else:
					return first_cards
		else:
			# Add an extra card on the game
			add_card = self._new_card()

			# Check whether the card is an ace
			self._set_number_aces(add_card)

			# Call the function again	
			return self._extra_cards(first_cards + add_card)

class Player(Game):
	def __init__(self,number_aces=0):
		self.number_aces = number_aces
		self.first_cards = self._first_hand(0)
		self.score = self.first_cards

	def get_first_hand(self):
		return self.first_cards

	def hit(self):
		new_card = self._new_card()

		if new_card == 11 and self.score >= 12:
			self.score += 1
			return self.score
		else:
			self.score += new_card
			return self.score

	def get_all_cards(self):
		return self.score

	def set_first_hand(self,score):
		self.first_cards = score
		self.score = self.first_cards

	def _first_hand(self,sum_cards):
		# Get two cards
		new_card = self._new_card()
		if sum_cards >= 12:
			return sum_cards
		else:
			if self.number_aces == 0:
				if new_card != 11:
					sum_cards += new_card
				return self._first_hand(sum_cards)
			else:
				if new_card == 11:
					return 12
				else:
					return 11 + new_card

def Play(Player_score,Dealer_score):
	if Player_score > 21:
		return -1
	else:
		if Dealer_score > 21:
			return 1
		else:
			if Player_score>Dealer_score:
				return 1
			elif Player_score==Dealer_score:
				return 0
			else:
				return -1

class Evaluation:
	def __init__(self,number_aces,policy):
		self.number_aces = number_aces
		self.policy = policy
		self.N = np.zeros((10,10))
		self.G = np.zeros((10,10))
		self.V = np.zeros((10,10))

	def get_N(self):
		return self.N

	def get_G(self):
		return self.G

	def get_V(self):
		return self.V

	def specific_run(self,number_samples,player_first_score,dealer_first_score):
		for element in range(number_samples):
			self.specific_evaluate(player_first_score,dealer_first_score)


	def specific_evaluate(self,player_first_score,dealer_first_score):
		P = Player(number_aces=self.number_aces)
		P.set_first_hand(player_first_score)

		D = Dealer()
		D.set_first_card(dealer_first_score)		


		P = self.policy_play(P, P.get_first_hand(),D.get_first_card())

		# Update score
		score = Play(P.get_all_cards(),D.get_all_cards())



		# Update N
		self.N[player_first_score-12,dealer_first_score-2] += 1
		# Update G
		self.G[player_first_score-12,dealer_first_score-2] += score

		# Update V
		self.V[player_first_score-12,dealer_first_score-2] = self.G[player_first_score-12,dealer_first_score-2]/self.N[player_first_score-12,dealer_first_score-2]


	def policy_play(self,P, player_score, dealer_score):
		if player_score > 21:
			return P
		else:
			if self.policy[player_score-12,dealer_score-2]==0:
				player_score = P.hit()
				return self.policy_play(P,player_score,dealer_score)
			else:
				return P


class BestPractice:
	def __init__(self,number_aces):
		self.N = np.zeros((2,10,10))
		self.Q = np.zeros((2,10,10))
		self.policy = np.zeros((10,10))
		self.number_aces = number_aces

	def get_policy(self):
		return self.policy


	def get_Q(self):
		return self.Q

	def get_N(self):
		return self.N

	def run_all_possibilities(self,number_episodes):
		progress = 0
		for k in xrange(1,number_episodes,1):		
			# Mesure progress
			if k*100/number_episodes > progress:
				print "Progress: " + str(round(k*100/number_episodes))+"%"
				progress += 1

			# run one episode
			for i in [12,13,14,15,16,17,18,19,20,21]:
				for j in [2,3,4,5,6,7,8,9,10,11]:
						self._specific_run(self.policy,i,j,0.1,[[1,i,j]])

	def run_one_possibility(self, number_episodes, i , j):
		progress = 0
		for k in xrange(1,number_episodes,1):		
			# Mesure progress
			if k*100/number_episodes > progress:
				print "Progress: " + str(round(k*100/number_episodes))+"%"
				progress += 1

				self._specific_run(self.policy,i,j,1/k,[[1,i,j]])

	def _specific_run(self,policy,player_first_score,dealer_first_score,epsilon,trajectories):
		

		P = Player(number_aces=self.number_aces)
		P.set_first_hand(player_first_score)

		D = Dealer()		
		D.set_first_card(dealer_first_score)
		
		#Play the game with the epsilon policy
		P = self._policy_play(P,P.get_first_hand(),dealer_first_score,epsilon)

		player_second_score = P.get_all_cards()

		#Get to know what action was taken
		if player_second_score == player_first_score:
			hit = 0
		else:
			hit = 1

		# update the lattest trajectories
		trajectories[len(trajectories)-1][0] = hit


		if hit == 1:
			trajectories.append([1,player_second_score,dealer_first_score])
			self._specific_run(policy,player_second_score,dealer_first_score,epsilon,trajectories)
		else:
			score = Play(player_second_score,D.get_all_cards())


			for trajectory in trajectories:
				key_hit = trajectory[0]
				key_player_score = trajectory[1]
				key_dealer_score = trajectory[2]
				
				if key_player_score <=21:

					self.N[key_hit,key_player_score-12,key_dealer_score-2] += 1

					self.Q[key_hit,key_player_score-12,key_dealer_score-2] += (score - self.Q[key_hit,key_player_score-12,key_dealer_score-2])/self.N[key_hit,key_player_score-12,key_dealer_score-2]

					self._improve_policy(key_player_score,key_dealer_score)

			# if trajectories[len(trajectories)-1][1] == 12 and trajectories[len(trajectories)-1][2]==5:
			# 	print(score)
			# 	print(trajectories)
			# 	print(D.get_all_cards())
			# 	print(self.Q[key_hit,key_player_score-12,key_dealer_score-2])
			# 	print(self.N[key_hit,key_player_score-12,key_dealer_score-2])
			# 	print("ok")
	def _policy_play(self,P, player_score, dealer_score,epsilon):
		
		proba = random.random()


		if player_score <= 21:
			if self.policy[player_score-12,dealer_score-2]==1:
				if epsilon < proba:
					P.hit()
			else:
				if epsilon > proba:
					P.hit()
		return P
	
		

	def _improve_policy(self,player_first_score, dealer_first_score):
		if self.Q[1,player_first_score-12,dealer_first_score-2]>=self.Q[0,player_first_score-12,dealer_first_score-2]:
			self.policy[player_first_score-12,dealer_first_score-2] = 1
		else:
			self.policy[player_first_score-12,dealer_first_score-2] = 0	







