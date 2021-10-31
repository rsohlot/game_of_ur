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


    def greedy_selection(self,current_player, pieces, step, board):
        """
        Greedy selection of the best move.
        """
        piece_with_max_reward = pieces[0]
        max_reward = 0
        reward = 0

        path_index = board.path_index.get(current_player)
        for piece,each_piece_pos in  board.piecesPosition.items():
          if each_piece_pos + step -1 < len(board.PATHS[path_index]):
            path_coord = board.PATHS[path_index][each_piece_pos + step-1]
          else:
            continue
          if piece[0] == current_player:
            if each_piece_pos == -1:
              reward = 10
            else:  
              # occupied_status = board.isOccupied(each_piece_pos + step-1)
              # if occupied_status[0] and occupied_status[1][0] != piece[0]:
              occupied_status = board.opponentCell(current_player, path_coord)
              if occupied_status:
                reward = 40

              elif board.cellSafe(path_coord):
                reward = 20
              else:
                reward =10

          if reward > max_reward:
              piece_with_max_reward = piece[1]
              max_reward = reward

        self.score += max_reward
        return piece_with_max_reward


    def choose(self, current_player, pieces, step, board):
        return self.greedy_selection(current_player, pieces, step, board)
