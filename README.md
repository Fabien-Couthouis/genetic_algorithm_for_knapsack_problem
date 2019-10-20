# Genetic algorithm implementatino for knapsack problem 

<cite>"The knapsack problem or rucksack problem is a problem in combinatorial optimization: Given a set of items, each with a weight and a value, determine the number of each item to include in a collection so that the total weight is less than or equal to a given limit and the total value is as large as possible. It derives its name from the problem faced by someone who is constrained by a fixed-size knapsack and must fill it with the most valuable items."</cite> - https://en.wikipedia.org/wiki/Knapsack_problem

The code provided here implements genetics algorithms to solve knapsack problem. Genetic algorithms are metaheuristic algorithms inspired by the process of natural selection to generate solutions to optimization and search problems.

## Usage
```python
    #Set random seed
    np.random.seed(42)

    #Set parameters
    darwin = Darwin(nb_items=10, max_item_weight=3, max_item_val=10, max_knapsack_weight=20,
    pop_size=30, mutation_rate=0.01, choice="wheel", keep_parents=True)

    #Launch natural selection process for 100 iterations
    darwin.natural_selection(nb_iter=100)

    # Show worst and best fitness in the population
    print("Worst fitness: {} \nBest fitness: {}".format(
    darwin.population[0].get_fitness(),darwin.population[-1].get_fitness()))
```
## Algorithm details
Knapsacks and items are generated at random.

2 methods of parent selection are implemented here: 
* Selection wheel
* Tournament

Parents reproduction are made thanks to a crosssover point.



## Credits
Based on [Laurent Simon courses](https://www.labri.fr/perso/lsimon/ia-2019/recherche/) at [ENSEIRB-MATMECA](https://enseirb-matmeca.bordeaux-inp.fr/fr)  
