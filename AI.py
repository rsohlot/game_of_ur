import random

class Player(object):
    """docstring for Player
    AI chooses which piece to play here
    Available data:
      piecces: the set of movable pieces for AI player
      self.board: Game board with complete state"""

    def __init__(self):
        super(Player, self).__init__()
        self.score = 0

    def get_reward(self,current_player, piece, step, board):
        """
        Get the reward of a piece.
        """
        reward = 0

        peice_updated_pos = {} 
        peice_reward = {}
        for k,v in  board.piecesPosition.items():
          if k[0] == current_player and k[1] == piece:
            peice_updated_pos[k[1]] = v + step
            # occupied_status = board.isOccupied( board.PATHS[0][v + step-1])
            occupied_status = board.isOccupied(v + step-1)
            if occupied_status[0] and occupied_status[1] != k[0]:
              peice_reward[k[1]] = 40
            else:
              peice_reward[k[1]] = 10
            return reward
        ###
        # peice_reward = sorted(peice_reward.items(), key=lambda x: x[1])
        # reward = peice_reward[0][0]
        # return reward


    def greedy_selection(self,current_player, pieces, step, board):
        """
        Greedy selection of the best move.
        """
        piece_with_max_reward = pieces[0]
        max_reward = 0
        temp_score = 0
        for each_piece in pieces:
          reward = self.get_reward(current_player, each_piece, step, board)
          if reward > max_reward:
              piece_with_max_reward = each_piece
              max_reward = reward

        self.score += temp_score
        return piece_with_max_reward


    def choose(self, current_player, pieces, step, board):
        # return random.choice(pieces, step, board)
        return self.greedy_selection(current_player, pieces, step, board)
