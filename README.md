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
