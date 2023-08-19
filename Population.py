import pygame as pg

from random import uniform

import projectVar as V
import Dot


class population():

    def __init__(self):
        super().__init__()
        self.fitnessSum = 0
        self.gen = 1
        self.bestDot = 0
        self.max = 0
        self.minStep = V.BRAINSIZE
        self.dots = pg.sprite.Group()
        for i in range(V.POPSIZE):
            self.dots.add(Dot.dot(V.BRAINSIZE))

    def show(self):
        for entity in reversed(list(self.dots)):
            entity.show()

    def update(self):
        for entity in self.dots:
            if entity.brain.step > self.minStep:
                entity.dead = True
            else:
                entity.update()

    def calculateFitness(self):
        for entity in self.dots:
            entity.calculateFitness()

    def allDotsDead(self):
        for entity in self.dots:
            if not entity.dead and not entity.reachedGoal:
                return False
        return True

    def naturalSelection(self):
        self.setBestDot()
        self.calculateFitnessSum()
        newDots = pg.sprite.Group()

        newDots.add(self.isMark.birth(self.minStep + 10))
        newDots.sprites()[0].isBest = True

        for i in range(V.POPSIZE):
            parent = self.parentage()

            newDots.add(parent.birth(self.minStep + 10))

        self.dots.empty()
        self.dots = newDots
        self.gen += 1

    def calculateFitnessSum(self):
        self.fitnessSum = 0
        for entity in self.dots:
            self.fitnessSum += entity.fitness

    def parentage(self):
        rand = uniform(0, self.fitnessSum)
        runningSum = 0

        for entity in self.dots:
            runningSum += entity.fitness
            if runningSum > rand:
                return entity

    def mutation(self):
        skip = True
        for entity in self.dots:
            if skip:
                skip = False
                continue
            entity.brain.mutate()

    def setBestDot(self):
        maxIndex = 0
        for entity in self.dots:
            if entity.fitness > self.max:
                self.max = entity.fitness
                maxIndex = self.dots.sprites().index(entity)

        self.bestDot = maxIndex
        self.isMark = self.dots.sprites()[maxIndex]

        if self.dots.sprites()[maxIndex].reachedGoal:
            self.minStep = self.dots.sprites()[maxIndex].brain.step
