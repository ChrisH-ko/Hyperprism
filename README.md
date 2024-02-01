# Hyperprism
## Chips & Circuits

Chips (or more precisely: integrated circuits) are found in your PC, MacBook, Android Phone and microwave oven where they perform a diversity of functions, ranging from timekeeping and motor control to arithmetic and logic. Basically a small plate of silicon, chips are usually designed logically and subsequentially transformed to a list of connectable gates. This list, commonly known as a netlist is finally transformed into a 2-dimensional design on a silicon base.

This last step however, the physical real-world process of connecting the gates, is highly volatile. Good arrangements with short nets lead to faster circuits, whereas poor arrangements with long nets lead to slower circuits. Besides, shorter nets are cheaper than long nets, so there is no doubt that a good arrangement of logical gates and short nets between them is of vital importance, both economically and performancewise.

To make things easier, we will consider the wiring problem only. The gates have already been arranged, and all it takes is finding very short wiring patterns.

### Requirements
This project has been written in Python 3.8. Any neccesary packages can be found in requirements.txt.

## How to use
```
python3.8 main.py
```
When running the program, you will be asked to enter a chip_id and net_id. These can be found in **/gates&netlists**.
Having succesfully selected a chip and netlist, the program will provide 3 options:
- *solve*
- *experiment*
- *quit*

Selecting *solve* will start the solver. Here you can choose a combination of algorithms to solve the netlist with.

Selecting *experiment* will open up the experiment menu, where you may choose an experiment to run for a certain amount of iterations.

Selecting *quit* will stop the program.

## Solve
To solve the chip and netlist, you will be asked to enter a *netsolver* and *pathfinder*. The *netsolver* selects an order in which the nets should be solved and the *pathfinder* connects the gates in each net. In other words, the algorithms provided solve the models net by net.

The provided netsolvers include:
- *standard*
- *random*
- *shortest_first*
- *hardest_first*

*Standard* uses the provided net order from the netlist. *Random* shuffles the netlist in a random order. *Shortest_first* starts with the nets whose gates are closest together. *Hardest_first* starts with the nets whose gates have the most connections.

The provided pathfinders include:
- *standard*
- *make_space*

*Standard* connects the gates with the cheapest available path using the A* algorithm and the manhattan distance as the heuristic. *Make_space* is a variation on *standard*, whereby upon calculating the priority of a path, the influence of the path's length and manhattan distance gets discounted, it gets rewarded for staying on a higher layer as well as being above the target gate and it gets punished for being next to a gate that is not the startor end point of the net. In other words, this algorithm gives paths an incentive to try and make more space for other nets.

After having solved the model, its details are displayed as well as a visualization of the solution upon user request.

The latest solution will be saved, since *solve* can be selected once more to rewire the nets in an existing solution in an attempt to lower the cost by replacing them with shorter available wires. One can for instance run a netsolver with the *make_space* pathfinder and rewire the solution with a different netsolver using the *standard* pathfinder to obtain a chip with possibly a low cost.

## Experiment
To carry out an experiment, first select one from the ones provided. Those include:
- *baseline*
- *hillclimber*
- *simanneal*

After which you will be asked for the amount of iterations *i* to run the selected experiment on.

- *baseline*
This test will run the *random* netsolver with the *standard* pathfinder *i* times, recording the cost of each solution on the way. After which, the results can be displayed as a distribution of the costs of the possible solutions.

- *hillclimber*
This test will run a hillclimber algorithm on a provided solution of the model for *i* iterations. Since a solution is required to start this experiment, you will need to solve the model in *solve* beforehand. The hillclimber algorithm will take the netorder of the solution, change the position of one of the nets in the netorder and solve the model in the new netorder. If the new solution were to be better than the previous, the change is kept. You may select beforehand which pathfinder is used by the hillclimber and whether to only rewire the solution upon solving, or whether to start with an empty chip from scratch. The results of the algorithm can be displayed afterwards.

- *simanneal*
This test will run a simulated annealing algorithm on a provided solution of the model for *i* iterations same as hillclimber. The same details apply, except that with this algorithm, worse solutions have a certain probability to be kept, decreasing with each iteration as well as the difference in score with the current solution.   
