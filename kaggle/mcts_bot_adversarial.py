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
from chess.polyglot import zobrist_hash

# https://gibberblot.github.io/rl-notes/single-agent/mcts.html
# https://medium.com/@_michelangelo_/monte-carlo-tree-search-mcts-algorithm-for-dummies-74b2bae53bfa
# https://int8.io/monte-carlo-tree-search-beginners-guide/#Monte_Carlo_Tree_Search_8211_basic_concepts
# Also reference Barton and Sutton on MTCS

# In a game of chess, the only rewards are win = 1, loss = -1, draw = 0
# qfunction is a map from (state, action) to expected rewards, or q value. We store it as a table.

def hash(state, a):
    return (zobrist_hash(state), a)

class Node:
    # Class variables
    qtable = defaultdict(lambda: 0)
    state_action_count = defaultdict(lambda: 0) # Number of times each state-action pair was visited
    state_count = defaultdict(lambda: 0) # Number of times each state was visited

    def __init__(
            self, 
            board, 
            parent=None, 
            parent_action=None
        ):
        self.state = board
        self.children = []
        self.parent = parent
        self.parent_action = parent_action

    def is_fully_expanded(self):
        return len(self.children) == len(list(self.state.legal_moves))

    def is_terminal(self):
        return True if self.state.outcome() else False
    
    def get_ucb_score(self, action, exploration_constant = 0.9):
        q_value = self.qtable[hash(self.state, action)]
        exploration_term = sqrt(2*Node.state_count[zobrist_hash(self.state)]/Node.state_action_count[hash(self.state, action)])
        return q_value + exploration_term * exploration_constant
    
    def get_negative_ucb_score(self, action, exploration_constant = 0.9):
        q_value = self.qtable[hash(self.state, action)]
        exploration_term = sqrt(2*Node.state_count[zobrist_hash(self.state)]/Node.state_action_count[hash(self.state, action)])
        return q_value - exploration_term * exploration_constant

    def choose_best_explored_child(self, metric="qvalue"):
        best_children = []
        actions = [a[0] for a in self.children]
        q_values = None
        if metric=="qvalue":
            q_values = [self.qtable[hash(self.state, a)] for a in actions]
        elif metric=="ucb":
            q_values = [self.get_ucb_score(a) for a in actions]

        max_q_value_of_actions = max(q_values)
        for i in range(len(q_values)):
            if q_values[i] == max_q_value_of_actions:
                best_children.append(self.children[i])
        action, child = random.choice(best_children)
        return action, child
    
    def find_not_fully_expanded_node(self, metric="qvalue"):
        if self.is_terminal():
            return self
        
        if not self.is_fully_expanded():
            return self
        
        _, node = self.choose_best_explored_child(metric)
        return node.find_not_fully_expanded_node()
        
    def create_new_child(self, action):
        board = self.state.copy()
        board.push(action)
        new_child = Node(board, self, action)
        self.children.append((action, new_child))
        return new_child
    
    def create_new_random_child(self):
        all_actions = set(self.state.legal_moves)
        explored_actions = {a[0] for a in self.children}
        unexplored_actions = all_actions - explored_actions
        action = random.choice(list(unexplored_actions))
        new_child = self.create_new_child(action)
        return action, new_child

    def rollout(self, player_color):
        board = self.state.copy()
        depth = 0

        while board.outcome() == None:
            move = random.choice(list(board.legal_moves))
            board.push(move)
            depth += 1

        if board.outcome().winner == None:
            return 0
        elif board.outcome().winner == player_color:
            return 1 # Maybe scale by depth?
        else:
            return -1
        
    def backup(self, action, reward):
        # We got r rewards from taking action a
        # TODO: Dont use the incremental mean method
        Node.state_count[zobrist_hash(self.state)] += 1
        Node.state_action_count[hash(self.state, action)] += 1
        q_value = Node.qtable[hash(self.state, action)]
        Node.qtable[hash(self.state, action)] += (1 / (Node.state_action_count[hash(self.state, action)])) * (reward - q_value)
        if self.parent:
            self.parent.backup(self.parent_action, 0.9*reward)

    def select_best_action(self):
        action, child = self.choose_best_explored_child()
        return action
    
class Agent:
    def __init__(
            self, 
            name,
            selection_metric="qvalue"
        ):
        self.name = name
        self.selection_metric = selection_metric

    def mcts(self, board, timeout=5):
        root_node = Node(board)
        end_time = timeout + time.time()
        while time.time() < end_time:
            not_fully_expanded_node = self.select(root_node)
            if not not_fully_expanded_node.is_terminal():
                new_action, new_child = not_fully_expanded_node.create_new_random_child()
                reward = new_child.rollout(root_node.state.turn)
                not_fully_expanded_node.backup(new_action, reward)
            # else:
            #     # At this point, we have explored all nodes, but will still simulate to 
            #     # reduce the exploration term in the ucb score of not_fully_expanded_node
            #     # So that other nodes may be potentially be explored, and we do not get
            #     # trapped in local minimum
            #     reward = not_fully_expanded_node.rollout(root_node.state.turn)
            #     if not_fully_expanded_node.parent:
            #         not_fully_expanded_node.parent.backup(not_fully_expanded_node.parent_action, reward)
        return root_node.select_best_action()
    
    def select(self, node):
        while node.is_fully_expanded() and not node.is_terminal():
            _, node = node.choose_best_explored_child(metric=self.selection_metric)
        return node
    

    def make_move(self, board, timeout=5):
        if board.outcome():
            raise Exception("Cannot make move, game is over")
        return self.mcts(board, timeout)

# a = Agent('Test')
# print(a.make_move(chess.Board("3r3r/2p3pp/Qp2p3/4P1P1/2p1pP1P/qk2P3/8/1KR5 w - - 0 33")))
# print(zobrist_hash(chess.Board("3r3r/2p3pp/Qp2p3/4P1P1/2p1pP1P/qk2P3/8/1KR5 w - - 0 33"))) # Checkmate position
# for key, value in Node.qtable.items():
#     if key[0] == 15117747300404167418:
#         print(key, value)
# pprint(Node.qtable)
