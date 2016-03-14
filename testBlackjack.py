from __future__ import division
import unittest
import Blackjack as BJ
import numpy as np
import random



class test_Dealer(unittest.TestCase):
	def setUp(self):
		self.Dealer = BJ.Dealer()

	def test__new_card(self):
		for element in range(100):
			self.assertTrue(isinstance(self.Dealer._new_card(),int))
			self.assertTrue(self.Dealer._new_card()<12)
			self.assertTrue(self.Dealer._new_card()>0)

	def test_get_first_card(self):
		self.assertTrue(isinstance(self.Dealer.get_first_card(),int))
		self.assertTrue(self.Dealer.get_first_card()<12)
		self.assertTrue(self.Dealer.get_first_card()>0)

	def test_get_all_cards(self):
		self.assertTrue(isinstance(self.Dealer.get_all_cards(),int))
		self.assertTrue(self.Dealer.get_all_cards()>=17)
		self.assertTrue(self.Dealer.get_all_cards()<=30)

	def test__extra_cards(self):
		for key in [17,18,19,20,21]:
			self.assertEqual(self.Dealer._extra_cards(key),key)
		for key in range(16):
			self.assertTrue(self.Dealer._extra_cards(key)>key)

	def test_set_first_card(self):
		for key in [2,3,4,5,6,7,8,9,10,11]:
			self.Dealer.set_first_card(key)
			self.assertTrue(self.Dealer.get_all_cards()>=13)
			self.assertTrue(self.Dealer.get_all_cards()<=31)

class testPlayer(unittest.TestCase):
	def setUp(self):
		self.Player_1 = BJ.Player()
		self.Player_2 = BJ.Player(number_aces=1)
	
	def test_get_first_hand(self):
		for element in range(100):
			self.assertTrue(self.Player_1._first_hand(0)>=12)
			self.assertTrue(self.Player_1._first_hand(0)<=21)
			self.assertTrue(self.Player_2._first_hand(0)>=12)
			self.assertTrue(self.Player_2._first_hand(0)<=21)			

	def test_hit(self):
		for element in range(100):
			self.Player1 = BJ.Player()
			self.Player2 = BJ.Player(1)
			self.assertTrue(self.Player1.hit()>=13)
			self.assertTrue(self.Player2.hit()<=31)

	def test_set_first_hand(self):
		for element in range(100):
			self.Player1 = BJ.Player()
			self.Player2 = BJ.Player(1)
			for key in [12,13,14,15,16,17,18,19,20,21]:
				self.Player1.set_first_hand(key)
				self.Player2.set_first_hand(key)

				self.assertTrue(self.Player1.hit()>=13)
				self.assertTrue(self.Player2.hit()<=31)		


class testPlay(unittest.TestCase):
	def test_Play(self):
		self.assertEqual(BJ.Play(22,22),-1)
		self.assertEqual(BJ.Play(22,20),-1)
		self.assertEqual(BJ.Play(18,22),1)
		self.assertEqual(BJ.Play(18,17),1)
		self.assertEqual(BJ.Play(17,21),-1)
		self.assertEqual(BJ.Play(17,17),0)


class testEvaluation(unittest.TestCase):
	def setUp(self):
		self.policy1 = np.zeros((10,10))
		for i in [9,8,7,6]:
			for j in range(10):
				self.policy1[i,j] = 1

	def test_sepicific_evaluation(self):
		for keyP in [12,13,14,15,16,17,18,19,20,21]:
			for keyD in [2,3,4,5,6,7,8,9,10,11]:
				policy = np.zeros((10,10))
				E1 = BJ.Evaluation(0,policy)
				policy[keyP-12,keyD-2] = 1
				E2 = BJ.Evaluation(0,policy)

				E1.specific_evaluate(keyP,keyD)
				E2.specific_evaluate(keyP,keyD)
				
				# Check N
				self.assertEqual(E1.get_N()[keyP-12,keyD-2],1)
				self.assertEqual(E2.get_N()[keyP-12,keyD-2],1)

				# Check G
				self.assertTrue(abs(E1.get_G()[keyP-12,keyD-2])==1 or E1.get_G()[keyP-12,keyD-2]==0)
				self.assertTrue(abs(E2.get_G()[keyP-12,keyD-2])==1 or E2.get_G()[keyP-12,keyD-2]==0)

				# Check V
				self.assertTrue(abs(E1.get_G()[keyP-12,keyD-2])<=1)
				self.assertTrue(abs(E2.get_G()[keyP-12,keyD-2])<=1)

	def test_policy_play(self):
		E = BJ.Evaluation(0,self.policy1)
		
		P = BJ.Player(0)

		for key in [18,19,20,21]:
			P.set_first_hand(key)
			X = E.policy_play(P,P.get_all_cards(),10)
			self.assertEqual(X.get_all_cards(),key)

		for key in [12,13,14,15,16,17]:
			P.set_first_hand(key)
			X = E.policy_play(P,P.get_all_cards(),10)
			self.assertTrue(X.get_all_cards()>key)



	def test_specific_run(self):
		number_run = 100

		E1 = BJ.Evaluation(0,policy=self.policy1)
		E2 = BJ.Evaluation(1,policy=self.policy1)

		for i in [12,12,13,14,15,16,17,18,19,20,21]:
			for j in [2,3,4,5,6,7,8,9,10,11]:
				E1.specific_run(number_run,i,j)
				E2.specific_run(number_run,i,j)
			#print("Progress: " +str((i-11)*10) + "%")
		
class testBestPractice(unittest.TestCase):
	def setUp(self):
		self.policy1 = np.zeros((10,10))
		for i in [9,8,7,6]:
			for j in range(10):
				self.policy1[i,j] = 1	

	def test__policy_play(self):
		BP = BJ.BestPractice(0)
		
		P = BJ.Player(0)

		for key in [12,13,14,15,16,17,19,20,21]:
			P.set_first_hand(key)
			X = BP._policy_play(P,P.get_first_hand(),10,1)
			self.assertTrue(X.get_all_cards()>=key)



	def test__improve_policy(self):
		BP = BJ.BestPractice(1)
		
		P = BJ.Player(0)

		i = random.randint(12,21)
		j = random.randint(2,11)

		BP._improve_policy(i,j)

		Policy = BP.get_policy()

		

		Policy[i-12,j-2] -= 1

		# for k in range(10):
		# 	for l in range(10):
				#self.assertEqual(Policy[k,l],1)

	def test__specific_run(self):
		BP = BJ.BestPractice(number_aces = 1)


		BP._specific_run(self.policy1,21,10,1,[[1,21,10]])

		

	def test_run_all_possibilities(self):
		number_run = 100000

		BP = BJ.BestPractice(0)
		BP.run_all_possibilities(number_run)
		self.assertTrue(sum(sum(sum(BP.get_N())))>=(number_run-1)*10*10)

		print(BP.get_Q())
		print(BP.get_policy())


	def test_run_one_possibility(self):
		number_run = 100000000
		BP = BJ.BestPractice(0)
		BP.run_one_possibility(number_run,12,5)

		print(BP.get_Q())
		print(BP.get_policy())

unittest.main()
