# YA SOLTAN TOOS
import os
import numpy as np
from PIL import Image
from sklearn import svm
from random import sample

root = "C:\\Users\\Asus\\PycharmProjects\\imp3\\src\\plak"
train_set, train_labels, test_set, true_prediction = [], [], [], []


def open_image(path: str) -> np.array:
    img = Image.open(path)
    array = np.array(img)
    flatten = array.flatten()
    return flatten


def split_to_train_and_test():
    for f in ['2', '3', '7', 'S', 'W']:
        rands = sample(range(300), 200)
        folder = os.path.join(root, f)
        i = 0
        for pic in os.listdir(folder):
            pic = os.path.join(folder, pic)
            if os.path.isfile(pic):
                image = open_image(pic)
                if i in rands:
                    train_set.append(image)
                    train_labels.append(f)
                else:
                    test_set.append(image)
                    true_prediction.append(f)
                i += 1


def print_prediction_precision():
    test_size = len(test_set)
    corr = test_size
    for j in range(test_size):
        if prediction[j] != true_prediction[j]:
            corr -= 1
    print(corr * 100 / test_size)


split_to_train_and_test()
clf = svm.SVC(kernel='poly')
clf.fit(train_set, train_labels)
prediction = clf.predict(test_set)
print_prediction_precision()
