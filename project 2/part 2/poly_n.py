# YA ALI
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neural_network import MLPRegressor

train_set_range = 100
test_set_range = 100
noise_percent = 0.4

x = np.arange(-train_set_range, train_set_range, 5).reshape(-1, 1)
y = 0.0001 * x ** 3 + 0.0095 * x ** 2 - 33         # func
y = y.ravel()
length = len(x)
indexes = np.random.randint(-length, length, int(length * 2 * noise_percent))
for i in indexes:
    y[i] = np.random.randint(-train_set_range, train_set_range, 1) + y[i]

clf = MLPRegressor(hidden_layer_sizes=(500, 500, 500, 500, 500), max_iter=1000, solver='lbfgs').fit(x, y)

test_x = np.arange(-test_set_range, test_set_range, 5).reshape(-1, 1)
test_y = clf.predict(test_x)

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(x, y, s=1, c='b', marker="s", label='real function')
ax1.scatter(test_x, test_y, s=10, c='r', marker="o", label='NN Prediction')
plt.legend()
# plt.savefig('D:\\university\\هوش\\assigns\\پروژه2\\poly_n.png')
plt.show()
