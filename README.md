# sestopy
INTRODUCTION
The software SESToPy supports the System Entity Structure (SES) infrastructure.
Purpose of the software is to model SES trees and support further processing.
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
couplings: node renamed -> change in couplings
aspectrules + specrules result = ``'' does not appear
selections constraints in pruning ignored yet
TreeView for showing the SES as tree -> graphviz, test with gvedit
error in semantic conditions function updateModel -> program crashes from time to time
