#test ppTypesFun

from ppTypesFun import *

PATH = {"_partialPlant": 1}
PartialPlantTypes = ['ps','cp','cp','wt']

x = ppTypesFun(PATH, PartialPlantTypes)
print(x)

#test cpNumFun

from cpNumFun import *

PATH = {"_partialPlant": 1}
PartialPlantTypes = ['ps','cp','cp','wt']
NumChemicalProductions = [2,1]

x = cpNumFun(PATH, PartialPlantTypes, NumChemicalProductions)
print(x)

#test cpTypesFun

from cpTypesFun import *

PATH = {"_partialPlant": 2, "_chemicalProduction": 1}
PartialPlantTypes = ['ps','cp','cp','wt']
ChemicalProductionTypes = [['acid','base'], ['acid']]

x = cpTypesFun(PATH, PartialPlantTypes, ChemicalProductionTypes)
print(x)

#test cpCtrlFun

from cpCtrlFun import *

PATH = {"_partialPlant": 2, "_chemicalProduction": 1}
PartialPlantTypes = ['ps','cp','cp','wt']
NumCtrlSysChemicalProductions = [[5,4],[3]]

x = cpCtrlFun(PATH, PartialPlantTypes, NumCtrlSysChemicalProductions)
print(x)