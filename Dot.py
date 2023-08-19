import pygame as pg
import projectVar as V
import Brain

class dot(pg.sprite.Sprite):
  def __init__(self, brain):
    super().__init__()
    pos = V.DOTSTART
    
    self.pos = V.vec(pos)
    self.vel = V.vec(0, 0)
    self.acc = V.vec(0, 0)
    self.brain = Brain.brain(brain)

    self.dead = False
    self.reachedGoal = False
    self.isBest = False

    self.fitness = 0
  
  def show(self):
    if V.STREAMLINED:
      if not self.dead and not self.reachedGoal and not self.isBest:
        pg.draw.circle(V.DISPLAYSURF, 0, (self.pos), V.dotsize, V.dotsize)
      elif self.dead:
        pg.draw.circle(V.DISPLAYSURF, (255, 0, 0), (self.pos), V.CORPSESIZE, V.CORPSESIZE)
      elif self.reachedGoal:
        pg.draw.circle(V.DISPLAYSURF, (0, 255, 0), (self.pos), V.GOALSIZE, V.GOALSIZE)
      elif self.isBest:
        pg.draw.circle(V.DISPLAYSURF, (0, 255, 255), (self.pos), V.CHAMPSIZE, V.CHAMPSIZE)
    elif V.DINO:
      if not self.dead and not self.reachedGoal and not self.isBest:
        image = V.DINODOT
      elif self.dead:
        image = V.DINOCORPSE
      elif self.reachedGoal and self.isBest:
        image = V.DINOCHAMPGOAL
      elif self.reachedGoal:
        image = V.DINOGOAL
      elif self.isBest:
        image = V.DINOCHAMP
      if not V.hdn or self.isBest:
        imgrect = image.get_rect(center = (self.pos))
      else:
        imgrect = (-100, -100)
      V.DISPLAYSURF.blit(image, imgrect)

  def move(self):
    if len(self.brain.directions) > self.brain.step:
      self.acc = self.brain.directions[self.brain.step]
      self.brain.step += 1
    else:
      self.dead = True
    self.vel += self.acc

    if self.vel.length() > V.MAXVEL:
      self.vel = self.vel.normalize()*V.MAXVEL
      
    self.pos += self.vel

  def update(self):
    if not self.dead and not self.reachedGoal:
      self.move()
      if self.pos.x < 2 or self.pos.y < 2 or self.pos.x > V.WIDTH-2 or self.pos.y > V.HEIGHT - 2:
        self.dead = True
      elif self.pos.distance_to(V.GOAL) < 7:
        self.reachedGoal = True
      for box in V.OBSTACLES[V.stage]:
        if self.pos.x > (box[2][0] - 2) and self.pos.x < (box[2][0] + box[2][2] + 2) and self.pos.y > (box[2][1] - 2) and self.pos.y < (box[2][1] + box[2][3] + 2):
          self.dead = True

  def calculateFitness(self):
    if self.reachedGoal:
      self.fitness = 1.0/16.0 + 10000.0/(self.brain.step**2/20)
    else:
      distanceToGoal = self.pos.distance_to(V.GOAL)
      self.fitness = 1.0/(distanceToGoal**2/20)

  def birth(self, minStep):
    baby = dot(minStep + 10)
    baby.brain = self.brain.clone()
    return baby