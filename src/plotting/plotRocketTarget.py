import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

x = np.random.rand(20)
y = np.random.rand(20)
z = x*y
f = open('resultsRocketTarget.txt', 'r')
contents = f.readlines()
f.close()
results = []

for content in contents:
    arr = np.array(content[1:-2].split(', '), dtype=float)
    results.append(arr)
results = np.array(results)
x = results[:, 0]
y = results[:, 1]
s = results[:, 2]


scores = np.zeros((9,9))
cnt = np.zeros((9,9))

for r in results:
    scores[  int(r[1] * 10) - 1, int(r[0] * 10) - 1] += r[2]  
    cnt[ int(r[1] * 10) - 1, int(r[0] * 10) - 1] += 1

x_axis = [.1, .2, .3, .4, .5, .6 , .7, .8, .9]
ax = sns.heatmap(scores/cnt, xticklabels=x_axis, yticklabels=x_axis, cmap='RdYlGn', linewidth=0.5)
ax.set(xlabel='Flee weight', ylabel='Protection Weight')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
ax.set_yticklabels(ax.get_yticklabels(), rotation=45, horizontalalignment='right')
ax.invert_yaxis()

plt.show()
