
Width, Height = 1600  , 900 
white, black = (217, 217, 217), (12, 12, 12)
size=(Width, Height)
FLAW_STARTING_TIME = 0 #in ticks
FLAW_ENDING_TIME = 0 #in ticks
FAULTY_BOIDS = 1
FAULTY_PREDATORS = 0
PREDATOR_LIFE_SPAN = 600 #in ticks
NUM_PREY = 11
NUM_PREDATORS = 1
BOID_FIELD_OF_VIEW = 300
FPS = 360
SCALE = 40
DISTANCE = 5
SPEED = 0.0005
#BEST_PREY_WEIGHTS = {'flee': 0.7910447835152755, 'protect': 0.5760747754070812}
#BEST_PREDATOR_WEIGHTS = {'attack_furthest': 0.7538711835589235, 'attack_closest': 0.5480466354601752}
BEST_PREY_WEIGHTS = {'flee': 0.6, 'protect': 0.4}
BEST_PREDATOR_WEIGHTS = {'attack_furthest': 0.4, 'attack_closest': 0.4}