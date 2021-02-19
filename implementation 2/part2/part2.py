# YA KARIM
from math import log2
from random import random, randint
import csv

from classes import Sample, Node


def getter(inp: list) -> Sample:
    return Sample(inp[0], inp[1], inp[2], inp[3], inp[4], inp[5], inp[6], inp[7], inp[8])


def test_in_tree(root: Node, sample: Sample) -> str:
    if root:
        if root.value == "1" or root.value == "0":
            return root.value
        x = sample.__getattribute__(root.value)
        for c in root.children:
            if x in c.label:
                return test_in_tree(c, sample)


def main():
    print("Reading data from CSV file...")
    train_set = []
    with open("diabetes.csv") as file:
        reader = csv.reader(file)
        counter = 0
        for row in reader:
            if counter == 0:
                counter += 1
                continue
            train_set.append(getter(row))
            counter += 1
        rnd = randint(50, 90)
        x = rnd * counter // 100
        test_set = train_set[x + 1:]
        train_set = train_set[:x]
        root = decision_tree_learning(train_set, Sample.attributes_values, [])
        print("DECISION TREE BUILT with %d percent of the data!\t this is the visualization:" % rnd)
        Node.print_tree(root)
        print("testing the remaining data in tree...")
        right_answer = 0
        for dat in test_set:
            if test_in_tree(root, dat) == dat.outcome:
                right_answer += 1
        print(
            "DECISION TREE predicted the right answer in %d percent of times." % (right_answer * 100 // len(test_set)))


def plurality_value(example: list) -> Node:
    mid = len(example) >> 1
    leaf = Node("", 0, 0, 0, [])
    positives = 0
    for e in example:
        if e.outcome == "1":
            positives += 1
    if positives > mid:
        leaf.value = "1"
    elif positives < mid:
        leaf.value = "0"
    else:
        x = random()
        if x >= 0.5:
            leaf.value = "1"
        else:
            leaf.value = "0"
    return leaf


def bin_entropy(var: float) -> float:
    if var == 1.0 or var == 0.0:
        return 0
    return -(var * log2(var) + (1 - var) * log2(1 - var))


def remainder(attr: str, examples: list) -> float:
    s = 0
    for val in Sample.get_values(attr):
        this_value = 0
        positive_this_value = 0
        for e in examples:
            if e.__getattribute__(attr) == val:
                this_value += 1
                if e.outcome == "1":
                    positive_this_value += 1
        if this_value == 0:
            continue
        s += ((this_value / len(examples)) * bin_entropy(positive_this_value / this_value))
    return s


def information_gain(attr: str, examples: list) -> tuple:
    p = 0
    for e in examples:
        if e.outcome == "1":
            p += 1
    entropy = bin_entropy(p / len(examples))
    f = remainder(attr, examples)
    return entropy - f, entropy, f


def max_importance(attributes: list, examples: list) -> tuple:
    index = 0
    maximum_g = 0
    maximum_e = 0
    maximum_r = 0
    for i in range(len(attributes)):
        gain, entropy, remainder_ = information_gain(attributes[i], examples)
        if gain > maximum_g:
            maximum_g = gain
            maximum_e = entropy
            maximum_r = remainder_
            index = i
    return attributes[index], maximum_g, maximum_r, maximum_e


def decision_tree_learning(examples: list, attributes: list, parent_examples: list) -> Node:
    if not examples:
        return plurality_value(parent_examples)
    elif Sample.same_classification(examples):
        return Node(examples[0].outcome, 0, 0, 0, [])
    elif not attributes:
        return plurality_value(examples)
    else:
        tup = max_importance(attributes, examples)
        a = tup[0]
        tree = Node(a, tup[1], tup[2], tup[3], [])
        for val in Sample.get_values(a):
            exs = []
            for e in examples:
                if e.__getattribute__(a) == val:
                    exs.append(e)
            attributes.remove(a)
            subtree = decision_tree_learning(exs, attributes, examples)
            subtree.set_label(a, val)
            tree.children.append(subtree)
            attributes.append(a)
        return tree


main()
