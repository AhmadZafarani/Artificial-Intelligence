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
    pregnancies_values = ["<0", "0-2", "2-4", "4-6", "6-8", "8-10", "10-12", "12-14", "14-16", ">16"]
    glucose_values = ["<0", "0-20", "20-40", "40-60", "60-80", "80-100", "100-120", "120-140", "140-160", "160-180",
                      ">180"]
    blood_pressure_values = ["<0", "0-12", "12-24", "24-36", "36-48", "48-60", "60-72", "72-84", "84-96", "96-108",
                             ">108"]
    skin_thickness_values = ["<0", "0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90",
                             ">90"]
    insulin_values = ["<0", "0-84", "84-168", "168-252", "252-336", "336-420", "420-494", "494-578", "578-662",
                      "662-746", "746-830", ">830"]
    bmi_values = ["<0", "0-7", "7-14", "14-21", "21-28", "28-35", "35-42", "42-49", "49-56", "56-63", ">63"]
    diabetes_pedigree_function_values = ["<0.078", "0.078-0.312", "0.312-0.546", "0.546-0.780", "0.780-1.014",
                                         "1.014-1.248", "1.248-1.482", "1.482-1.716", "1.716-1.950", "1.950-2.184",
                                         "2.184-2.418", ">2.418"]
    age_values = ["<21", "21-27", "27-33", "33-39", "39-45", "45-51", "51-57", "57-63", "63-69", "69-75", ">75"]
    attributes_values = ["pregnancies", "glucose", "blood_pressure", "skin_thickness", "insulin", "bmi",
                         "diabetes_pedigree_function", "age"]

    def __init__(self, pregnancies: str, glucose: str, blood_pressure: str, skin_thickness: str, insulin: str,
                 bmi: str, diabetes_pedigree_function: str, age: str, outcome: str):
        self.pregnancies = self.setter(0, 16, 2, int(pregnancies), self.pregnancies_values)
        self.glucose = self.setter(0, 180, 20, int(glucose), self.glucose_values)
        self.blood_pressure = self.setter(0, 108, 12, int(blood_pressure), self.blood_pressure_values)
        self.skin_thickness = self.setter(0, 90, 10, int(skin_thickness), self.skin_thickness_values)
        self.insulin = self.setter(0, 830, 84, int(insulin), self.insulin_values)
        self.bmi = self.setter(0, 63, 7, int(float(bmi) * 10) // 10, self.bmi_values)
        self.diabetes_pedigree_function = self.setter(78, 2418, 234, int(float(diabetes_pedigree_function) * 1000),
                                                      self.diabetes_pedigree_function_values)
        self.age = self.setter(21, 75, 6, int(age), self.age_values)
        self.outcome = outcome

    @staticmethod
    def same_classification(examples: list) -> bool:
        same = examples[0].outcome
        for e in examples:
            if e.outcome != same:
                return False
        return True

    @staticmethod
    def get_values(attr: str) -> list:
        if attr == "pregnancies":
            return Sample.pregnancies_values
        elif attr == "glucose":
            return Sample.glucose_values
        elif attr == "blood_pressure":
            return Sample.blood_pressure_values
        elif attr == "skin_thickness":
            return Sample.skin_thickness_values
        elif attr == "skin_thickness":
            return Sample.skin_thickness_values
        elif attr == "insulin":
            return Sample.insulin_values
        elif attr == "bmi":
            return Sample.bmi_values
        elif attr == "diabetes_pedigree_function":
            return Sample.diabetes_pedigree_function_values
        elif attr == "age":
            return Sample.age_values

    def __repr__(self) -> str:
        return self.pregnancies + self.glucose + self.blood_pressure + self.skin_thickness + self.insulin + self.bmi + \
               self.diabetes_pedigree_function + self.age + self.outcome

    @staticmethod
    def setter(inf: int, sup: int, interval_length: int, val: int, array: list) -> str:
        if val < inf:
            return array[0]
        elif val > sup:
            return array[-1]
        else:
            val -= inf
            return array[val // interval_length + 1]
