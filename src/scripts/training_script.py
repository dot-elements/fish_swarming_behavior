import argparse
import os
import sys

RUNS_NO = 10
path = os.getcwd()
prentDir = os.path.abspath(os.path.join(path, os.pardir))
command ='python '+ prentDir + '\\preyPredator\\geneticsTraining.py'

for i in range(RUNS_NO):
    print("run no: ", i + 1)
    os.system(command + ' -b ' + f'{10}' + ' -p ' + f'{0}')
