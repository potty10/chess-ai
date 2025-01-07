import chess
import chess.polyglot
import sys
import os
from typing import Callable
import random
import time 
from math import sqrt, log
from collections import defaultdict
from pprint import pprint
import chess.polyglot
from chess.polyglot import zobrist_hash

sys.path.append(os.path.dirname(__file__))
from heuristics import *

# https://gibberblot.github.io/rl-notes/single-agent/mcts.html
# https://medium.com/@_michelangelo_/monte-carlo-tree-search-mcts-algorithm-for-dummies-74b2bae53bfa
# https://int8.io/monte-carlo-tree-search-beginners-guide/#Monte_Carlo_Tree_Search_8211_basic_concepts
# Also reference Barton and Sutton on MTCS

# In a game of chess, the only rewards are win = 1, loss = -1, draw = 0
# qfunction is a map from (state, action) to expected rewards, or q value. We store it as a table.

def hash(state, a):
    return (chess.polyglot.zobrist_hash(state), a)

class Node():
    # Class variables
    visits = defaultdict(lambda: 0) # Number of times each state was visited

    def __init__(
        self,
        parent,
        state,
        qtable, # Simply a dictionary from (q,s) to q-value or expected rewards (discounted for this version)
        reward=0.0,
        action=None,
    ):
        self.parent = parent
        self.state: chess.Board = state
        self.qtable = qtable

        # The immediate reward received for reaching this state, used for backpropagation
        self.reward = reward

        # The action that generated this node
        self.action = action

        # Array of (action, child_node) that has been explored
        self.children = []

        self.N = 0 # Number of times this is visited
        self.T = 0 # Total accumualated rewards
    

    """ Return true if and only if all child actions have been expanded """

    def is_fully_expanded(self):
        if len(list(self.state.legal_moves)) == len(self.children):
            return True
        else:
            return False

    """ Select a node that is not fully expanded """

    def select(self):
        if not self.is_fully_expanded() or self.state.outcome():
            return self
        else:
            best_actions = []
            actions = [a[0] for a in self.children]
            q_values = [self.qtable[hash(self.state, a)] for a in actions]
            max_q_value_of_actions = max(q_values)
            for i in range(len(q_values)):
                if q_values[i] == max_q_value_of_actions:
                    best_actions.append(actions[i])

            action = random.choice(best_actions)
            return self.get_outcome_child(action).select()

    """ Expand a node if it is not a terminal node """

    def expand(self):
        if not self.state.outcome():
            visited_actions = {a[0] for a in self.children}
            all_actions = set(self.state.legal_moves)
            
            # Randomly select an unexpanded action to expand
            actions = all_actions - visited_actions
            try:
                action = random.choice(list(actions))
            except Exception as e:
                pprint(self.state.turn)
                pprint(self.is_fully_expanded())
                print(self.state)
                pprint(self.children)
                pprint(list(self.state.legal_moves))
                raise e
            
            child = self.create_new_child(action)
            return child
        return self

    """ Backpropogate the reward back to the parent node """

    def back_propagate(self, reward, child):
        action = child.action

        Node.visits[hash(self.state, action)] += 1

        q_value = self.qtable[hash(self.state, action)]
        delta = (1 / (Node.visits[hash(self.state, action)])) * (
            reward - q_value
        )
        self.qtable[hash(self.state, action)] += delta

        if self.parent != None:
            self.parent.back_propagate(self.reward + reward, self)

    """ Simulate the outcome of an action, and return the child node """

    def create_new_child(self, action):
        board = self.state.copy()
        board.push(action)

        # This outcome has not occured from this state-action pair previously
        new_child = Node(
            self, board, self.qtable, 0, action
        )
        self.children.append((action, new_child))
        return new_child
    
    def get_outcome_child(self, action):
        # Find the corresponding child node and return if this already exists
        for next_action, child_node in self.children:
            if next_action == action:
                return child_node
            
        # Choose one outcome based on transition probabilities
        board = self.state.copy()
        board.push(action)

        # This outcome has not occured from this state-action pair previously
        new_child = Node(
            self, board, self.qtable, 0, action
        )
        self.children.append((action, new_child))
        return new_child

    def choose_best_action(self):
        
        ''' 
        Once we have done enough search in the tree, the values contained in it should be statistically accurate.
        We will at some point then ask for the next action to play from the current node, and this is what this function does.
        There may be different ways on how to choose such action, in this implementation the strategy is as follows:
        - pick at random one of the node which has the maximum visit count, as this means that it will have a good value anyway.
        '''
        
        # Choose the best action amongst the explored children? Or should non-explored children be given a chance? To encourage exploration
        best_actions = []
        actions = [a[0] for a in self.children]
        q_values = [self.qtable[hash(self.state, a)] for a in actions]
        max_q_value_of_actions = max(q_values)
        for i in range(len(q_values)):
            if q_values[i] == max_q_value_of_actions:
                best_actions.append(actions[i])

        action = random.choice(best_actions)
        
        return action

class MCTSAgent:

    def __init__(self, name):
        self.name = name
        self.qtable = defaultdict(lambda: 0)

    """The main Monte Carlo Tree Search algorithm"""

    def mcts(self, board, timeout=8):
        root_node = Node(None, board, self.qtable)
        current_color = board.turn
        start_time = time.time()
        current_time = time.time()
        while current_time < start_time + timeout:

            # Find a state node to expand
            selected_node = root_node.select() # Possible for selected node to be terminal
            if not selected_node.state.outcome():

                child = selected_node.expand()
                reward = self.simulate(child, current_color)
                selected_node.back_propagate(reward, child)
            
            current_time = time.time()

        return root_node.choose_best_action()
    
    def make_move(self, board):

        return self.mcts(board)

    """ Simulate until a terminal state """

    def simulate(self, node, player_color):
        board = node.state.copy()
        depth = 0

        while board.outcome() == None:
            # Choose an action to execute
            move = random.choice(list(board.legal_moves))

            # Execute the action
            board.push(move)
            depth += 1

        if board.outcome().winner == None:
            return 0
        elif board.outcome().winner == player_color:
            return 1 # Maybe scale by depth?
        else:
            return -1
