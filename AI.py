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


    def greedy_action_selection(self, current_player, step, board, possible_pieces, state, possible_actions):
        '''
        Preforms epsilon greedy action selectoin based on the Q-values.
        '''
        # get the action q values for the state
        q_values = self.q_values.get(current_player,{}).get(state,{})
        choice = random.choice(possible_pieces)
        if q_values and np.random.rand() < (1 - self.epsilon):
          # get the max q value for the state
          best_val = sorted(q_values.items(), key=lambda e: e[1])[-1][1]
          b_actions = list(filter(lambda elem: elem[1] == best_val, q_values.items()))
          best_action = b_actions[np.random.choice(len(b_actions))][0]
          if best_action in possible_actions.keys():
            # pick the first piece from the possible_pieces
            best_pieces = [i for i in possible_actions[best_action] if len(possible_actions[best_action]) > 0 and i in possible_pieces]
            if len(best_pieces) > 0:
              choice =  best_pieces[0]
        return choice


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


    def set_q_value(self, current_player, choice, step, reward, board, complete, opponent_killed, all_pieces_pos):
      current_pos = board.piecesPosition[current_player + choice]
      state = str(",".join(map(str, all_pieces_pos)))
      action = str(current_pos)+","+str(current_pos+step)
      rewards = str(reward)+","+str(complete)+","+str(opponent_killed)
      
      if current_player not in self.q_values.keys():
        self.q_values[current_player] = {}
      if state not in self.q_values[current_player].keys():
        self.q_values[current_player][state] = {}
      if action not in self.q_values[current_player][state].keys():
        self.q_values[current_player][state][action] = self.init_q_value
      # Q -value
      G = reward + self.gamma * self.q_values[current_player].get(state, {}).get(action, self.init_q_value)
      new_q_value = self.q_values[current_player].get(state, {}).get(action, self.init_q_value) + self.alpha * (G - self.q_values[current_player].get(state, {}).get(action, self.init_q_value))
      self.q_values[current_player][state][action] = new_q_value

    def get_all_pieces_pos(self, current_player, board):
      '''
      Return list of position for all pieces
      '''
      pieces_number = ['1','2','3','4','5','6']
      pieces_pos = []
      for each_piece in pieces_number:
        pieces_pos.append(board.piecesPosition[current_player + each_piece])
      return pieces_pos


    def choose(self, current_player, pieces, step, board):
        # choice =  np.random.choice(pieces)
        # check reward for each piece
        all_pieces_pos = self.get_all_pieces_pos(current_player, board)
        state = str(",".join(map(str, all_pieces_pos)))
        possible_actions = self.possible_action(step, current_player, board)

        peices_reward = {}
        for each_piece in pieces:
          reward, complete, opponent_killed = self.check_reward(current_player, each_piece, step, board)
          peices_reward[each_piece] = {'reward': reward, 'complete': complete, 'opponent_killed': opponent_killed}
        choice = self.greedy_action_selection(current_player, step, board, pieces, state=state, possible_actions = possible_actions)
        reward = peices_reward[choice]['reward']
        complete = peices_reward[choice]['complete']
        opponent_killed = peices_reward[choice]['opponent_killed']
        self.set_q_value(current_player, choice, step, reward, board, complete, opponent_killed, all_pieces_pos)
        return choice

