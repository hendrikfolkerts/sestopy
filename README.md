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
installed and the Python executable needs to be on the path. The program
then can be started with the shell command:
- in Windows: python main.py
- in Linux: python3 main.py

Versions built for Windows or Linux have an executable file with the name
"SESToPy" in the program directory.

CHANGELOG
- added: couplings, pruning, flattening
- reading a tree from file now with uid
- uniformity now results to nodes with different uid
- couplings: Ports have a type
- Socket client connection

KNOWN BUGS, NOTES, TODO
- aspectrules + specrules result = ``'' does not appear
- selections constraints in pruning ignored
- error in semantic conditions function updateModel -> program crashes from time to time

LICENSE

This application is licensed under GNU GPLv3.

HOW TO CITE

Folkerts, H., Deatcu, C., Pawletta, T., Hartmann, S. (2019). Python-Based eSES/MB
Framework: Model Specification and Automatic Model Generation for Multiple Simulators.
SNE - Simulation Notes Europe Journal, ARGESIM Pub. Vienna, SNE 29(4)2019, 207-215.
(DOI: 10.11128/sne.29.tn.10497),(Selected EUROSIM 2019 Postconf. Publ.)

Folkerts, H., Pawletta, T., Deatcu, C., and Hartmann, S. (2019). A Python Framework for
Model Specification and Automatic Model Generation for Multiple Simulators. In: Proc. of
ASIM Workshop 2019 - ARGESIM Report 57, ASIM Mitteilung AM 170. ARGESIM/ASIM Pub.
TU Vienna, Austria, 02/2019, 69-75. (Print ISBN 978-3-901608-06-3)

Folkerts, H., Pawletta, T., Deatcu, T. (2019). An Integrated Modeling,
Simulation and Experimentation Environment in Python Based on SES/MB and DEVS.
Proc. of the 2019 Summer Simulation Conference, ACM Digital Lib.,
2019 July 22-24, Berlin, Germany, 12 pages.