from model.model import Model

myModel = Model()
myModel.buildGraph("2015", "France")
bestPath, maxCost = myModel.bestPath(5)
print(maxCost)
for d in bestPath: print(d)
