import algorythm_tidbscan as tidb
import pickle
import sys


inputfile = sys.argv[1]
epsilon_start = float(sys.argv[2])

with open(inputfile, 'rb') as f:
    d = pickle.load(f)

tweets, class_vector, tweet_vector = d

print("starting dbscan for epsilon={}".format(epsilon_start))
results = tidb.algorythm_tidbscan(2, epsilon_start, tweet_vector)

filename = inputfile + '_results_' + str(epsilon_start)

data = [tweets, class_vector, tweet_vector, results]
with open(filename, 'wb') as f:
    pickle.dump(data, f)

print("EOF.GG")
