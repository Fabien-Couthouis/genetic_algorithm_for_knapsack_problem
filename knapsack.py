# Genetic algorithm implementation for knapsack problem - V1 - searching algorithms course (L. Simon)
# By F. Couthouis
import numpy as np


class Item():
    """Knapsack item with weight and value"""

    def __init__(self, id, weight, value):
        self.id = id
        self.weight = weight
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented

        return self.id == other.id

    def __str__(self):
        return "Item n°{}  with weight {} and value : {}".format(self.id, self.weight, self.value)


class Knapsack():
    """Knapsack object 

    Args:
        max_weight (int): Max knapsack weight
        possible_items (list<Items>): List of all items that could be put in the knapsack
    """

    def __init__(self, max_weight, possible_items=None):
        self.weight = 0
        self.max_weight = max_weight
        self.items = []
        self.possible_items = [] if possible_items is None else possible_items.copy()

    def get_fitness(self):
        "0 if weight > max weight, sum of values otherwise"
        fitness = 0
        if self.weight <= self.max_weight:
            fitness = sum(item.value for item in self.items)
        return fitness

    def add_item(self, item):
        if item not in self.items:
            self.weight += item.weight
            self.items.append(item)
            self.possible_items.remove(item)

    def remove_item(self, item):
        if item in self.items:
            self.weight -= item.weight
            self.items.remove(item)
            self.possible_items.append(item)

    def add_items(self, items):
        for item in items:
            self.add_item(item)

    def mutate(self):
        """Change an item in item list for another which is not already in the knapsack"""
        # Check if list is not empty
        if self.possible_items:
            new_item = np.random.choice(self.possible_items)
            old_item = np.random.choice(self.items)
            self.remove_item(old_item)
            self.add_item(new_item)


class Darwin():
    """
    Genetic algorithm implementation 

    Args:
            nb_items (int): Number of possible different items
            max_item_weight (int)
            max_item_val (int)
            max_knapsack_weight (int)
            pop_size (int, optional: default=30) : Size of the population
            mutation_rate (float, optional: default=0.1): Between 0 and 1
            choice (str, optional: default="wheel"): Parent selection method ("wheel" or "tournament")
            keep_parents (bol, optional: default=False): Keep parents in the next population
    """

    def __init__(self, nb_items, max_item_weight, max_item_val, max_knapsack_weight,
                 pop_size=20, mutation_rate=0.01, choice="wheel", keep_parents=False):
        self.nb_items = nb_items
        self.max_knapsack_weight = max_knapsack_weight
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.choice = choice
        self.keep_parents = keep_parents
        self.population = []

        # Generate the items
        self.weights = np.random.randint(1, max_item_weight+1, size=nb_items)
        self.values = np.random.randint(1, max_item_val+1, size=nb_items)
        self.items = [Item(i, w, v)
                      for i, (w, v) in enumerate(zip(self.weights, self.values))]

        self.generate_population(pop_size)

    def generate_population(self, pop_size):
        """First population generation"""
        # Generate knapsacks individuals
        for _ in range(pop_size):
            knapsack = Knapsack(self.max_knapsack_weight, self.items)
            nb_items = np.random.randint(self.nb_items+1)

            # Add items to the knapsack
            for _ in range(nb_items):
                # Knapsack already contains all items
                if not knapsack.possible_items:
                    break
                selected_item = np.random.choice(knapsack.possible_items)
                knapsack.add_item(selected_item)

            self.population.append(knapsack)

    def replace_population(self, new_population):
        self.population = new_population

    def sort_pop_by_fitness(self):
        self.population.sort(key=lambda knapsack: knapsack.get_fitness())

    def choose_parents_wheel(self):
        """Use selection wheel method to select parents"""
        self.sort_pop_by_fitness()
        wheel_cursor = np.random.randint(0, self.pop_size)
        parents = self.population[wheel_cursor:]

        return parents

    def choose_parents_tournament(self):
        """Use tournament method to select parents"""
        max_nb_rounds = int(np.log2(self.pop_size))
        nb_rounds = np.random.randint(1, max_nb_rounds)
        parents = []
        not_selected = self.population.copy()

        for _ in range(nb_rounds):
            while len(not_selected) > 2:
                p1 = np.random.choice(not_selected)
                not_selected.remove(p1)

                p2 = np.random.choice(not_selected)
                not_selected.remove(p2)

                selected_parent = p1 if p1.get_fitness() > p2.get_fitness() else p2
                parents.append(selected_parent)

        return parents

    def choose_parents(self):
        if self.choice == "wheel":
            return self.choose_parents_wheel()
        else:
            return self.choose_parents_tournament()

    def natural_selection(self, nb_iter):
        """Genetic algorithm loop : selection of the best individuals"""
        for _ in range(nb_iter):
            parents = self.choose_parents()
            new_population = []

            if self.keep_parents:
                new_population.extend(parents)

            while len(new_population) < len(self.population):
                new_indiv = self.make_child(parents)
                new_population.append(new_indiv)

            self.replace_population(new_population)
            # print(sum(knapsack.get_fitness() for knapsack in self.population))
        self.sort_pop_by_fitness()

    def make_child(self, possible_parents):
        """
        Return a child given the list of possible parent.
        The child shares the features from his parents (thanks to a crossover point), with a little chance to mutate
        """
        p1 = np.random.choice(possible_parents)
        p2 = np.random.choice(possible_parents)
        child = Knapsack(self.max_knapsack_weight, self.items)
        crossover_point = np.random.randint(len(p1.items)+1)

        child.add_items(p1.items[:crossover_point])
        child.add_items(p2.items[crossover_point:])

        if np.random.random_sample() <= self.mutation_rate:
            child.mutate()

        return child


if __name__ == "__main__":
    np.random.seed(42)
    darwin = Darwin(nb_items=10, max_item_weight=3, max_item_val=10, max_knapsack_weight=20,
                    pop_size=30, mutation_rate=0.01, choice="wheel", keep_parents=True)
    darwin.natural_selection(nb_iter=30)

    # show worst fitness in the population
    print(darwin.population[0].get_fitness())
    # best
    print(darwin.population[-1].get_fitness())
    # best fitness = 55 ?
    # wheel selection method seems to converge faster with keep_parents set to True and a mutation rate of 1%
