INTRODUCTION

The software SESToPy has been developed by the research group Computational
Engineering and Automation (CEA) at Wismar University of Applied Sciences.
Purpose of the software is ontology based modeling of system variants
(system structures and parameter configurations) using the
System Entity Structure (SES). It provides transformation methods for
deriving unique system variants.
Please read the documentation for further information.
The software is written in Python3 with PyQt5 as user interface.

EXECUTE

The program can be executed from source by the command:
python main.py      in Windows or
python3 main.py     in Linux
Versions built for Windows or Linux have an executable with the name
SESToPy
in the program directory.

CHANGELOG

added: couplings, pruning, flattening
reading a tree from file now with uid
uniformity now results to nodes with different uid

ToDo, Known Bugs, Notes
- couplings: node renamed -> change in couplings
- aspectrules + specrules result = ``'' does not appear
- selections constraints in pruning ignored yet
- TreeView for showing the SES as tree -> graphviz, test with gvedit
- error in semantic conditions function updateModel -> program crashes from time to time

LICENSE


HOW TO CITE

Folkerts, H., Pawletta, T., Deatcu, C., and Hartmann, S. (2019). A Python Framework for
Model Specification and Automatic Model Generation for Multiple Simulators. In: Proc. of
ASIM Workshop 2019 - ARGESIM Report 57, ASIM Mitteilung AM 170. ARGESIM/ASIM Pub.
TU Vienna, Austria, 02/2019, 69-75. (Print ISBN 978-3-901608-06-3)

Deatcu, C., Folkerts, H., Pawletta, T., Durak, U. (2018). Design Pattern For Variability
Modeling Using SES Ontology. SpringSim-Mod4Sim 2018, April 15-18, Baltimore, MD, USA,
Society for Modeling & Simulation International (SCS), 528-539.
(DOI: 10.22360/SpringSim.2018.Mod4Sim.004) 
