from play import Ur


def train():
    episodes = 100
    for i in range(episodes):
        print("Episode: ", i)
        Ur().start({"gameType":"3", "autosaveMoves":"y"})


    
if __name__ == '__main__':
    train()