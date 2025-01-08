\* SantaToyDistribution *\
Maximize
MaximizeFactoryToChildAssignments: FactoryToChild_(1,_2)
 + FactoryToChild_(1,_4) + FactoryToChild_(1,_5) + FactoryToChild_(2,_4)
 + FactoryToChild_(3,_1) + FactoryToChild_(3,_3)
Subject To
ChildSatisfactionAndRequest_4: FactoryToChild_(1,_4) + FactoryToChild_(2,_4)
 <= 1
FactoryCapacity_1: FactoryToChild_(1,_2) + FactoryToChild_(1,_4)
 + FactoryToChild_(1,_5) <= 1
MaxExport_1: FactoryToChild_(1,_4) + FactoryToChild_(1,_5) <= 1
MinToysInCirculation_1: FactoryToChild_(1,_2) + FactoryToChild_(3,_1) >= 2
MinToysInCirculation_3: FactoryToChild_(1,_4) + FactoryToChild_(1,_5)
 + FactoryToChild_(2,_4) >= 2
Binaries
FactoryToChild_(1,_2)
FactoryToChild_(1,_4)
FactoryToChild_(1,_5)
FactoryToChild_(2,_4)
FactoryToChild_(3,_1)
FactoryToChild_(3,_3)
End
