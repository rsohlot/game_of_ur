from play import Ur
import time
import pandas as pd
import matplotlib.pyplot as plt
import logging
import json

def load_rewards():
    with open('data/rewards.json') as file:
        rewards = json.load(file)
    player1_rewards, player2_rewards = rewards.values()
    return player1_rewards, player2_rewards

def train():
    episodes = 10000
    start_time = 0
    episodes_data = []
    try:
        for i in range(episodes):
            print("Episode: ", i)
            start_time = time.time()
            Ur().start({"gameType":"3", "autosaveMoves":"y"})
            player1_rewards, player2_rewards = load_rewards()
            episodes_data.append({"episode": i, "time": time.time() - start_time, "player1_rewards" : player1_rewards, "player2_rewards" : player2_rewards})
            

    
    except KeyboardInterrupt:
        logging.info('Inturpt the training.')

    # save figure
    ax = plt.gca()
    # plt.plot(pd.DataFrame(episodes_data).rolling(10, min_periods=1).mean(), color='red')
    data = pd.DataFrame(episodes_data)
    data.plot(x='episode', y=['player1_rewards', 'player2_rewards'], ax=ax)
    logging.info('Saving figure and data')
    plt.savefig('data/value_function_mc.jpg', dpi=600)    
    data.to_csv('data/value_function_mc.csv', index=False)

if __name__ == '__main__':
    train()