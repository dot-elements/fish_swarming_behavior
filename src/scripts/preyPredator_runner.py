import os
RUNS_NO = 5
path = os.getcwd()
prentDir = os.path.abspath(os.path.join(path, os.pardir))
command ='python '+ prentDir + '\\preyPredator\\preyPredator.py'

for x in range(RUNS_NO):
    print("run no: ", x + 1 )
    for i in range(7 + 1):
        for j in range(7 + 1):
            FAULTY_BOIDS = i * 10
            FAULTY_PREDATORS = j
            print(i * 10, " faulty boids")
            print(j, " faulty predators")
            os.system(command + ' -b ' + f'{FAULTY_BOIDS}' + ' -p ' + f'{FAULTY_PREDATORS}')
