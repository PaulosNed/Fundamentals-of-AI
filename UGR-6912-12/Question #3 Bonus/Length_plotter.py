
from matplotlib import pyplot as plt

plt.title("Graph Comparision Based On Length", fontsize=25)

plt.plot([40, 60, 80, 100],[370.9365384615385, 375.164406779661, 396.69208860759494, 416.6377777777778],color='blue',marker='.',markersize=8)
plt.plot([40, 60, 80, 100],[782.4461538461538, 1023.6087570621469, 1535.525, 1508.7615151515151],color='black',marker='.',markersize=8)
plt.plot([40, 60, 80, 100],[350.04358974358973, 343.2361581920904, 360.0164556962025, 381.5349494949495],color='green',marker='.',markersize=8)
plt.plot([40, 60, 80, 100],[353.4076923076923, 346.8098870056497, 364.1373417721519, 385.30242424242425],color='red',marker='.',markersize=8)
plt.legend(['BREADTH_FIRST','DEPTH_FIRST','DIJKSTRA', 'ASTAR'], loc='upper left')
plt.show()

