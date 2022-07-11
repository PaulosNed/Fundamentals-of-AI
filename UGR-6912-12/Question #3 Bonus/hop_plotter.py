from matplotlib import pyplot as plt

plt.title("Graph Comparision Based On number of hops", fontsize=25)

plt.plot([40, 60, 80, 100],[4.2525641025641026, 4.307344632768362, 4.382594936708861, 4.60929292929293],color='blue',marker='.',markersize=8)
plt.plot([40, 60, 80, 100],[7.806410256410256, 10.537853107344633, 14.504905063291138, 14.355151515151515],color='black',marker='.',markersize=8)
plt.plot([40, 60, 80, 100],[4.401282051282052, 4.535028248587571, 4.635759493670886, 4.85010101010101],color='green',marker='.',markersize=8)
plt.plot([40, 60, 80, 100],[4.420512820512821, 4.544632768361582, 4.651424050632912,  4.860202020202021],color='red',marker='.',markersize=8)
plt.legend(['BREADTH_FIRST','DEPTH_FIRST','DIJKSTRA', 'ASTAR'], loc='upper left')
plt.show()