from sklearn import svm
import random as rnd
import matplotlib.pyplot as plt
import numpy as np

samples = []
labels = []


def func(x: float, y: float) -> float:
    if x > 0 and y > 0:
        return eval('(y - 50)**2 + (x - 50)**2 - 625')
    elif y > 0:
        return eval('(y - 50)**2 + (x + 50)**2 - 625')
    elif x < 0 and y < 0:
        return eval('(y + 50)**2 + (x + 50)**2 - 625')
    return y


i = 0
while i < 500:
    s = [rnd.uniform(-100, 100), rnd.uniform(-100, 100)]
    result = func(s[0], s[1])
    if result >= 0:
        labels.append(1)
    else:
        labels.append(-1)
    samples.append(s)
    i += 1

clf = svm.SVC(kernel='rbf')
clf.fit(samples, labels)

test_size = 200
test = [[rnd.uniform(-100, 100), rnd.uniform(-100, 100)] for i in range(test_size)]
true_clf = []

for sam in test:
    result = func(sam[0], sam[1])
    if result >= 0:
        true_clf.append(1)
        plt.scatter([sam[0]], [sam[1]], color="green", marker="+", s=30)
    else:
        true_clf.append(-1)
        plt.scatter([sam[0]], [sam[1]], color="red", s=30)

corr = test_size
prediction = clf.predict(test)
for i in range(test_size):
    if prediction[i] != true_clf[i]:
        corr -= 1
print(corr * 100 / test_size)


def plot_svc_decision_function(model, ax=None, plot_support=True):
    if ax is None:
        ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    x = np.linspace(xlim[0], xlim[1], 30)
    y = np.linspace(ylim[0], ylim[1], 30)
    Y, X = np.meshgrid(y, x)
    xy = np.vstack([X.ravel(), Y.ravel()]).T
    P = model.decision_function(xy).reshape(X.shape)
    ax.contour(X, Y, P, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])
    if plot_support:
        ax.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1], s=300, linewidth=1, facecolors='none')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


plot_svc_decision_function(clf)
# plt.show()
plt.savefig('foo.png')
