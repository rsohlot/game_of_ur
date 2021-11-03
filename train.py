from play import Ur
import time
import pandas as pd
import matplotlib.pyplot as plt
import logging


def train():
    episodes = 10000
    start_time = 0
    episodes_data = []
    try:
        for i in range(episodes):
            print("Episode: ", i)
            start_time = time.time()
            Ur().start({"gameType":"3", "autosaveMoves":"y"})
            episodes_data.append({"episode": i, "time": time.time() - start_time})
    
    except KeyboardInterrupt:
        logging.info('Inturpt the training.')

    # save figure
    plt.figure(figsize=(20, 6))
    # plt.plot(pd.DataFrame(episodes_data).rolling(10, min_periods=1).mean(), color='red')
    data = pd.DataFrame(episodes_data)
    plt.plot(data, color='red')
    plt.xlabel('Episodes')
    plt.ylabel('Value')
    plt.title("Time per episodes")
    logging.info('Saving figure and data')
    plt.savefig('data/value_function_mc.jpg', dpi=600)    
    data.to_csv('data/value_function_mc.csv', index=False)

if __name__ == '__main__':
    train()