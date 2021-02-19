# YA HEYDAR
class Node:
    def __init__(self, value: str, information_gain: float, remainder_entropy: float, entropy: float, children: list):
        self.value = value
        self.children = children
        self.label = "noValue"
        self.information_gain = information_gain
        self.remainder_entropy = remainder_entropy
        self.entropy = entropy

    @staticmethod
    def print_tree(root):
        if root:
            print(
                "value = %s\tinBranch = %s\t entropy = %.3f\t remainderEntropy = %.3f\t informationGain = %.3f" % (
                    root.value, root.label, root.entropy, root.remainder_entropy, root.information_gain))
            for c in root.children:
                Node.print_tree(c)

    def set_label(self, father_attribute: str, this_branch_value: str):
        self.label = father_attribute + " = " + this_branch_value


class Sample:
    wait_estimate_values = {"0-10", "10-30", "30-60", ">60"}
    patrons_values = {"None", "Some", "Full"}
    food_type_values = {"French", "Thai", "Burger", "Italian"}
    price_values = {"$", "$$", "$$$"}
    boolean_values = {"Yes", "No"}
    attributes_values = ["alternate", "bar", "fri_sat", "hungry", "patrons", "price", "raining", "reservation",
                         "food_type", "wait_estimate"]

    def __init__(self, alternate: str, bar: str, fri_sat: str, hungry: str, patrons: str, price: str, raining: str,
                 reservation: str, food_type: str, wait_estimate, goal: str):
        self.hungry = hungry
        self.patrons = patrons
        self.wait_estimate = wait_estimate
        self.alternate = alternate
        self.reservation = reservation
        self.raining = raining
        self.bar = bar
        self.fri_sat = fri_sat
        self.food_type = food_type
        self.price = price
        self.goal = goal

    @staticmethod
    def same_classification(examples: list) -> bool:
        same = examples[0].goal
        for e in examples:
            if e.goal != same:
                return False
        return True

    @staticmethod
    def get_values(attr: str) -> set:
        if attr == "patrons":
            return Sample.patrons_values
        elif attr == "food_type":
            return Sample.food_type_values
        elif attr == "price":
            return Sample.price_values
        elif attr == "wait_estimate":
            return Sample.wait_estimate_values
        else:
            return Sample.boolean_values

    def __repr__(self) -> str:
        return self.alternate + self.bar + self.fri_sat + self.hungry + self.patrons + self.price + self.raining + \
               self.reservation + self.food_type + self.wait_estimate + self.goal
