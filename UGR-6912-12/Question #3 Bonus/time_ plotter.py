from matplotlib import pyplot as plt

plt.title("Graph Comparision Based On Time", fontsize=25)

plt.plot([40, 60, 80, 100],[0.02468801216402939, 0.027793898375600964, 0.03784762646526222, 0.04984060615757386],color='blue',marker='.',markersize=8)
plt.plot([40, 60, 80, 100],[0.01940666655009875, 0.028223615918455826, 0.04336167731028731, 0.0606215050187658],color='black',marker='.',markersize=8)
plt.plot([40, 60, 80, 100],[0.057597948827419594, 0.08228265548090051, 0.1216512816553623, 0.1554650101634895],color='green',marker='.',markersize=8)
plt.plot([40, 60, 80, 100],[0.04010474294773303, 0.0599682483880315, 0.08746064876377894, 0.11626761623027951],color='red',marker='.',markersize=8)
plt.legend(['BREADTH_FIRST','DEPTH_FIRST','DIJKSTRA', 'ASTAR'], loc='upper left')
plt.show()