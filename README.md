# Fish Swarming Behaviour
This is part of the TU Delft [Research Project](https://github.com/TU-Delft-CSE/Research-Project). It serves as a way to recreate the
results described in the paper [Protection algorithms using fault resilient fish swarming behaviour](http://resolver.tudelft.nl/uuid:f751b734-6fa9-4ca1-ab5e-940f5682c90f).
## Libraries
 > pygame : pip install pygame
 
 > colorsys : pip install colorsys

---
## Prey Predator 
To run this instance:
- With custom weights:
 > python preyPredator/preyPredator.py -b {FAULTY_BOIDS} -p {FAULTY_PREDATORS}

- With the default weights:
> python preyPredator/preyPredator.py 

To use the genetic algorithm for weight training:
> python script/training_script.py 

---
## Missile Target 
- With custom weights:
 > python preyPredator/missileTarget.py -b {FLEE_WEIGHT} -p {PROTECT_WEIGHT}

- With the default weights:
> python preyPredator/missileTarget.py 
---
## Results
To generate the graphs for each instance:
- Run the runner script for that instance:
 > python scrips/preyPredator_runner.py

 > python scrips/rocketTarget_runner.py
 - Run the plotting script for that instance:
 > python plotting/plotPreyPredator.py

 > python plotting/plotRocketTarget.py
 - The results are firstly generated in the results folder and then plotted
---

## Other remarks
 - All weights and constants can be modified in the constants file of each instance
 - Training instances can also be run individually using:
 > python preyPredator/geneticsTraining.py 

