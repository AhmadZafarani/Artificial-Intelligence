# YA REZA
import os
import numpy as np
from PIL import Image
from sklearn.neural_network import MLPClassifier


def extract_image_and_label(root: str) -> tuple:
    images = []
    labels = []
    for f in os.listdir(root):
        s = os.path.join(root, f)
        if os.path.isfile(s):
            img = Image.open(s)
            array = np.array(img)
            flatten = array.flatten()
            images.append(flatten)
            labels.append(int(f[0]))
    return images, labels


train_set, train_labels = extract_image_and_label("C:\\Users\\Asus\\PycharmProjects\\AI-project2\\src\\images\\train")
test_set, true_prediction = extract_image_and_label("C:\\Users\\Asus\\PycharmProjects\\AI-project2\\src\\images\\test")
clf = MLPClassifier(hidden_layer_sizes=1000, activation='logistic', max_iter=500)
clf.fit(train_set, train_labels)
prediction = clf.predict(test_set)

test_size = len(test_set)
corr = test_size
for i in range(test_size):
    if prediction[i] != true_prediction[i]:
        corr -= 1
print("classification precision is %.3f percents." % (corr * 100 / test_size))
