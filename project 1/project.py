# YA HOSSEIN
from decimal import Decimal, getcontext, Overflow, InvalidOperation, DivisionByZero
import heapq
from random import shuffle, randint, choice, random, sample
import math
from time import time
from copy import deepcopy


class Node:
    def __init__(self, val) -> None:
        self.value = val
        self.right = None
        self.left = None

    def __repr__(self) -> str:
        s = self.value + " right is: "
        if self.right:
            s += self.right.value
        else:
            s += "None"
        s += " left is: "
        if self.left:
            s += self.left.value
        else:
            s += "None"
        return s


def truncate(x: float, precision: int) -> Decimal:
    y = 10 ** precision
    x = int(x * y)
    return Decimal(x) / y


def subtree_size(root: Node) -> int:
    if not root:
        return 0
    else:
        return subtree_size(root.left) + subtree_size(root.right) + 1


def evaluator(s: str, variable: Decimal) -> Decimal:
    sin = math.sin
    cos = math.cos
    exp = math.exp
    x = variable.__float__()
    return Decimal(truncate(eval(s), 6))


class Function:
    binary_operands = ['/', '*', '+', '-', 'pow']
    unary_operands = ['sin', 'cos', 'exp']
    all_values = ['binary', 'unary', 'x', 'constant']

    def __hash__(self) -> int:
        return self.string_function.__hash__()

    def __eq__(self, o) -> bool:
        return self.string_function.__hash__() == o.string_function.__hash__()

    def __gt__(self, other):
        return self.fitness > other.fitness

    def fit(self) -> int:
        fitness = Decimal(0)
        for t in inp:
            calculate = self.calculate(self.root, t[0])
            try:
                fitness += calculate
            except InvalidOperation:
                raise SyntaxError
        fitness /= Decimal(len(inp))
        return -abs(fitness - goal)

    def random_operator(self, typ: str) -> str:
        if typ == 'binary':
            return self.random_binary_operand()
        elif typ == 'unary':
            return self.random_unary_operand()
        elif typ == 'constant':
            return Decimal(randint(-max_functions_constant, max_functions_constant))
        elif typ == 'x':
            return 'x'

    @staticmethod
    def random_binary_operand(not_this_operand=None) -> str:
        x = randint(0, 4)
        if not_this_operand:
            while Function.binary_operands[x] == not_this_operand:
                x = randint(0, 4)
        return Function.binary_operands[x]

    @staticmethod
    def random_unary_operand(not_this_operand=None) -> str:
        x = randint(0, 2)
        if not_this_operand:
            while Function.unary_operands[x] == not_this_operand:
                x = randint(0, 2)
        return Function.unary_operands[x]

    @staticmethod
    def is_binary(node: Node) -> bool:
        return node.value in Function.binary_operands

    @staticmethod
    def is_unary(node: Node) -> bool:
        return node.value in Function.unary_operands

    def x_or_constant(self) -> str:
        y = random()
        if y < 0.9:
            return 'x'
        else:
            return self.random_operator('constant')

    def generate_function(self, length: int, root: Node):
        if self.is_unary(root):
            if length < 2:
                root.right = Node(self.x_or_constant())
                return
            elif length == 2:
                root.right = Node(self.random_operator('unary'))
                self.generate_function(length - 1, root.right)
            else:
                root.right = Node(self.random_operator(choice(self.all_values)))
                self.generate_function(length - 1, root.right)
        elif root.value == 'x' or type(root.value) is Decimal:
            return
        elif self.is_binary(root):
            if length < 2:
                raise SyntaxError(root)
            elif length == 2:
                root.right = Node(self.x_or_constant())
                root.left = Node(self.x_or_constant())
                return
            else:
                root.right = Node(self.random_operator(choice(self.all_values)))
                self.generate_function(length - 2, root.right)
                y = length - subtree_size(root.right)
                if y < 2:
                    root.left = Node(self.x_or_constant())
                    return
                elif y == 2:
                    root.left = Node(self.random_operator('unary'))
                    self.generate_function(1, root.left)
                else:
                    root.left = Node(self.random_operator(choice(self.all_values)))
                    self.generate_function(y - 1, root.left)

    def in_order(self, root: Node):
        if root:
            self.string_function += '('
            self.in_order(root.left)
            self.string_function += root.value.__str__()
            self.in_order(root.right)
            self.string_function += ')'

    def calculate(self, root: Node, x: Decimal) -> Decimal:
        try:
            if root:
                if isinstance(root.value, Decimal) or root.value is int:
                    return Decimal(root.value)
                elif root.value is 'x':
                    return x
                elif root.value is '+':
                    return self.calculate(root.left, x) + self.calculate(root.right, x)
                elif root.value is '-':
                    return self.calculate(root.left, x) - self.calculate(root.right, x)
                elif root.value is '*':
                    return self.calculate(root.left, x) * self.calculate(root.right, x)
                elif root.value is '/':
                    return self.calculate(root.left, x) / self.calculate(root.right, x)
                elif root.value is 'sin':
                    return truncate(math.sin(self.calculate(root.right, x)), 6)
                elif root.value is 'cos':
                    return truncate(math.cos(self.calculate(root.right, x)), 6)
                elif root.value is 'exp':
                    return self.calculate(root.right, x).exp()
                elif root.value is 'pow':
                    return self.calculate(root.left, x) ** self.calculate(root.right, x)
        except Overflow:
            raise SyntaxError
        except InvalidOperation:
            raise SyntaxError()
        except DivisionByZero:
            raise SyntaxError
        except ValueError:
            raise SyntaxError
        except TypeError:
            raise SyntaxError

    def __init__(self, n: int) -> None:
        self.string_function = ''
        self.size = n
        successful = False
        while not successful:
            try:
                self.root = Node(self.random_operator(choice(['binary', 'unary'])))
                self.generate_function(n - 1, self.root)
                self.in_order(self.root)
                self.fitness = self.fit()
                successful = True
            except SyntaxError:
                self.string_function = ''

    def __repr__(self) -> str:
        s = self.string_function
        s += '\t\twith fitness: '
        s += self.fitness.__str__()
        return s


def random_traverse(func: Function) -> tuple:
    depth = randint(1, subtree_size(func.root))
    node = func.root
    father = None
    for i in range(2, depth):
        x = choice(['right', 'left'])
        if x is 'right' and node.right:
            father = node
            node = node.right
        elif x is 'left' and node.left:
            father = node
            node = node.left
    return node, father


def generation_generator(n: int) -> list:
    generation = []
    for i in range(n):
        x = randint(2, max_tree_function_height)
        func = Function(x)
        heapq.heappush(generation, func)
    return generation


def swap_subtrees(individual1: Function, individual2: Function):
    nd1, fath1 = random_traverse(individual1)
    nd2, fath2 = random_traverse(individual2)
    if not fath1 and nd1 is individual1.root:
        if not fath2 and nd2 is individual2.root:
            return 'nothing'
        else:
            if fath2.right is nd2:
                fath2.right = individual1.root
                individual1.root = nd2
            elif fath2.left is nd2:
                fath2.left = individual1.root
                individual1.root = nd2
    elif not fath2 and nd2 is individual2.root:
        if fath1.right is nd1:
            fath1.right = individual2.root
            individual2.root = nd1
        elif fath1.left is nd1:
            fath1.left = individual2.root
            individual2.root = nd1
    else:
        if fath1.right is nd1:
            if fath2.right is nd2:
                fath1.right = nd2
                fath2.right = nd1
            elif fath2.left is nd2:
                fath1.right = nd2
                fath2.left = nd1
        elif fath1.left is nd1:
            if fath2.right is nd2:
                fath1.left = nd2
                fath2.right = nd1
            elif fath2.left is nd2:
                fath1.left = nd2
                fath2.left = nd1


def crossover(individual1: Function, individual2: Function) -> tuple:
    successful = False
    while not successful:
        if swap_subtrees(individual1, individual2) is 'nothing':
            break
        try:
            for indi in [individual1, individual2]:
                indi.string_function = ''
                indi.in_order(indi.root)
                indi.fitness = indi.fit()
            successful = True
        except SyntaxError:
            pass
    return individual1, individual2


def mutation(individual: Function) -> Function:
    node = random_traverse(individual)[0]
    if Function.is_binary(node):
        node.value = Function.random_binary_operand(not_this_operand=node.value)
    elif Function.is_unary(node):
        node.value = Function.random_unary_operand(not_this_operand=node.value)
    else:
        node.value = individual.x_or_constant()
    individual.string_function = ''
    individual.in_order(individual.root)
    individual.fitness = individual.fit()
    return individual


def genetic_programming() -> list:
    n = len(inp) * first_generation_multiplier
    current_population = generation_generator(n)
    calculate_fitness_num = n
    generation_counter = 0

    while len(current_population) >= 20:
        if max(current_population).fitness == Decimal(0):
            return [max(current_population), generation_counter, calculate_fitness_num, n]
        calculate_fitness_num, current_population, generation_counter = policy(calculate_fitness_num,
                                                                               current_population, generation_counter)
        current_population = remove_constant_functions(current_population)
    return [max(current_population), generation_counter, calculate_fitness_num, n]


def remove_constant_functions(current_population):
    temp = []
    for item in current_population:
        if item.string_function.find('(x)') != -1:
            heapq.heappush(temp, item)
    current_population = temp
    return current_population


def policy(calculate_fitness_num, current_population, generation_counter):
    length = len(current_population)
    mid = length // 2
    a = heapq.nlargest(mid, current_population)
    b = heapq.nsmallest(mid, current_population)
    shuffle(a)
    shuffle(b)
    x = heapq.nsmallest(length // 20, current_population)[-1].fitness
    temp = []
    for itm in heapq.nlargest(length // 10, current_population):
        t = deepcopy(itm)
        heapq.heappush(temp, t)
    for i in range(mid):
        children = crossover(a[i], b[i])
        for j in range(2):
            if children[j].fitness >= x:
                heapq.heappush(temp, children[j])
            else:
                try:
                    node = mutation(children[j])
                except SyntaxError:
                    continue
                # print('mutation')        uncomment this statement to get notified when a successful mutation occur
                if node.fitness >= x:
                    heapq.heappush(temp, node)
    current_population = list(dict.fromkeys(temp))
    calculate_fitness_num += len(current_population)
    generation_counter += 1

    # uncomment this statement to see each generation population, and its best individual
    # print(generation_counter, len(current_population), heapq.nlargest(1, current_population))
    return calculate_fitness_num, current_population, generation_counter


def get_input_and_set_goal():
    global goal
    yn = input("IF you want to enter the target function press 'Y'.for just entering some points press 'N'.\n")
    n = int(input("PLEASE enter number of learning points(at least 10) : "))
    if yn is 'Y':
        successful = False
        while not successful:
            s = input("PLEASE enter the function. note to use 2**3 instead of 2^3 and use 'x' as the input of " +
                      "function (enter f(x)):\n")
            try:
                for u in sample(range(-100, 100), n):
                    x = Decimal(u)
                    y = evaluator(s, x)
                    inp.append((x, y))
                    goal += y
                successful = True
            except SyntaxError:
                print("GOT a SyntaxError while evaluating the input! please try again : \n")
    elif yn is 'N':
        print("NOW enter the points. separate the coordination with space : ")
        for i in range(n):
            x, y = map(Decimal, input().split())
            inp.append((x, y))
            goal += y
    else:
        raise RuntimeError("ENTER Y or N")
    goal /= Decimal(n)


def print_result(result: list, start_time: float):
    print("GENETIC PROGRAMMING started  from a generation with  " + str(result[3]) + "  individuals.\nAFTER  " +
          str(result[1]) + "  generations and calculating fitness of  " + str(result[2]) +
          "  individual, IT reached a function with formula :\n" + result[0].string_function + "\nAND fitness of : "
          + str(result[0].fitness) + "\nALGORITHM found this result in %.6f seconds" % (time() - start_time))


def main():
    get_input_and_set_goal()
    start_time = time()
    print_result(genetic_programming(), start_time)


getcontext().prec = 6
first_generation_multiplier = 500
max_tree_function_height = 15
max_functions_constant = 100
goal = 0
inp = []
main()
