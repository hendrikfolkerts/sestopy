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

The program can be executed from source. Python3 with PyQt5 needs to be
installed and the Python executable needs to be on the path. Open a shell
and change with the cd command to the SESToPy directory. The program then can
be started with the shell command:
- in Windows: python main.py
- in Linux: python3 main.py

Build as executable  
SESToPy can alternatively be built as executable for Windows and Linux. More
information on this is in the documentation. This is not preferred and not
tested in new program versions. The created executable file in the program
directory has the name "SESToPy". 

Execution in Docker  
The program can alternatively be executed as standalone application in a Docker
container. Instructions are in the README file in the Docker directory of this
program.

CHANGELOG
- added: couplings, pruning, flattening
- reading a tree from file now with uid
- uniformity now results to nodes with different uid
- couplings: Ports have a type
- Socket client connection

KNOWN BUGS, NOTES, TODO
- aspectrules + specrules result = ``'' does not appear
- if a node gets the name of another node, the alternating mode can be violated
- selections constraints in pruning ignored
- error in semantic conditions function updateModel -> program crashes from time to time
- Undo / Redo not implemented
- In documentation: update citations like in this README

LICENSE

This application is licensed under GNU GPLv3.

HOW TO CITE

Folkerts, H., Pawletta, T., Deatcu, C., and Hartmann, S. (2019). A Python Framework for
Model Specification and Automatic Model Generation for Multiple Simulators. In: Proc. of
ASIM Workshop 2019 - ARGESIM Report 57, ASIM Mitteilung AM 170. ARGESIM/ASIM Pub.
TU Vienna, Austria, 02/2019, 69-75. (Print ISBN 978-3-901608-06-3)

Folkerts, H., Deatcu, C., Pawletta, T., Hartmann, S. (2019). Python-Based eSES/MB
Framework: Model Specification and Automatic Model Generation for Multiple Simulators.
SNE - Simulation Notes Europe Journal, ARGESIM Pub. Vienna, SNE 29(4)2019, 207-215.
(DOI: 10.11128/sne.29.tn.10497),(Selected EUROSIM 2019 Postconf. Publ.)

Folkerts, H., Pawletta, T., Deatcu, C., Santucci, J.F., Capocchi, L. (2019). An Integrated
Modeling, Simulation and Experimentation Environment in Python Based on SES/MB and DEVS.
Proc. of the 2019 Summer Simulation Conference, ACM Digital Lib., 2019 July 22-24, Berlin,
Germany, 12 pages.

Folkerts, H., Pawletta, T., Deatcu, C., Zeigler, B. (2020). Automated, Reactive Pruning
of System Entity Structures for Simulation Engineering. SCS SpringSim'20, May 19-May 21,
2020, Virtual Conference (Corona pand.), 12 pages.

Folkerts, H., Pawletta, T., Deatcu, C. (2021). Model Generation for Multiple Simulators
Using SES/MB and FMI. SNE - Simulation Notes Europe Journal, ARGESIM Pub. Vienna,
SNE 31(1) 2021, 25-32. (DOI: 10.11128/sne.31.tn.10554), (Selected ASIM 2020 Postconf. Publ.)