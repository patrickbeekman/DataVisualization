import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos

def main():
    upper_left = (-1, 1)
    upper_right = (1, 1)
    lower_left = (-1, -1)
    lower_right = (1, -1)
    corners = np.array([upper_left, upper_right, lower_right, lower_left])

    plt.plot(list(corners[:,0]) + list(corners[:1,0]), list(corners[:,1]) + list(corners[:1,1]), 'k')
    plt.scatter(corners[:,0], corners[:,1], c=[1,2,3,4])
    plt.show()

def rot(a):
    # based on https://en.wikipedia.org/wiki/Rotation_matrix
    c = cos(a*np.pi/180)
    s = sin(a*np.pi/180)
    return np.array([
        [c, -s],
        [s, c]
    ])

if __name__ == "__main__":
    main()