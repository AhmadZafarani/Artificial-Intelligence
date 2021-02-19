# YA HOSSEIN
import numpy as np
from sklearn.neural_network import MLPRegressor

train_set_range = 1500
test_set_range = 3000

y = np.arange(-train_set_range, train_set_range, 10).reshape(30, 10)
x = y.copy()
for r in x:
    np.random.shuffle(r)
clf = MLPRegressor(hidden_layer_sizes=1000, activation='identity', solver='lbfgs', max_iter=1000, alpha=0.1).fit(x, y)

true_y = np.arange(-test_set_range, test_set_range, 10).reshape(60, 10)
test_x = true_y.copy()
for r in test_x:
    np.random.shuffle(r)
test_y = clf.predict(test_x)

lose = 0
for w in range(len(test_y)):
    lose += np.linalg.norm(test_y[w] - true_y[w])
print(lose)
