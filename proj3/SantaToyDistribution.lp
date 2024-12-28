\* SantaToyDistribution *\
Maximize
MaximizeSatisfiedChildren: ChildSatisfied_1 + ChildSatisfied_2
 + ChildSatisfied_3 + ChildSatisfied_4 + ChildSatisfied_5
Subject To
ChildRequest_1: FactoryToChild_(3,_1) <= 1
ChildRequest_2: FactoryToChild_(1,_2) <= 1
ChildRequest_3: FactoryToChild_(3,_3) <= 1
ChildRequest_4: FactoryToChild_(1,_4) + FactoryToChild_(2,_4) <= 1
ChildRequest_5: FactoryToChild_(1,_5) <= 1
ChildSatisfaction_1: - ChildSatisfied_1 + FactoryToChild_(3,_1) = 0
ChildSatisfaction_2: - ChildSatisfied_2 + FactoryToChild_(1,_2) = 0
ChildSatisfaction_3: - ChildSatisfied_3 + FactoryToChild_(3,_3) = 0
ChildSatisfaction_4: - ChildSatisfied_4 + FactoryToChild_(1,_4)
 + FactoryToChild_(2,_4) = 0
ChildSatisfaction_5: - ChildSatisfied_5 + FactoryToChild_(1,_5) = 0
FactoryCapacity_1: FactoryToChild_(1,_2) + FactoryToChild_(1,_4)
 + FactoryToChild_(1,_5) <= 1
FactoryCapacity_2: FactoryToChild_(2,_4) <= 2
FactoryCapacity_3: FactoryToChild_(3,_1) + FactoryToChild_(3,_3) <= 2
MaxExport_1: FactoryToChild_(1,_4) + FactoryToChild_(1,_5) <= 1
MaxExport_2: FactoryToChild_(2,_4) <= 2
MaxExport_3: FactoryToChild_(3,_1) + FactoryToChild_(3,_3) <= 1
MinToysInCirculation_1: FactoryToChild_(1,_2) + FactoryToChild_(3,_1) >= 1
MinToysInCirculation_2: FactoryToChild_(3,_3) >= 1
MinToysInCirculation_3: FactoryToChild_(1,_4) + FactoryToChild_(1,_5)
 + FactoryToChild_(2,_4) >= 1
Binaries
ChildSatisfied_1
ChildSatisfied_2
ChildSatisfied_3
ChildSatisfied_4
ChildSatisfied_5
FactoryToChild_(1,_2)
FactoryToChild_(1,_4)
FactoryToChild_(1,_5)
FactoryToChild_(2,_4)
FactoryToChild_(3,_1)
FactoryToChild_(3,_3)
End
