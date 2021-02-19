# YA HOSSEIN
import numpy as np
from sklearn.neural_network import MLPRegressor

train_set_range = 1500
test_set_range = 3000

A = np.random.randint(-100, 100, 100)
A = np.reshape(A, (10, 10))
b = np.random.randint(-100, 100, 10)
x = np.arange(-train_set_range, train_set_range, 10).reshape(30, 10)
y = [np.dot(A, v) + b for v in x]        # func
clf = MLPRegressor(activation='identity', solver='lbfgs', max_iter=1000).fit(x, y)

test_x = np.arange(-test_set_range, test_set_range, 10).reshape(60, 10)
test_y = clf.predict(test_x)
true_y = [np.dot(A, v) + b for v in test_x]

lose = 0
for w in range(len(test_y)):
    lose += np.linalg.norm(test_y[w] - true_y[w])
print(lose)
