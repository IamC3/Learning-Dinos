from random import uniform, randint
import projectVar as V

class brain():
  def __init__(self, size):
    super().__init__()
    self.directions = []
    for x in range(size):
      self.directions.append(-1)
    self.step = 0
    self.randomize()
    
  def randomize(self):
    count = 0
    for i in self.directions:
      randomAngle = uniform(0, 360)
      go = V.vec(V.MAXVEL, 0)
      self.directions[count] = go.rotate(randomAngle)
      count += 1

  def clone(self):
    clone = brain(V.BRAINSIZE)
    count = 0
    for direct in self.directions:
      clone.directions[count] = direct
      count += 1
    return clone

  def mutate(self):
    count = 0
    for direct in self.directions:
      rand = randint(0, 1000)
      if rand < V.URANIUM:
        randomAngle = uniform(0, 360)
        self.directions[count] = direct.rotate(randomAngle)
      count += 1
      