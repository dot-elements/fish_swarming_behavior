import sys
from helpers.tools import *
import pygame
from boid import Boid, Predator
import random
from helpers.matrix import *
from constants import *
import argparse
import sys

def timeScore(time):
	return (50 * FPS - time) / (45 * FPS)
def faultScore(faultyRemaining, faultyTotal):
	if faultyTotal == 0:
		return 0
	else:
		return faultyRemaining / faultyTotal

def aliveScore(remainingBoids, totalBoids):
	return remainingBoids / totalBoids

def scoringFunction(timeScore, faultScore, aliveScore, type):
	if type == "prey":
		return max(min((0.5 * timeScore + 0.5 * aliveScore + faultScore), 1), 0)
	return max(min((0.5 * timeScore + 0.5 * aliveScore +  faultScore), 1), 0)

def generatePrey(n, faulty):
	flock = []
	for _ in range(n):
		if faulty > 0:
			flock.append(Boid(random.randint(20, Width-20), random.randint(20, Height-20), True, BEST_PREY_WEIGHTS))
		else:
			flock.append(Boid(random.randint(20, Width-20), random.randint(20, Height-20), False, BEST_PREY_WEIGHTS))
		faulty -= 1
	return flock

def generatePredators(pn, faulty):
	flockPredators = []
	for _ in range(pn):
		if faulty > 0:
			flockPredators.append(Predator(random.randint(20, Width-20), random.randint(20, Height-20), True, BEST_PREDATOR_WEIGHTS))
		else:
			flockPredators.append(Predator(random.randint(20, Width-20), random.randint(20, Height-20), False, BEST_PREDATOR_WEIGHTS))
		faulty -= 1
	return flockPredators

def main(args):
	parser = argparse.ArgumentParser(description="Get faulty data")
	parser.add_argument("-b", "--FAULTY_BOIDS", type=float, default= FAULTY_BOIDS, required=False)
	parser.add_argument("-p", "--FAULTY_PREDATORS", type=float, default= FAULTY_PREDATORS, required=False)
	args = parser.parse_args(args)
	FAULTY_BOIDS2 = args.FAULTY_BOIDS
	FAULTY_PREDATORS2 = args.FAULTY_PREDATORS
	pygame.init()
	window = pygame.display.set_mode(size, pygame.DOUBLEBUF ) # pygame.DOUBLEBUF   pygame.FULLSCREEN
	clock = pygame.time.Clock()
	flock = generatePrey(NUM_PREY, FAULTY_BOIDS2)
	flockPredators = generatePredators(NUM_PREDATORS, FAULTY_PREDATORS2)
	run = True
	while run:
		ticks = 0
		clock.tick(FPS)
		window.fill((10, 10, 15))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False
		if len(flock) <= (NUM_PREY * 5) // 100:
			f = open("results.txt", "a+")
			finishTime = (pygame.time.get_ticks()/10**3) * FPS # in miliseconds
			faultyBoids= Predator.getFaulty(flockPredators)
			score = scoringFunction(timeScore(finishTime), faultScore(faultyBoids, FAULTY_PREDATORS2), aliveScore(len(flockPredators), NUM_PREDATORS), "predator")
			print("Predators win in:", finishTime, "with score: ", score )
			data = [0, score, FAULTY_BOIDS2, FAULTY_PREDATORS2]
			with open(sys.path[0] + " /../../results/resultsPreyPredator.txt", "a+") as f:
				f.write(str(data))
				f.write('\n')
			f.close()
			sys.exit()
		if len(flockPredators) <= (NUM_PREDATORS * 10) // 100 or len(flockPredators) <= 1:
			finishTime = (pygame.time.get_ticks()/10**3) * FPS
			faultyBoids= Boid.getFaulty(flock)
			score = scoringFunction(timeScore(finishTime), faultScore(faultyBoids, FAULTY_BOIDS2), aliveScore(len(flock), NUM_PREY), "prey")
			print("Prey wins in:", finishTime, "with score: ", score)
			data = [1, score, FAULTY_BOIDS2, FAULTY_PREDATORS2]
			with open(sys.path[0] + " /../../results/resultsPreyPredator.txt", "a+") as f:
				f.write(str(data))
				f.write('\n')
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
					if distance < boid.field_of_view  :
						if faultyBoid.faultStrategy == 1:
							if distance < minDist:
								minDist = distance
								closestFaulty = faultyBoid
			if closestFaulty is not None:
				boid.goalBehaviour([closestFaulty.position.x, closestFaulty.position.y] ,  boid.DNA["protect"])
			boid.goalBehaviour(goal, 0.2)

			for predator in flockPredators:
				distance = getDistance(boid.position, predator.position)
				if distance < boid.field_of_view  :
					boid.fleeBehaviour(predator)
			boid.update()
			boid.hue += SPEED
			boid.Draw(window, DISTANCE, SCALE)
		goal = [Width/2, Height/2] 

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