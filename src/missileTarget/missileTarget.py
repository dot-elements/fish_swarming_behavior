import sys
import numpy as np
import pygame
from boid import Boid, Predator
import math
import random
from helpers.matrix import *
from helpers.tools import *
from constants import *
import sys
import argparse
import sys

def createBounds(radius):
	imaginaryBounds = []
	for i in range(450 - radius, 450 + radius):
		x1 = 1500 - math.sqrt(abs(radius**2 - (i - 450)**2))
		x1 = int(x1) 
		x2 = 1500 + math.sqrt(abs(radius**2 - (i - 450)**2))
		x2 = int(x2) 
		imaginaryBounds.append([x1, i])
		imaginaryBounds.append([x2, i])
	for i in range(0 , 450 - radius):
		imaginaryBounds.append([(i + 1100), i])
	for i in range(499 , 901):
		imaginaryBounds.append([(2000 - i), i])
	for i in range(901):
		imaginaryBounds.append([550, i])
	return imaginaryBounds

def generatePrey(n, faulty, TRIAL_WEIGHTS):
	flock = []
	for _ in range(n):
		if faulty > 0:
			flock.append(Boid(1500, 450, True, TRIAL_WEIGHTS))
		else:
			flock.append(Boid(random.randint(800, 1300-20), random.randint(200, 600), False, TRIAL_WEIGHTS))
		faulty -= 1
	return flock

def generatePredators(pn, faulty):
	flockPredators = []
	for _ in range(pn):
		if faulty > 0:
			
			flockPredators.append(Predator(random.randint(20, Width-20), random.randint(20, Height-20), True, BEST_PREDATOR_WEIGHTS))
		else:
			flockPredators.append(Predator(random.randint(20, 100), random.randint(20, Height-20), False, BEST_PREDATOR_WEIGHTS))
		faulty -= 1
	return flockPredators

def main(args):
	parser = argparse.ArgumentParser(description="Get weights")
	parser.add_argument("-b", "--DNA_PREY_FLEE", type=float, default= BEST_PREY_WEIGHTS["flee"], required=False)
	parser.add_argument("-p", "--DNA_PREY_PROTECT", type=float, default= BEST_PREY_WEIGHTS["protect"], required=False)
	args = parser.parse_args(args)
	DNA_PREY_FLEE = args.DNA_PREY_FLEE
	DNA_PREY_PROTECT = args.DNA_PREY_PROTECT
	pygame.init()
	window = pygame.display.set_mode(size, pygame.DOUBLEBUF ) # pygame.DOUBLEBUF   pygame.FULLSCREEN
	clock = pygame.time.Clock()

	TRIAL_WEIGHTS = {'flee': DNA_PREY_FLEE, 'protect': DNA_PREY_PROTECT}
	flock = generatePrey(NUM_PREY, FAULTY_BOIDS, TRIAL_WEIGHTS)
	flockPredators = generatePredators(NUM_PREDATORS, FAULTY_PREDATORS)

	run = True
	imaginaryBounds = createBounds(50)
	while run:
		ticks = 0
		clock.tick(FPS)
		window.fill((10, 10, 15))

		for bound in imaginaryBounds:
			pygame.draw.line(window, (70, 255, 0), bound, bound)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False

		if len(flock) <= 0 or flock[0].isFlawed == False:
			finishTime = (pygame.time.get_ticks()/10**3) * FPS # in miliseconds
			print("Attack wins in:", finishTime, )
			data = [DNA_PREY_FLEE, DNA_PREY_PROTECT, finishTime]
			with open(sys.path[0] + " /../../results/resultsMissileTarget.txt", "a+") as f:
				f.write(str(data))
				f.write('\n')
			f.close()
			sys.exit()
		if len(flockPredators) < 1:
			finishTime = (pygame.time.get_ticks()/10**3) * FPS
			print("Defense wins in:", finishTime,)
			data = [DNA_PREY_FLEE, DNA_PREY_PROTECT, finishTime]
			with open(sys.path[0] + "/../../results/resultsMissileTarget.txt", "a+") as f:
				f.write(str(data))
				f.write('\n')
			sys.exit()

		goal = [1300, 450] 
		for boid in reversed(flock):
			boid.radius = SCALE
			boid.bounceOffLimits(Width, Height)
			boid.behaviour(flock)
			for predator in flockPredators:
				distance = getDistance(boid.position, predator.position)
				if distance < boid.field_of_view  :
					boid.fleeBehaviour(predator)
			boid.avoidObstacles(imaginaryBounds)
			boid.goalBehaviour(goal, boid.DNA["protect"])
			boid.update()
			boid.hue += SPEED
			boid.Draw(window, DISTANCE, SCALE)

		for boid in reversed(flockPredators):
			boid.radius = SCALE
			boid.bounceOffLimits(Width, Height)
			boid.behaviour(flockPredators)
			close_prey = []
			for prey in flock:
				dist = getDistance(boid.position, prey.position) 
				if dist < boid.field_of_view:
					close_prey.append(prey)
			closePrey = boid.getClosest(close_prey)
			if closePrey is not None:
				boid.attackPrey(closePrey) 
			boid.attackBehaviour(close_prey)
			boid.goalBehaviour(goal, 0.2)
			boid.update()
			boid.updateHunger(flockPredators)
			boid.eatPrey(flock)
			boid.hue += SPEED
			boid.Draw(window, DISTANCE, SCALE)	
		ticks+=1
		pygame.display.flip()
	pygame.quit()
	
if __name__ == "__main__":
	main(sys.argv[1:])

