class BingoSimulation:
  inputData:[]
  exceptData:[]
  #載入輸入、期望array
  def __init__(self,inputData:[],exceptData:[]):
    self.inputData = inputData
    self.exceptData = exceptData

  def testAdd(self,a:int,b:int):
    return a + b


if __name__ == '__main__':
  bingoSimulation = BingoSimulation([],[])
  sum = bingoSimulation.testAdd(1,2)
  print('')