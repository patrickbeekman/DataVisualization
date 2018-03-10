import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def read_pgm(filename):
    f = open(filename, 'rb')
    type = f.readline()
    type = str(type.strip()).replace("b", "").replace("'", "")
    print(type.strip())
    size = f.readline()
    size = str(size.strip()).replace("b", "").replace("'", "")
    size = size.split(" ")
    x = int(size[0])
    y = int(size[0])
    print("X: " + str(x) + " Y: " + str(y))
    white = f.readline()
    white = white.strip()
    white = int(white)
    print(white)

    matrix = np.zeros((x, y))
    for i in range(0, x):
        line = f.readline()
        line = str(line.strip()).replace("b", "").replace("'", "")
        line = line.split(" ")
        for j in range(0, y):
            matrix[i][j] = int(line[j])
    return white, matrix

    size = f.readline()
    size = str(size.strip()).replace("b", "").replace("'", "")
    size = size.split(" ")
    x = int(size[0])
    y = int(size[0])
    print("X: " + str(x) + " Y: " + str(y))
    white = f.readline()
    white = white.strip()
    white = int(white)
    print(white)

    matrix = np.zeros((x, y))
    for i in range(0, x):
        line = f.readline()
        line = str(line.strip()).replace("b", "").replace("'", "")
        line = line.split(" ")
        for j in range(0, y):
            matrix[i][j] = int(line[j])
    return matrix


def main():
    # white, matrix = read_pgm()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    z = 0
    for mri_num in range(1,16):
        name = os.path.dirname(__file__) + "/../hw5/mri/" + str(mri_num).zfill(2) + ".pgm"
        print(name)
        matrix = read_pgm(name)
        num_rows, num_cols = matrix.shape
        matrix = matrix / matrix.max()
        j, i = np.meshgrid(range(num_cols), range(num_rows))
        i = i.reshape((-1,))
        j = j.reshape((-1,))
        c = matrix.reshape((-1,))
        ax.scatter(j, i, z, c=c)
        z+=4

    '''
    # np.save('slice14.npy', matrix)
    matrix = np.load('slice14.npy')

    # print(white)
    print(matrix)
    num_rows, num_cols = matrix.shape
    matrix = matrix / matrix.max()
    print(num_rows, num_cols)

    j, i = np.meshgrid(range(num_cols), range(num_rows))
    i = i.reshape((-1,))
    j = j.reshape((-1,))
    c = matrix.reshape((-1,))
    plt.scatter(j, i, c=c, cmap='gray')
    '''
    plt.show()


main()

