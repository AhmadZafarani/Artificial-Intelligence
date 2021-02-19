from sklearn import svm
import random as rnd
import matplotlib.pyplot as plt
import numpy as np

samples = []
labels = []
string = 'abs( y ) - abs( x )'

i = 0
while i < 500:
    s = [rnd.uniform(-150, 150), rnd.uniform(-150, 150)]
    x = s[0]
    y = s[1]
    result = eval(string)
    # if abs(result) < 10:
    #     continue
    if result >= 0:
        labels.append(1)
    else:
        labels.append(-1)
    samples.append(s)
    i += 1

clf = svm.SVC(kernel='poly', degree=2, coef0=2)
clf.fit(samples, labels)

test_size = 200
test = []
true_clf = []
i = 0
while i < test_size:
    s = [rnd.uniform(-150, 150), rnd.uniform(-150, 150)]
    x = s[0]
    y = s[1]
    result = eval(string)
    # if abs(result) < 10:
    #     continue
    if result >= 0:
        true_clf.append(1)
        plt.scatter([x], [y], color="green", marker="+", s=30, cmap='autumn')
    else:
        true_clf.append(-1)
        plt.scatter([x], [y], color="red", s=30, cmap='autumn')
    test.append(s)
    i += 1

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
plt.show()
# plt.savefig('foo.png')
