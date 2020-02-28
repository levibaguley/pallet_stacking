# pallet_stacking
This is a project I worked on from May to July 2019. It is a set of tools that allowed me to simulate the distribution of how long it would take a pallet-stacking robot (called a gantry in this project) to stack an order of pallets of various frozen foods given various conditions. These conditions include the size and shape of the area the robot works in and where the robot stacks the pallets within that area. [This](https://youtu.be/y0LIWy-ASEs) is what the robot would be like.

This is the configuration referred to as the "base case". 

<img width="400" src="https://github.com/levibaguley/pallet_stacking/blob/master/base_case.jpg?raw=true">
Running the simulation on the base case produces a distribution like below. The "Build Pallet Cost" on the x-axis refers to the total number of spaces/squares in the grid the gantry had to travel to build a particular pallet.

<img width="900" src="https://github.com/levibaguley/pallet_stacking/blob/master/dist.png?raw=true">

cost_distribution.py is the driver file for the simulation and UML.pdf is well... the pdf of the UML.
