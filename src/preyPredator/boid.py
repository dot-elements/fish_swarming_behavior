import random
import pygame
from helpers.tools import *
from random import uniform
from helpers.matrix import *
from math import pi
from constants import *

class Boid:

	def __init__(self, x, y, isFlawed, DNA={"flee": random.uniform(0, 1), "protect": random.uniform(0, 1)}):
		self.position = Vector(x, y)
		vec_x = uniform(-1, 1)
		vec_y = uniform(-1, 1)
		self.velocity = Vector(vec_x, vec_y)
		self.velocity.normalize()
		self.velocity = self.velocity * uniform(1.5, 4)
		self.acceleration = Vector()
		self.color = (0, 0,255)
		self.temp = self.color
		self.secondaryColor = (70, 70, 70)
		self.max_speed = 5
		self.max_length = 1
		self.size = 2
		self.stroke = 5
		self.angle = 0
		self.hue = 0
		self.radius = 40
		self.field_of_view = BOID_FIELD_OF_VIEW
		self.isFlawed = isFlawed
		self.timeToFlaw = 0
		self.faultStrategy = random.randint(0,1)
		if self.faultStrategy != 0:
			self.faultStrategy = random.randint(1, 3)
		self.flawStartingTime = random.randint(FLAW_STARTING_TIME, FLAW_ENDING_TIME)
		self.DNA = DNA

	def limits(self, width , height):
		if self.position.x > width:
			self.position.x = 0
		elif self.position.x < 0:
			self.position.x = width

		if self.position.y > height:
			self.position.y = 0
		elif self.position.y < 0:
			self.position.y = height

	def bounceOffLimits(self, width, height):
		weight = 0.2
		offset = 10
		if self.position.x > width:
			self.velocity.x  = -self.velocity.x 
			self.position.x = self.position.x - offset
			self.goalBehaviour([Width/2, Height/2], weight)
		elif self.position.x < 0 :
			self.velocity.x = -self.velocity.x 
			self.position.x = self.position.x + offset
			self.goalBehaviour([Width/2, Height/2], weight)
		if self.position.y > height:
			self.velocity.y = -self.velocity.y 
			self.position.y = self.position.y - offset
			self.goalBehaviour([Width/2, Height/2], weight)
		elif self.position.y < 0:
			self.velocity.y = -self.velocity.y 
			self.position.y = self.position.y + offset
			self.goalBehaviour([Width/2, Height/2], weight)

	def behaviour(self, flock):
		self.acceleration.reset()
		avoid = self.separation(flock)
		avoid = avoid * 0.5
		self.acceleration.add(avoid)

		coh = self.cohesion(flock)
		coh = coh * 0.3
		self.acceleration.add(coh)

		align = self.alignment(flock)
		align = align * 0.2
		self.acceleration.add(align)

	def fleeBehaviour(self, predator):
		weight = self.DNA["flee"]
		toGoal = self.flee(predator)
		toGoal = toGoal * weight#0.6
		self.acceleration = self.acceleration - toGoal

	def goalBehaviour(self, goal, weight=0.4):
		toGoal = self.followMouse(goal)
		toGoal = toGoal * weight #0.4
		self.acceleration.add(toGoal)

	def separation(self, flockMates):
		total = 0
		steering = Vector()
		for mate in flockMates:
			dist = getDistance(self.position, mate.position)
			if dist == 0:
				dist = 1
			if mate is not self and dist < self.radius:
				temp = SubVectors(self.position,mate.position)
				temp = temp/(dist ** 2)
				steering.add(temp)
				total += 1
		if total > 0:
			steering = steering / total
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity
			steering.limit(self.max_length)
		return steering

	def alignment(self, flockMates):
		total = 0
		steering = Vector()
		for mate in flockMates:
			dist = getDistance(self.position, mate.position)
			if mate is not self and dist < self.radius:
				vel = mate.velocity.Normalize()
				steering.add(vel)
				total += 1
		if total > 0:
			steering = steering / total
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity.Normalize()
			steering.limit(self.max_length)
		return steering

	def cohesion(self, flockMates):
		total = 0
		steering = Vector()
		for mate in flockMates:
			dist = getDistance(self.position, mate.position)
			if mate is not self and dist < self.radius:
				steering.add(mate.position)
				total += 1
		if total > 0:
			steering = steering / total
			steering = steering - self.position
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity
			steering.limit(self.max_length)
		return steering

	def followMouse(self, mousePos):
		steering = Vector()
		mousePos = Vector(mousePos[0], mousePos[1])
		steering.add(mousePos)
		steering = steering - self.position
		steering.normalize()
		steering = steering * self.max_speed
		steering = steering - self.velocity
		steering.limit(self.max_length)
		return steering

	def flee(self, predator):
		steering = Vector()
		steering.add(predator.position)
		vel = predator.velocity.Normalize()
		steering = steering + vel * 2
		steering = steering - self.position
		steering.normalize()
		steering = steering * self.max_speed 
		steering = steering - self.velocity.Normalize()
		steering.limit(self.max_length)
		return steering

	def update(self):
		if self.isFlawed and self.timeToFlaw > self.flawStartingTime:
			self.secondaryColor = (255, 255, 255)
			self.selectFaultStrategy(1/10, 1/10)
		else:
			self.position = self.position + self.velocity
			self.velocity = self.velocity + self.acceleration
			self.velocity.limit(self.max_speed)
			self.angle = self.velocity.heading() + pi/2
		self.timeToFlaw += 1

	def faultyNoMovement(self):
		self.position = self.position
		self.angle = self.angle
		self.velocity = Vector(0, 0)

	def faultyBadMovement(self, Xfactor, Yfactor):
		a = Vector(self.acceleration.x * Xfactor, self.acceleration.y * Yfactor)
		v = Vector(self.velocity.x + Xfactor, self.velocity.y + Yfactor)
		self.position = self.position + self.velocity
		self.velocity = self.velocity + a
		self.velocity.limit(self.max_speed)
		self.angle = self.velocity.heading() + pi/2

	def faultySpin(self, axis):
		self.position = self.position
		self.velocity = Vector(0, 0)
		self.angle = self.angle + axis * pi/100

	def selectFaultStrategy(self,  Xfactor=0, Yfactor=0):
		if self.faultStrategy == 0:
			self.faultyNoMovement()
		elif self.faultStrategy == 1:
			self.faultyBadMovement(Xfactor, Yfactor)
		elif self.faultStrategy == 2:
			self.faultySpin(1)
		elif self.faultStrategy ==3:
			self.faultySpin(-1)	

	@staticmethod
	def getSlowest(boidList):
		if len(boidList) == 0:
			return None
		minVel = boidList[0].acceleration.magnitude()
		minBoid = boidList[0]
		for boid in boidList:
			vel = boid.acceleration.magnitude()
			if vel < minVel:
				minVel = vel
				minBoid = boid
		return minBoid

	def getClosest(self, boidList):
		minDist = 9999
		closestBoid = None
		for boid in boidList:
			distance = getDistance(self.position, boid.position)
			if distance < minDist:
				minDist = distance
				closestBoid= boid
		return closestBoid

	@staticmethod
	def getFaulty(boidList):
		res = 0
		for boid in boidList:
			if boid.isFlawed:
				res += 1
		return res

	@staticmethod
	def mutate(DNA):
		for gene in DNA:
			DNA[gene] += random.uniform(-0.1,0.1)
			DNA[gene] = max(min(DNA[gene], 1), 0)
		return DNA

	def reporduce(self, closeFaulty):
		if closeFaulty:
			mutationProb = 0.065 /FPS
		else:
			mutationProb = 0.05 /FPS
		if self.isFlawed == True and random.uniform(0, 1) < mutationProb:
			return Boid(random.randint(20, Width-20), random.randint(20, Height-20), True)
		if random.uniform(0, 1) < mutationProb:
			return Boid(random.randint(20, Width-20), random.randint(20, Height-20), False, Boid.mutate(self.DNA))
		else:
			return None

	def getCloseMates(self, boids):
		closeBoids = []
		for boid in boids:
			distance = getDistance(self.position, boid.position)
			if distance <= self.field_of_view:
				closeBoids.append(boid)
		return closeBoids

	@staticmethod
	def containsFaulty(boids):
		for boid in boids:
			if boid.isFlawed == True:
				return True
		return False

	def Draw(self, screen, distance, scale):
		ps = []
		points = [None for _ in range(3)]
		points[0] = [[0],[-self.size],[0]]
		points[1] = [[self.size//2],[self.size//2],[0]]
		points[2] = [[-self.size//2],[self.size//2],[0]]
		for point in points:
			rotated = matrix_multiplication(rotationZ(self.angle) , point)
			z = 1/(distance - rotated[2][0])

			projection_matrix = [[z, 0, 0], [0, z, 0]]
			projected_2d = matrix_multiplication(projection_matrix, rotated)

			x = int(projected_2d[0][0] * scale) + self.position.x 
			y = int(projected_2d[1][0] * scale) + self.position.y  
			ps.append((x, y))
		pygame.draw.polygon(screen, self.secondaryColor, ps)
		pygame.draw.polygon(screen, self.color, ps, self.stroke)

class Predator(Boid):

	def __init__(self, x, y, isFlawed, DNA = {"attack_furthest": random.uniform(0, 1), "attack_closest": random.uniform(0, 1)}):
		super().__init__(x, y, isFlawed, DNA)
		self.max_speed = 6
		self.color = (255, 0, 0)
		self.lifeSpan = PREDATOR_LIFE_SPAN
		self.lifeSpanReset = PREDATOR_LIFE_SPAN
		self.killable = True

	def attack(self, prey):
		steering = Vector()
		steering.add(prey.position)
		vel = prey.velocity.Normalize()
		steering = steering + vel * 2
		steering = steering - self.position
		steering.normalize()
		steering = steering * self.max_speed 
		steering = steering - self.velocity.Normalize()
		steering.limit(self.max_length)
		return steering

	def attackPrey(self, prey):
		weight = self.DNA["attack_closest"]
		toGoal = self.attack(prey)
		toGoal = toGoal * weight 
		self.acceleration.add(toGoal)

	def attackBehaviour(self, close_prey):
		weight=self.DNA["attack_furthest"]
		if len(close_prey) == 0:
			return
		center = Vector(0, 0)
		for prey in close_prey:
			center = center + prey.position
		center.x /= len(close_prey)
		center.y /= len(close_prey)
		target_ids = []
		for target in close_prey:
			dist = getDistance(center, target.position)
			target_ids.append((target, dist))	
		target_ids.sort(key=lambda elem: elem[1]) 
		toGoal = self.attack(target_ids[0][0])
		toGoal = toGoal * weight  
		self.acceleration.add(toGoal)

	def eatPrey(self, prey_list, deadList=None):
		for prey in prey_list:
			dist = getDistance(self.position, prey.position)
			if dist < self.radius/2:
				prey_list.remove(prey)
				if deadList is not None:
					deadList.append(prey.DNA)
					deadList = deadList[-5:]
				self.lifeSpan = self.lifeSpanReset

	def updateHunger(self, list, deadList=None):
		if self.killable:
			self.lifeSpan -= 1
			if self.lifeSpan <= 0:
				list.remove(self)
				if deadList is not None:
					deadList.append(self.DNA)
					deadList = deadList[-5:]
					
	def reporduce(self):
		mutationProb = 0.05 /FPS
		if self.isFlawed == True and random.uniform(0, 1) < mutationProb:
			return Predator(random.randint(20, Width-20), random.randint(20, Height-20), True)
		if random.uniform(0, 1) < mutationProb:
			return Predator(random.randint(20, Width-20), random.randint(20, Height-20), False, Predator.mutate(self.DNA))
		else:
			return None
