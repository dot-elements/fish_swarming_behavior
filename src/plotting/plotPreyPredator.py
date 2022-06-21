import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

x = np.random.rand(20)
y = np.random.rand(20)
z = x*y
f = open('results.txt', 'r')
contents = f.readlines()
f.close()
results = []

for content in contents:
    arr = np.array(content[1:-2].split(', '), dtype=float)
    results.append(arr)
results = np.array(results)
x = results[:, 2]
y = results[:, 3]
z = ['r' if x == 0 else 'b' for x in results[:, 0]]
s = results[:,1]

scores = np.zeros((8,8))
cnt = np.zeros((8,8))

for r in results:
    if r[0] == 1:
        scores[ int(r[3]), int(r[2]/10)] += r[1]  
    else:
        scores[ int(r[3]), int(r[2]/10)] -= r[1]  
    cnt[ int(r[3]), int(r[2]/10)] += 1
print(scores/cnt)
for i in range(8):
    for j in range(8):
        scores[i][j] /= cnt[i][j] 
x_axis = [0, 10, 20, 30, 40, 50, 60 ,70]
y_axis = [0 , 1, 2, 3, 4, 5, 6 ,7]
ax = sns.heatmap(scores, xticklabels=x_axis, yticklabels=y_axis, cmap='RdYlGn', linewidth=0.5, vmin=-1, vmax=1)
ax.set(xlabel='Faulty prey', ylabel='Faulty predators')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
ax.set_yticklabels(ax.get_yticklabels(), rotation=45, horizontalalignment='right')
ax.invert_yaxis()
colorbar = ax.collections[0].colorbar
colorbar.set_ticks([-1, -0.5, 0, 0.5, 1])
colorbar.set_ticklabels(['Pred Win', 'Pred Favoured', 'Balanced', 'Prey Favoured', 'Prey Win'])
y_axis.append(8)
plt.plot( y_axis, y_axis, color='b')
plt.show()
