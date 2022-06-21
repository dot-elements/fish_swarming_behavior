import ast
import os
import sys
import pygame
from boid import Boid, Predator
from helpers.tools import *
import random
from helpers.matrix import *
from constants import *
import argparse
import sys
def main(args):
	parser = argparse.ArgumentParser(description="Do something.")
	parser.add_argument("-b", "--FAULTY_BOIDS", type=float, default= 0, required=False)
	parser.add_argument("-p", "--FAULTY_PREDATORS", type=float, default= 0, required=False)
	args = parser.parse_args(args)
	FAULTY_BOIDS2 = args.FAULTY_BOIDS
	FAULTY_PREDATORS2 = args.FAULTY_PREDATORS
	pygame.init()
	window = pygame.display.set_mode(size, pygame.DOUBLEBUF ) # pygame.DOUBLEBUF   pygame.FULLSCREEN
	clock = pygame.time.Clock()

	flock = []
	flockPredators = []
	deadPrey = []
	deadPredators = []
	genesPred = []
	genesPrey = []
	n = NUM_PREY
	pn = NUM_PREDATORS 
	faulty = FAULTY_BOIDS2
	with open(sys.path[0] + ' /../../results/genesPred.txt') as f:
		genesDataPred = f.read()
		
	with open(sys.path[0] + ' /../../results/genesPrey.txt') as f:
		genesDataPrey = f.read()
	genesPredIsEmpty = os.stat(sys.path[0] + ' /../../results/genesPred.txt').st_size == 0
	genesPreyIsEmpty = os.stat(sys.path[0] + ' /../../results/genesPrey.txt').st_size == 0
	if not genesPredIsEmpty:
		genesPred = ast.literal_eval(genesDataPred)
	if not genesPreyIsEmpty:
		genesPrey = ast.literal_eval(genesDataPrey)
	j = 0
	for i in range(n):
		if faulty > 0:
			flock.append(Boid(random.randint(20, Width-20), random.randint(20, Height-20), True))
		else:
			flock.append(Boid(random.randint(20, Width-20), random.randint(20, Height-20), False))
		if not genesPreyIsEmpty:
			flock[i].DNA = genesPrey[j]
			j += 1
			j %= len(genesPrey)
		faulty -= 1

	faulty = FAULTY_PREDATORS2
	j = 0
	for i in range(pn):
		if faulty > 0:
			flockPredators.append(Predator(random.randint(20, Width-20), random.randint(20, Height-20), True))
		else:
			flockPredators.append(Predator(random.randint(20, Width-20), random.randint(20, Height-20), False))
		if not genesPredIsEmpty:
			flockPredators[i].DNA = genesPred[j]
			j += 1
			j %= len(genesPred)
		faulty -= 1

	run = True
	while run:
		clock.tick(FPS)
		window.fill((10, 10, 15))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False


		if len(flock) <= (NUM_PREY * 5) // 100:
			topPred = [pred.DNA for pred in flockPredators[-5:]]
			os.remove(sys.path[0] + " /../../results/genesPred.txt")
			f1 = open(sys.path[0] + " /../../results/genesPred.txt", "w")
			f1.write(str(topPred))
			f1.close()
			os.remove(sys.path[0] + " /../../results/genesPrey.txt")
			f2 = open(sys.path[0] + " /../../results/genesPrey.txt", "w")
			f2.write(str(deadPrey[-5:]))
			f2.close()
			sys.exit()
		if len(flockPredators) <= (NUM_PREDATORS * 5) // 100 or len(flockPredators) <= 1:
			topPrey = [prey.DNA for prey in flock[-5:]]
			os.remove(sys.path[0] + " /../../results/genesPrey.txt") 
			f1 = open(sys.path[0] + " /../../results/genesPrey.txt", "w")
			f1.write(str(topPrey))
			f1.close()
			os.remove(sys.path[0] + " /../../results/genesPred.txt")
			f2 = open(sys.path[0] + " /../../results/genesPred.txt", "w")
			f2.write(str(deadPredators[-5:]))
			f2.close()
			sys.exit()


		goal = [Width/2, Height/2]
		for boid in reversed(flock):
			boid.radius = SCALE
			boid.bounceOffLimits(Width, Height)
			boid.behaviour(flock)
			minDist = 9999
			closestFaulty = None
			for faultyBoid in flock:
				if faultyBoid == boid:
					continue
				if faultyBoid.secondaryColor == (255, 255, 255):
					distance = getDistance(boid.position, faultyBoid.position)
					if distance < boid.field_of_view:
						if faultyBoid.faultStrategy == 1:
							if distance < minDist:
								minDist = distance
								closestFaulty = faultyBoid
			if closestFaulty is not None:
				boid.goalBehaviour([closestFaulty.position.x, closestFaulty.position.y] , boid.DNA["protect"])
			boid.goalBehaviour(goal, 0.2)

			for predator in flockPredators:
				distance = getDistance(boid.position, predator.position)
				if distance < boid.field_of_view  :
					boid.fleeBehaviour(predator)
			boid.update()
			offsprig = boid.reporduce(Boid.containsFaulty(boid.getCloseMates(flock)))
			if offsprig != None:
				flock.append(offsprig)
			boid.hue += SPEED
			boid.Draw(window, DISTANCE, SCALE)
		goal = [Width/2, Height/2] 
		ticks = 0
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
			offsprig = boid.reporduce()
			if offsprig != None:
				flockPredators.append(offsprig)
			boid.updateHunger(flockPredators, deadPredators)
			boid.eatPrey(flock, deadPrey)
			boid.hue += SPEED
			boid.Draw(window, DISTANCE, SCALE)	
		ticks+=1
		pygame.display.flip()
	pygame.quit()

if __name__ == "__main__":
	main(sys.argv[1:])