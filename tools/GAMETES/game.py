from __future__ import division
import re, sys, math, copy, time, random
import numpy as np
from copy import deepcopy
from itertools import product
sys.path.append('../../')
from tools.userError import userError
from NashEqFinder import NashEqFinder

class game(object):
    """
    This is a general class holding information for a N-player game 


    METHODS:
    -------
    find_NashEq: Find the pure strategy Nash equilibrium of the game

    Ali R. Zomorrodi - Daniel Segre lab @ BU
    Last updated: August-10-2015 
    """

    def __init__(self, game_name, players_names, players_strategies, payoff_matrix, players_strategiesDetails = None, pureNashEq = None, **additional_args):
       """
       INPUTS:    
       -------
                game_name: A string containing the name of the game 
                           (e.g., 'Prisoner;s dilemma') 
            players_names: A list of strings containing the name of game players
       players_strategies: A dictionary whose keys are the names of players and values are a
                           list of strings containing the names of strategies played by 
                           that player. Example:
                           {'player1':['strategy1','strategy2'],
                          'player2':['strategy1','strategy2','strategy3']}
       players_strategiesDetails: A diciotnary of dictionaries. The keys of the main dictionary 
                           are the names of  the game palyers. The values are another 
                           dictionary. The keys of this inner dictionary are the names of 
                           strategies that could be taken by that player  and the values can be any 
                           data type that the user may wish (such as a list, tuple, etc). 
                           This is particularly useful as sometimes a strategy invovles multiples 
                           simultaneous actions. For example, a  strategy by a microbial strain 
                           can be to produce three different compounds. In this case the exchange rxns 
                           correspondong to those three compounds can be used as the values 
                           of the inner dicitonary. Example:
                           {'player1':{'strategy1':['EX_m1','EX_m2',EX_m2'],
                           'strategy2':['Ex_m4']'},'player2':{'strategy1':['EX_m5'],
                           'strategy2':['EX_m6','EX_m7']}'} 
             payoff_matrix: Payoff matrix of the game. This is a dictionary whose keys are
                               Keys: Tuple of tuples where each inner tuple has two elements:
                                     The first element is the name of the player
                                     The second element is the name of the strategy. 
                                     Note that keys cannot be a dictionary or a list because pythong
                                     will complain if the keys are not tuples
                             Values: A dictionary with keys and values as follows:
                                     Keys: Name of the players
                                     Values: Their payoff
                             Example: If we have two players p1 and p2 and each can play strategies s1 or s2,
                                      then the payoff_matrix is as follows: 
                                      {(('p1','s1),('p2','s1')):{'p1':2,'p2':3},
                                      (('p1','s1'),('p2','s2')):{'p1':0,'p':1}}
               pureNashEq: Pure strategy Nash equilibria of the game. This is a list of 
                           tuples whose elements are the elements of the payoff matrix that 
                           are pure strategy Nash equilibria of the game. For example, for a 
                           two player game:
                           [('p1s1','pss2),('p1s3','p2s5')], where pNsM means the 
                           strtegey M played by player N 
          additional_args: Additoinal arguments, which are entered as normal but they are 
                           converted to a dictionary whose keys are the names of the arguments 
                           and values are the values of those arguments
       """

       # Game name 
       self.game_name = game_name

       # Names of the game players
       self.players_names = players_names[:]

       # Number of the game players
       self.numberOfPlayers = len(self.players_names) 

       # Players strategies 
       self.players_strategies = players_strategies.copy()

       # Strategy details 
       self.players_strategiesDetails = deepcopy(players_strategiesDetails)

       # Payoff matrix of the game
       # First check if the total number of elements of the payoff matrix is equal to the 
       # product of the number of strategies for each player. 
       # The set of all strategies based on payoff_matrix 
       strategy_set_payoff_matrix = payoff_matrix.keys()

       # The set of strategies based on players_strategies for different types of players      
       # Two-player game
       listOfStrategies = [] # This is a list of lists [[s1,s2],[s2,s3,s4],[s5,s6]]
       for player in self.players_names:
          listOfStrategies.append([(player,k) for k in self.players_strategies[player]]) 
       strategy_set = [k for k in product(*listOfStrategies)]
             
       if set(strategy_set_payoff_matrix).issubset(set(strategy_set)) and set(strategy_set).issubset(set(strategy_set_payoff_matrix)):
          self.payoff_matrix = deepcopy(payoff_matrix) 
       else:
          print 'Is strategy_set_payoff_matrix a subset of strategy_set? ',set(strategy_set_payoff_matrix).issubset(set(strategy_set)) 
          print 'Is strategy_set  a subset of strategy_set_payoff_matrix?',set(strategy_set).issubset(set(strategy_set_payoff_matrix))

          print '\nset(strategy_set_payoff_matrix) = ',set(strategy_set_payoff_matrix)
          print '\nset(strategy_set)',set(strategy_set),'\n'

          error_message = '**Error! The set of strategies given in the payoff matrix does not match those given for each player (missing or additional strategies in payoff matrix)'
          raise customError(error_message)

       # A list of tuples whose elements are the elements of the payoff matrix that are pure 
       # strategy Nash equilibria of the game. For example, for a two player game
       # [(('p1','s1'),('p2','s2')),(('p1','s3'),('p2','s5'))]
       self.pureNashEq = deepcopy(pureNashEq)

       # Additoinal arguments. Additional arguments should be entered as normal but they are 
       # converted to a dictionary whose keys are the names of the arguments and values are 
       # the values of  those arguments
       argnames = additional_args.keys()
       argvals = additional_args.values()
       for argname in argnames:
         exec "self." + argname + " = " +"additional_args['" + argname + "']"

    def find_NashEq(self,NashEq_type = 'pure', stdout_msgs = True):
        """
        Finds the Nash equilibrium of the game
        """
        NashEqFinder_inst = NashEqFinder(game = self,stdout_msgs = stdout_msgs, NashEq_type = NashEq_type)
        [Nash_equilibria,exit_flag] = NashEqFinder_inst.run()
        if NashEq_type.lower() == 'pure':
            self.pureNash_equilibria = Nash_equilibria
            self.pureNashEq_exitflag = exit_flag
        elif NashEq_type.lower() == 'mixed':
            self.mixedNash_equilibria = Nash_equilibria
            self.mixedNashEq_exitflag = exit_flag
