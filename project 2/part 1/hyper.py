# YA ALI
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neural_network import MLPRegressor

train_set_range = 100
test_set_range = 500

x = np.arange(-train_set_range, train_set_range, 10)
x = np.delete(x, 10)
x = x.reshape(-1, 1)
y = 100 / x         # func
y = y.ravel()
clf = MLPRegressor(hidden_layer_sizes=1000, max_iter=1000, activation='logistic').fit(x, y)

test_x = np.arange(-test_set_range, test_set_range, 10).reshape(-1, 1)
test_y = clf.predict(test_x)

fig = plt.figure()
ax1 = fig.add_subplot(111)

x = np.arange(-test_set_range, test_set_range, 10)
x = np.delete(x, 50)
x = x.reshape(-1, 1)
y = 100 / x         # func
y = y.ravel()

ax1.scatter(x, y, s=1, c='b', marker="s", label='real function')
ax1.scatter(test_x, test_y, s=10, c='r', marker="o", label='NN Prediction')
plt.legend()
# plt.savefig('D:\\university\\هوش\\assigns\\پروژه2\\hyper.png')
plt.show()
