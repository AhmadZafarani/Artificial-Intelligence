# YA HOSSEIN
import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from time import time

noise_percent = 0.3


def noisy(vector: np.ndarray) -> np.ndarray:
    for j in range(len(vector)):
        dice = np.random.random()
        if dice < noise_percent:
            vector[j] = np.random.randint(0, 256)
    return vector


def extract_image_and_noisy(root: str, images_n=None, images=None) -> tuple:
    if images is None and images_n is None:
        images_n = []
        images = []
    for f in os.listdir(root):
        s = os.path.join(root, f)
        if os.path.isfile(s):
            img = Image.open(s)
            array = np.array(img)
            flatten = array.flatten()
            images_n.append(noisy(flatten.copy()))
            images.append(flatten)
    return images_n, images


start = time()

pictures_n, pictures = extract_image_and_noisy("images - Copy/train")
pictures_n, pictures = extract_image_and_noisy("images - Copy/test", pictures_n, pictures)

train_x, test_x, train_y, test_y = train_test_split(pictures_n, pictures)
clf = MLPRegressor(hidden_layer_sizes=1000, solver='lbfgs', max_iter=1000)
clf.fit(train_x, train_y)
prediction = clf.predict(test_x)

indexes = np.random.randint(0, len(test_x), 20)
for i in indexes:
    t = test_y[i].reshape(16, 16)
    n = test_x[i].reshape(16, 16)
    p = prediction[i].reshape(16, 16)

    fig, ax = plt.subplots(1, 3)
    ax[0].imshow(t)
    ax[1].imshow(n)
    ax[2].imshow(p)
    ax[0].text(2.5, -3, 'Original', c='g', size=18)
    ax[1].text(4.5, -3, 'Noisy', c='r', size=18)
    ax[2].text(1.5, -3, 'Prediction', c='b', size=18)
    # plt.savefig('test1.png')
    plt.show()

print(time() - start)
