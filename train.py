from play import Ur
import time
import pandas as pd
import matplotlib.pyplot as plt
import logging
import json
import argparse
import numpy as np

players = ['A', 'B']


def load_rewards():
    with open('data/rewards.json') as file:
        rewards = json.load(file)
    player1_rewards = rewards.get(players[0])
    player2_rewards = rewards.get(players[1])
    return player1_rewards, player2_rewards

plt.style.use('ggplot')

def live_plotter(x_vec,y1_data,line1,identifier='',pause_time=0.1):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec,y1_data,'-o',alpha=0.8)        
        #update plot label/title
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1

    
def train(episodes=10000):
    start_time = 0
    episodes_data = []
    try:
        for i in range(episodes):
            print("Episode: ", i)
            start_time = time.time()
            Ur().start({"gameType":"3", "autosaveMoves":"y"})
            player1_rewards, player2_rewards = load_rewards()
            time_taken = time.time() - start_time
            episodes_data.append({"episode": i, "time": time_taken, "player1_rewards" : player1_rewards, "player2_rewards" : player2_rewards})
            # line = []
            # line = live_plotter(time_taken, player1_rewards,line)

    
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
    logging.info('Done')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--episode', type=int, help='No. of episodes to train', default=10000)
    args = parser.parse_args()
    episodes = args.episode
    train(episodes)