from model.model import Model

myModel = Model()
myModel.buildGraph("2015", "France")
print(myModel.getNumNodi())
print(myModel.getNumArchi())
