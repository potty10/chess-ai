import chess
import chess.polyglot
import sys
import os
from typing import Callable
import random
import time 

sys.path.append(os.path.dirname(__file__))
from heuristics import *

WIN_VALUE = 9999999
DRAW_VALUE = 0

# https://gibberblot.github.io/rl-notes/single-agent/mcts.html
# https://medium.com/@_michelangelo_/monte-carlo-tree-search-mcts-algorithm-for-dummies-74b2bae53bfa
# https://int8.io/monte-carlo-tree-search-beginners-guide/#Monte_Carlo_Tree_Search_8211_basic_concepts
# Also reference Barton and Sutton on MTCS

# In a game of chess, the only rewards are win = 1, loss = -1, draw = 0
class Node():
    def __init__(
        self,
        mdp,
        parent,
        state,
        qfunction,
        bandit,
        reward=0.0,
        action=None,
    ):
        self.mdp = mdp
        self.parent = parent
        self.state: chess.Board = state
        self.id = Node.next_node_id
        Node.next_node_id += 1

        # The Q function used to store state-action values
        self.qfunction = qfunction

        # A multi-armed bandit for this node
        self.bandit = bandit

        # The immediate reward received for reaching this state, used for backpropagation
        self.reward = reward

        # The action that generated this node
        self.action = action

        # A dictionary from actions to a set of node-probability pairs
        self.children = {}

    """ Return true if and only if all child actions have been expanded """

    def is_fully_expanded(self):
        valid_actions = self.mdp.get_actions(self.state)
        if len(valid_actions) == len(self.children):
            return True
        else:
            return False

    """ Select a node that is not fully expanded """

    def select(self):
        if not self.is_fully_expanded() or self.mdp.is_terminal(self.state):
            return self
        else:
            actions = list(self.children.keys())
            action = self.bandit.select(self.state, actions, self.qfunction)
            return self.get_outcome_child(action).select()

    """ Expand a node if it is not a terminal node """

    def expand(self):
        if not self.mdp.is_terminal(self.state):
            # Randomly select an unexpanded action to expand
            actions = self.mdp.get_actions(self.state) - self.children.keys()
            action = random.choice(list(actions))

            self.children[action] = []
            return self.get_outcome_child(action)
        return self

    """ Backpropogate the reward back to the parent node """

    def back_propagate(self, reward, child):
        action = child.action

        Node.visits[self.state] = Node.visits[self.state] + 1
        Node.visits[(self.state, action)] = Node.visits[(self.state, action)] + 1

        q_value = self.qfunction.get_q_value(self.state, action)
        delta = (1 / (Node.visits[(self.state, action)])) * (
            reward - self.qfunction.get_q_value(self.state, action)
        )
        self.qfunction.update(self.state, action, delta)

        if self.parent != None:
            self.parent.back_propagate(self.reward + reward, self)

    """ Simulate the outcome of an action, and return the child node """

    def get_outcome_child(self, action):
        # Choose one outcome based on transition probabilities
        (next_state, reward, done) = self.mdp.execute(self.state, action)

        # Find the corresponding state and return if this already exists
        for (child, _) in self.children[action]:
            if next_state == child.state:
                return child

        # This outcome has not occured from this state-action pair previously
        new_child = Node(
            self.mdp, self, next_state, self.qfunction, self.bandit, reward, action
        )

        # Find the probability of this outcome (only possible for model-based) for visualising tree
        probability = 0.0
        for (outcome, probability) in self.mdp.get_transitions(self.state, action):
            if outcome == next_state:
                self.children[action] += [(new_child, probability)]
                return new_child



class MCTSAgent:

    def __init__(self, name, depth=2):
        self.name = name
        self.depth = depth
        self.eval_func = larry_kaufman_piece_sum

        # self.mdp = mdp
        # self.qfunction = qfunction
        # self.bandit = bandit

    """The main Monte Carlo Tree Search algorithm"""

    def mcts(self, board, timeout=20):
        root_node = Node(None, board)
        current_color = board.turn
        start_time = time.time()
        current_time = time.time()
        while current_time < start_time + timeout:

            # Find a state node to expand
            selected_node = root_node.select()
            if not self.mdp.is_terminal(selected_node):

                child = selected_node.expand()
                reward = self.simulate(child, current_color)
                selected_node.back_propagate(reward, child)

            current_time = time.time()

        return root_node

    """ Simulate until a terminal state """

    def simulate(self, node, player_color):
        board = node.state.copy()

        while board.outcome() == None:
            # Choose an action to execute
            move = random.choice(list(board.legal_moves))

            # Execute the action
            board.push(move)

        if board.outcome().winner == None:
            return 0
        elif board.outcome().winner == player_color:
            return 1
        else:
            return -1
