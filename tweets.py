import tensorflow_hub as hub
import pandas as pd
import sklearn
import numpy as np
import matplotlib.pyplot as plt
import pickle
import algorythm_tidbscan as tidb

# Follow readme and update location of TENSORFLOW MODEL:
TENSORFLOW_MODEL = 'model/'
DATA = ['BarackObama.csv', 'BillGates.csv', 'BorisJohnson.csv', 'elonmusk.csv', 'jk_rowling.csv',
        'KamalaHarris.csv', 'PolandMFA.csv', 'Pontifex.csv', 'POTUS.csv', 'RobertDowneyJr.csv', 'RoyalFamily.csv']


def read_n_tweets(filepath, n=-1):
    data = pd.read_csv(filepath)
    tweets_list = data['tablescraper-selected-row'].to_list()

    vector = []
    for tweet in tweets_list[0:n]:
        if pd.isnull(tweet):
            continue
        vector.append(tweet)
    return vector


def read_n_tweets_from_data(path=DATA, number=-1):
    master_vector = []
    class_vector = []
    for d in path:
        vector = read_n_tweets('data/' + d, number)
        master_vector.extend(vector)
        class_vector.extend([d for i in vector])

    return master_vector, class_vector


def read_all_tweets(path=DATA):
    master_vector = []
    class_vector = []
    for d in path:
        vector = read_n_tweets('data/' + d)
        master_vector.extend(vector)
        class_vector.extend([d for i in vector])

    return master_vector, class_vector


def get_vectors(tweets_list):
    embed = hub.load(TENSORFLOW_MODEL)
    return embed(tweets_list)


def create_and_save_distances_list(vector, save=False):
    distance_list = []
    for i in range(len(vector)):
        p = vector[i]
        dis = []
        for q in vector:
            distance = np.linalg.norm(p - q)
            dis.append(distance)
        distance_list.append(dis)

    if save:
        with open('dump/distances_list', 'wb') as file:
            pickle.dump(distance_list, file)

    return distance_list


def read_distances_list():
    with open('dump/distances_list', 'rb') as f:
        my_list = pickle.load(f)

    return my_list


def get_basic_statistics(distances_list):
    mins = []
    maxs = []
    meds = []

    for distance in distances_list:
        # distance[distance.index(0.0)] = float("nan")
        distance.pop(distance.index(0.0))
        mins.append(min(distance))
        maxs.append(max(distance))
        meds.append(np.median(distance))

    return [mins, meds, maxs]


def plot_basic_statistics(mini, medi, maxi):
    df = pd.DataFrame(mini, columns=['min'])
    df['max'] = maxi
    df['median'] = medi
    ax = df.plot.hist(bins=60, alpha=0.5)
    ax.plot()
    plt.show()


def save_data(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def get_results_for_multiple_eps(vector, eps_start, eps_end, n, min_pts=2):
    delta = (eps_end-eps_start) / n
    results = []
    for i in range(n):
        r = tidb.algorythm_tidbscan(min_pts, eps_start + n * delta, vector)
        results.append(r)

    return results
if __name__ == '__main__':
    pass
