from sklearn import metrics
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
    delta = (eps_end - eps_start) / n
    results = []
    for i in range(n):
        r = tidb.algorythm_tidbscan(min_pts, eps_start + i * delta, vector)
        results.append(r)
    return results


def get_results_for_multiple_eps_not_our_implementation(vector, eps_start, eps_end, n, min_pts=2):
    epsilons = get_epsilon_array(eps_start, eps_end, n)
    results = []
    for i in range(n):
        r = sklearn.cluster.dbscan(X=vector, eps=epsilons[i], min_samples=min_pts)
        results.append(r[1])

    return results


def get_df_for_test_results(results, class_vector, eps_start, eps_end, n):
    df = pd.DataFrame()

    epsilons = get_epsilon_array(eps_start, eps_end, n)
    for el_index, result in enumerate(results):
        # current_epsi = epsilon_start + el_index * (epsilon_end - epsilon_start) / n
        for num in range(len(DATA)):
            cluster = []
            first_occ = class_vector.index(DATA[num])
            last_occ = next(i for i in reversed(range(len(class_vector))) if class_vector[i] == DATA[num])
            for point in result[first_occ:last_occ]:
                cluster.append(point)
            name = 'eps_' + str(round(epsilons[el_index], 2)) + '_' + DATA[num]
            tmp_df = pd.DataFrame({name: cluster})
            df = pd.concat([df, tmp_df], ignore_index=False, axis=1)

    return df


def get_df_for_results(results, class_vector, epsilon_start, epsilon_end, n):
    df = pd.DataFrame()
    epsilons = get_epsilon_array(epsilon_start, epsilon_end, n)

    for el_index, result in enumerate(results):
        # current_epsi = epsilon_start + el_index * (epsilon_end - epsilon_start) / n
        for num in range(len(DATA)):
            cluster = []
            first_occ = class_vector.index(DATA[num])
            last_occ = next(i for i in reversed(range(len(class_vector))) if class_vector[i] == DATA[num])
            for point in result[first_occ:last_occ]:
                cluster.append(int(point.label))
            name = 'eps_' + str(round(epsilons[el_index], 2)) + '_' + DATA[num]
            tmp_df = pd.DataFrame({name: cluster})
            df = pd.concat([df, tmp_df], ignore_index=False, axis=1)

    return df


def get_purity_for_n_results_dbscan(class_vector, results, number):
    scores = []
    for i in range(number):
        scores.append(purity_score(class_vector, results[i]))

    return scores


def get_purity_for_n_results_tidbscan(class_vector, results, number):
    scores = []
    flat = []
    for i in range(number):
        flat.append([])
        for point in results[i]:
            flat[i].append(point.label)

    for i in range(number):
        scores.append(purity_score(class_vector, flat[i]))

    return scores


def purity_score(y_true, y_pred):
    # Source: https://stackoverflow.com/a/51672699
    # compute contingency matrix (also called confusion matrix)
    contingency_matrix = metrics.cluster.contingency_matrix(y_true, y_pred)
    # return purity
    return np.sum(np.amax(contingency_matrix, axis=0)) / np.sum(contingency_matrix)


def get_epsilon_array(eps_start, eps_end, number):
    c = (eps_end - eps_start) / number
    return [eps_start + i * c for i in range(number)]


if __name__ == '__main__':
    pass
