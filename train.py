from play import Ur
import time
import pandas as pd
import matplotlib.pyplot as plt
import logging
import json
import argparse

players = ['A', 'B']


def load_rewards():
    with open('data/rewards.json') as file:
        rewards = json.load(file)
    player1_rewards = rewards.get(players[0])
    player2_rewards = rewards.get(players[1])
    return player1_rewards, player2_rewards

def train(episodes):
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
    data = pd.DataFrame(episodes_data)
    ax = plt.gca()
    # 1 
    # ax.set_xlabel('Episode')
    # ax.set_ylabel('Time')
    # ax.set_title('Training time')
    # plt.plot(data[['player1_rewards','player2_rewards']].rolling(10, min_periods=1).mean(), color='C0')
    # 2
    data.plot(x='episode', y=['player1_rewards', 'player2_rewards'], ax=ax)

    
    logging.info('Saving figure and data')
    plt.savefig('data/value_function_mc.jpg', dpi=600)    
    data.to_csv('data/value_function_mc.csv', index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.parse_args()
    parser.add_argument('-e', '--episode', type=int, help='No. of episodes to train', default=10000)
    args = parser.parse_args()
    episodes = args.episode
    train(episodes)