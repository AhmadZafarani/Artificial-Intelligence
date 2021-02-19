# YA JAVAD
from time import time
from random import random, randint, uniform
from decimal import Decimal, MIN_EMIN, getcontext


class Node:

    def __eq__(self, o) -> bool:
        return self.fitness == o.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __repr__(self) -> str:
        return "coordinates are " + self.coordinates.__repr__() + "\nwith fitness = " + self.fitness.__repr__() + "\n"

    def fit(self) -> Decimal:
        """put coordinates in each equation, subtracts constant value from the result and adds the absolute value of
        the answer to @param fit """
        fit = 0
        for e in equations:
            this_equ = 0
            for i in range(num_of_params):
                this_equ += (self.coordinates[i] * e[i])
            fit += abs(this_equ - e[-1])
        return -Decimal(fit)

    def __init__(self, coordinates: list) -> None:
        self.coordinates = coordinates
        self.fitness = self.fit()


def truncate(x: float, precision: int) -> Decimal:
    y = 10 ** precision
    x = int(x * y)
    return Decimal(x) / y


def next_state_policy(current: Node, step: Decimal) -> list:
    next_state = []
    for i in range(num_of_params):
        x = current.coordinates[i]
        next_state.append(Node(current.coordinates[0:i] + [x + step] + current.coordinates[i + 1:]))
        next_state.append(Node(current.coordinates[0:i] + [x - step] + current.coordinates[i + 1:]))
    return next_state


def hill_climbing_search(current_state: Node, step: Decimal) -> list:
    partial_time = time()
    ret = [current_state]
    successors = next_state_policy(current_state, step)
    node = max(successors)
    num_of_steps_to_goal = 0
    while node.fitness > current_state.fitness:
        current_state = node
        successors = next_state_policy(current_state, step)
        node = max(successors)
        num_of_steps_to_goal += 1
    ret.extend([step, current_state, time() - partial_time, num_of_steps_to_goal])
    return ret


def initial_point_generator() -> list:
    x = []
    for i in range(num_of_params):
        x.append(truncate(uniform(interval_start, interval_end), 3))
    return x


def getter(obj: map) -> tuple:
    global num_of_params, worst_fitness
    t = tuple(obj)
    if num_of_params == 0:
        num_of_params = len(t)
    elif num_of_params != len(t):
        raise IndexError("number of parameters in equation doesn't match!")
    sm = 0
    for factor in t:
        sm += abs(factor)
    worst_fitness += sm
    return t


def best(lst: list) -> list:
    bst = Decimal(MIN_EMIN)
    bst_t = []
    for t in lst:
        if t[2].fitness > bst:
            bst_t = t
            bst = t[2].fitness
    return bst_t


def this_step_temp(steps: int) -> Decimal:
    if steps < max_steps_sas:
        return Decimal(max_steps_sas - steps)
    else:
        return Decimal(0)


def simulated_annealing_search(current_state: Node, step: Decimal) -> list:
    partial_time = time()
    ret = [current_state, step]
    nodes_visited = 0
    while 1:
        nodes_visited += 1
        temperature = this_step_temp(nodes_visited)
        if temperature == Decimal(0):
            ret.extend([current_state, time() - partial_time, nodes_visited])
            return ret
        i = randint(0, num_of_params - 1)
        sub_or_add = randint(1, 2)
        if sub_or_add == 1:  # add step to chosen value
            next_state = Node(current_state.coordinates[0:i] + [current_state.coordinates[i] + step] +
                              current_state.coordinates[i + 1:])
        else:  # sub step from chosen value
            next_state = Node(current_state.coordinates[0:i] + [current_state.coordinates[i] - step] +
                              current_state.coordinates[i + 1:])
        delta_e = next_state.fitness - current_state.fitness
        if delta_e > 0:
            current_state = next_state
        else:
            delta_e /= temperature
            probability = delta_e.exp()
            if random() <= probability:
                current_state = next_state


def main():
    global equations, interval_start, interval_end, step_length, num_of_params, worst_fitness, max_steps_sas
    print("please enter start of interval, end of interval and step length")
    interval_start, interval_end, step_length = map(float, input().split(" "))
    start_exec_time = time()
    with open("input.txt", "r") as inp:
        lines = inp.readlines()
        equations = [getter(map(Decimal, lns.split(","))) for lns in lines]
        inp.close()

    num_of_params -= 1
    worst_fitness *= Decimal(-max(abs(interval_start), abs(interval_end)))
    max_steps_sas = Decimal(interval_end - interval_start) // Decimal(step_length) * num_of_params

    hill_climbing_result = exec_algo(hill_climbing_search)
    simulated_annealing_result = exec_algo(simulated_annealing_search)
    print_results(hill_climbing_result, simulated_annealing_result, start_exec_time)


def printer(lst: list) -> str:
    s = "["
    for i in range(len(lst) - 1):
        s += lst[i].__str__()
        s += ", "
    s += lst[-1].__str__()
    s += "]"
    return s


def print_results(hill_climbing_result, simulated_annealing_result, start_exec_time):
    print("Hill Climbing Search ran", algo_exec_numbers, "times. best answer started from a point with coordinates :\n",
          printer(hill_climbing_result[0].coordinates), "\nand fitness : ", hill_climbing_result[0].fitness,
          "\nwith step length : ", hill_climbing_result[1], "\nand now a local maximum found with coordinates : \n",
          printer(hill_climbing_result[2].coordinates), "\nand fitness : ", hill_climbing_result[2].fitness,
          "\nin %.6f seconds and the algorithm found the answer in " % hill_climbing_result[3], hill_climbing_result[4],
          " steps.")
    print("****************************************************")
    print("Simulated Annealing Search ran ", algo_exec_numbers,
          "times. best answer started from a point with coordinates :\n",
          printer(simulated_annealing_result[0].coordinates), "\nand fitness : ", simulated_annealing_result[0].fitness,
          "\nwith step length : ", simulated_annealing_result[1],
          "and now the temperature reach's zero, after : ", simulated_annealing_result[4],
          "steps.\nthe answer found in %.6f seconds a point with coordinates : \n" % simulated_annealing_result[3],
          printer(simulated_annealing_result[2].coordinates), "\nand fitness : ", simulated_annealing_result[2].fitness)
    print("****************************************************")
    if hill_climbing_result[2].fitness > simulated_annealing_result[2].fitness:
        best_result = hill_climbing_result[2]
    else:
        best_result = simulated_annealing_result[2]
    print("code elapsed time is %.6f seconds.\ncoordinates and fitness of best answer is : " % (
            time() - start_exec_time), printer(best_result.coordinates), "\n", best_result.fitness,
          "\nwitch means the error is : ",
          round(hill_climbing_result[2].fitness / worst_fitness * Decimal(100), 2), " percents.")


def exec_algo(func) -> list:
    results = []
    for i in range(algo_exec_numbers):
        node = Node(initial_point_generator())
        if step_length >= 1:
            d = truncate(step_length * random(), 1)
        else:
            d = truncate(random(), 1)
        if d == Decimal(0):
            d = Decimal(5) / Decimal(10)
        results.append(func(node, d))
    return best(results)


algo_exec_numbers = 10
getcontext().prec = 6
interval_start = 0
interval_end = 0
step_length = 0
equations = []
num_of_params = 0
worst_fitness = 0
max_steps_sas = 0
main()
