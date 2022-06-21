import os

RUNS_NO = 5
path = os.getcwd()
prentDir = os.path.abspath(os.path.join(path, os.pardir))
command ='python '+ prentDir + '\\rocketTarget\\rocketTarget.py'
for x in range(RUNS_NO):
    print("run no: ", x + 1 )
    for i in range(1, 10):
        for j in range(1, 10):
            FLEE_WEIGHT = i * 0.1
            PROTECT_WEIGHT = j * 0.1
            print(FLEE_WEIGHT, " FLEE_WEIGHT")
            print(PROTECT_WEIGHT, " PROTECT_WEIGHT")
            os.system(command + ' -b ' + f'{FLEE_WEIGHT}' + ' -p ' + f'{PROTECT_WEIGHT}')
