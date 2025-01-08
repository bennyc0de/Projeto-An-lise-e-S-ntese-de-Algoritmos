\* SantaToyDistribution *\
Maximize
OBJ: F1C2 + F1C4 + F1C5 + F2C4 + F3C1 + F3C3
Subject To
FactoryCapacity_1: F1C2 + F1C4 + F1C5 <= 1
MaxExport_1: F1C4 + F1C5 <= 1
MaxExport_3: F3C1 + F3C3 <= 1
MinToysInCirculation_1: F1C2 + F3C1 >= 1
MinToysInCirculation_2: F3C3 >= 1
MinToysInCirculation_3: F1C4 + F1C5 + F2C4 >= 1
_C1: F1C4 + F2C4 <= 1
Binaries
F1C2
F1C4
F1C5
F2C4
F3C1
F3C3
End
