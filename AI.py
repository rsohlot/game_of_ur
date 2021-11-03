import random
import json
import numpy as np
from collections import defaultdict
import os

class Player(object):
    """docstring for Player
    AI chooses which piece to play here
    Available data:
      piecces: the set of movable pieces for AI player
      self.board: Game board with complete state"""

    def __init__(self):
        super(Player, self).__init__()
        self.score = 0
        self.player_reward = {}
        self.epsilon = 0.1
        self.alpha = 0.1
        self.gamma = 0.9
        self.init_q_value = 0.0
        self.action_space_n = 25
        self.q_values_file_path = 'data/q_value.json'
        self.load_q_values()


    def save_rewards(self):
      with open('data/rewards.json', 'w') as file:
        json.dump(self.player_reward, file)


    def save_q_values(self):
      with open(self.q_values_file_path , 'w') as file:
        json.dump(self.q_values, file)


    def load_q_values(self):
      if os.path.exists(self.q_values_file_path):
        with open(self.q_values_file_path) as file:
          self.q_values = json.load(file)
      else:
        self.q_values = {}


    def check_reward(self,current_player, choice, step, board):
        """
        Greedy selection of the best move.
        """
        reward = 0
        complete = False
        opponent_killed = False
        piece_pos = board.piecesPosition[current_player + choice]
        path_index = board.path_index.get(current_player)
        if piece_pos + step == len(board.PATHS[path_index]):
          # finish the piece
          reward = 100
          complete = True

        elif piece_pos + step  < len(board.PATHS[path_index]):
          next_pos = board.PATHS[path_index][piece_pos + step]
          if piece_pos == -1:
            reward = 10
          else:  
            occupied_status = board.opponentCell(current_player, next_pos)
            if occupied_status:
              reward = 40
              opponent_killed = True
            elif board.cellSafe(next_pos):
              reward = 20
            else:
              reward =10
        # update reward for player
        self.player_reward[current_player] = self.player_reward.get(current_player,0) + reward
        
        return reward, complete, opponent_killed


    def greedy_action_selection(self, current_player, pieces, step, board, possible_actions):
        '''
        Preforms epsilon greedy action selectoin based on the Q-values.
        '''
        q_values = self.q_values.get(current_player,{})
        if q_values and np.random.rand() < (1 - self.epsilon):
            best_val = sorted(q_values.items(), key=lambda e: e[1][3])[-1][1][3]
            b_actions = list(filter(lambda elem: elem[1][3] == best_val, q_values.items()))
            best_action = b_actions[np.random.choice(len(b_actions))][1][1]
            if best_action in possible_actions.keys(): 
              return possible_actions[best_action][0]
        return np.random.choice(pieces)

    
    def possible_action(self, step, current_player, board):
        possible_actions = {}
        path_index = board.path_index.get(current_player)
        for piece,each_piece_pos in  board.piecesPosition.items():
          if piece[0] == current_player and each_piece_pos + step <= len(board.PATHS[path_index]):
            action = str(each_piece_pos)+","+str(each_piece_pos + step)
            possible_actions[action] = possible_actions.get(action,[]) + [piece[1]]
          else:
            continue
        return possible_actions


    def set_q_value(self, current_player, choice, step, reward, board, complete, opponent_killed):
      current_pos = board.piecesPosition[current_player + choice]
      state = str(current_player)+","+str(current_pos)
      action = str(current_pos)+","+str(current_pos+step)
      rewards = str(reward)+","+str(complete)+","+str(opponent_killed)
      
      q_value_key = str(state)+","+str(action)+","+ str(rewards)
      if current_player not in self.q_values.keys():
        self.q_values[current_player] = {}
      # Q -value
      G = 0
      G = reward + (self.gamma * G)
      new_q_tuple = (state,action,reward,0)
      old_q_tuple = self.q_values.get(current_player,{}).get(q_value_key,new_q_tuple)[3]
      q_value = (self.alpha * (G - old_q_tuple))
      q_value = q_value + old_q_tuple
      self.q_values[current_player][q_value_key] = (state,action,reward,q_value)


    def choose(self, current_player, pieces, step, board):
        # choice =  np.random.choice(pieces)
        possible_actions = self.possible_action(step, current_player, board)
        choice = self.greedy_action_selection(current_player, pieces, step, board, possible_actions)
        reward, complete, opponent_killed = self.check_reward(current_player, choice, step, board)
        self.set_q_value(current_player, choice, step, reward, board, complete, opponent_killed)
        return choice

