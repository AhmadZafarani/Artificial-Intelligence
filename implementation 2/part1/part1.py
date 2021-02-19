# YA KARIM
from math import log2
from random import random

from utill import Sample, Node


def getter(string: str) -> Sample:
    strs = string.split()
    return Sample(strs[0], strs[1], strs[2], strs[3], strs[4], strs[5], strs[6], strs[7], strs[8], strs[9], strs[10])


def test_in_tree(root: Node, sample: Sample) -> str:
    if root:
        if root.value == "Yes" or root.value == "No":
            return root.value
        x = sample.__getattribute__(root.value)
        for c in root.children:
            if x in c.label:
                return test_in_tree(c, sample)


def main():
    n = int(input("Enter size of training set:"))
    print("Enter each sample, in this order: Alternate Bar Fri/Sat Hungry Patrons Price Raining Reservation Type \
    WaitEstimate\t(split the input with spaces)")
    train_set = []
    for i in range(n):
        train_set.append(getter(input()))
    root = decision_tree_learning(train_set, Sample.attributes_values, [])
    print("DECISION TREE BUILT!\tthis is the visualization:")
    Node.print_tree(root)
    m = int(input("Enter size of test set:"))
    print("Enter each test case in the same manner of training set")
    for i in range(m):
        s = getter(input())
        if test_in_tree(root, s) == s.goal:
            print("Right prediction :))")
        else:
            print("Wrong prediction :((")


def plurality_value(example: list) -> Node:
    mid = len(example) >> 1
    leaf = Node("", 0, 0, 0, [])
    positives = 0
    for e in example:
        if e.goal == "Yes":
            positives += 1
    if positives > mid:
        leaf.value = "Yes"
    elif positives < mid:
        leaf.value = "No"
    else:
        x = random()
        if x >= 0.5:
            leaf.value = "Yes"
        else:
            leaf.value = "No"
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
                if e.goal == "Yes":
                    positive_this_value += 1
        if this_value == 0:
            continue
        s += ((this_value / len(examples)) * bin_entropy(positive_this_value / this_value))
    return s


def information_gain(attr: str, examples: list) -> tuple:
    p = 0
    for e in examples:
        if e.goal == "Yes":
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
        return Node(examples[0].goal, 0, 0, 0, [])
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
