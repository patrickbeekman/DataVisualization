import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

threshold = 40


def main():
    mri_path = os.path.dirname(__file__) + "/mri/14.pgm"
    with open(mri_path, 'rb') as file:
        file_format = str(file.readline().strip()).replace('b', '').replace('\'', '')
        width = int(str(file.read(3))[2:5])
        file.read(1)
        height = int(str(file.read(3))[2:5])
        file.read(1)
        max = int(str(file.read(2))[2:4])
        file.read(1)
        #image = np.fromfile(file, dtype=np.uint16).reshape((height, width))

        image = np.zeros((width, height))
        for i in range(0, width):
            whole_line = str(file.readline())[2:-4].split(" ")
            for j in range(0, width):
                image[i][j] = int(whole_line[j])

    thresholded = np.copy(image)

    thresholded[thresholded < threshold] = 0
    thresholded[thresholded >= threshold] = 1

    j, i = np.meshgrid(range(height), range(width))
    i = i.reshape((-1,))
    j = j.reshape((-1,))
    c = image.reshape((-1,))
    plt.scatter(j, i, c=c, cmap='gray')

    for n in range(width-1):
        for m in range(height-1):
            bit_pattern(thresholded[i,j], thresholded[i+1,j], thresholded[i+1, j-1], thresholded[i, j-1])
            # create bit pattern
            # pass into lookup with n and m
            print(n,",",m)
    plt.show()


def bit_pattern(first, second, third, fourth):
    bits = 0b0
    bits = (bits << 1) | first
    bits = (bits << 1) | second
    bits = (bits << 1) | third
    bits = (bits << 1) | fourth
    return int(bits)


def lookup(val, i, j):
    if val == 0:
        print("lookup:", 0)
    elif val == 1:
        print("lookup:", 1)
    elif val == 2:
        print("lookup:", 1)
    elif val == 3:
        print("lookup:", 1)
    elif val == 4:
        print("lookup:", 1)
    elif val == 5:
        print("lookup:", 1)
    elif val == 6:
        print("lookup:", 1)
    elif val == 7:
        print("lookup:", 1)
    elif val == 8:
        print("lookup:", 1)
    elif val == 9:
        print("lookup:", 1)
    elif val == 10:
        print("lookup:", 1)
    elif val == 11:
        print("lookup:", 1)
    elif val == 12:
        print("lookup:", 1)
    elif val == 13:
        print("lookup:", 1)
    elif val == 14:
        print("lookup:", 1)
    elif val == 15:
        print("lookup:", 1)


if __name__ == "__main__":
    main()