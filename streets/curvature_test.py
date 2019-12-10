import matplotlib.pyplot as plt
import numpy

from curvature import curvature

points = numpy.array(
    [
        [0.0, 0.0],
        [0.3, 0.0],
        [1.25, -0.1],
        [2.1, -0.9],
        [2.85, -2.3],
        [3.8, -3.95],
        [5.0, -5.75],
        [6.4, -7.8],
        [8.05, -9.9],
        [9.9, -11.6],
        [12.05, -12.85],
        [14.25, -13.7],
        [16.5, -13.8],
        [19.25, -13.35],
        [21.3, -12.2],
        [22.8, -10.5],
        [23.55, -8.15],
        [22.95, -6.1],
        [21.35, -3.95],
        [19.1, -1.9],
    ]
)

print(len(points))
print(points)

curvature_results = curvature(points)

print(len(curvature_results))
print(curvature_results)

plt.scatter(points[:, 0], points[:, 1])
plt.show()

plt.scatter(points[:, 0], curvature_results)
plt.show()
