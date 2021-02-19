# YA HOSSEIN
import numpy as np
from sklearn.neural_network import MLPRegressor

train_set_range = 1500
test_set_range = 3000

x = np.arange(-train_set_range, train_set_range, 10).reshape(30, 10)
y = [np.append(v, v // 10) for v in x]  # func
clf = MLPRegressor(hidden_layer_sizes=1000, activation='identity', solver='lbfgs', max_iter=1000, random_state=1).fit(x,
                                                                                                                      y)

test_x = np.arange(-test_set_range, test_set_range, 10).reshape(60, 10)
test_y = clf.predict(test_x)
true_y = [np.append(v, v // 10) for v in test_x]

lose = 0
for w in range(len(test_y)):
    lose += np.linalg.norm(test_y[w] - true_y[w])
print(lose)
