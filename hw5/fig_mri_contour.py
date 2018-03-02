import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.interpolate import griddata
import pandas as pd

threshold = 40
lines = []
fig = plt.figure()
ax = fig.add_subplot(111)


def main():
    global threshold
    #mri_path = os.path.dirname(__file__) + "/mri/14.pgm"
    mri_path = sys.argv[1]
    threshold = int(sys.argv[2])
    with open(mri_path, 'rb') as file:
        file_format = str(file.readline().strip()).replace('b', '').replace('\'', '')
        width = int(str(file.read(3))[2:5])
        file.read(1)
        height = int(str(file.read(3))[2:5])
        file.read(1)
        max = int(str(file.read(2))[2:4])
        file.read(1)

        global image
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
    #ax.scatter(j, i, c=c, cmap='gray')
    main_image = ax.imshow(image, cmap='gray')

    for n in range(width-1):
        for m in range(height-1):
            bit = bit_pattern(thresholded[n,m-1], thresholded[n+1,m-1], thresholded[n+1, m], thresholded[n, m])
            lookup(bit, m, n)

    plt.title(mri_path[-11:] + " , threshold = " + str(threshold))
    plt.colorbar(main_image)
    #plt.show()
    plt.savefig(sys.argv[3])


# bottom left is start, top left is end
def bit_pattern(first, second, third, fourth):
    bits = 0b0
    bits = (bits << 1) | int(first)
    bits = (bits << 1) | int(second)
    bits = (bits << 1) | int(third)
    bits = (bits << 1) | int(fourth)
    return int(bits)


def lookup(val, i, j):
    if val == 1:
        # curr = Line2D([i, i+.5], [j-.5, j-1], color='b')
        curr = Line2D([i-.5, i -1], [j, j +.5], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 2:
        # curr = Line2D([i+.5, i+1], [j-1, j-.5], color='b')
        curr = Line2D([i-1, i - .5], [j + .5, j + 1], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 3:
        #curr = Line2D([i, i+1], [j-.5, j-.5], color='b')
        curr = Line2D([i-.5, i -.5], [j, j +1], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 4:
        # curr = Line2D([i+.5, i+1], [j, j-.5], color='b')
        curr = Line2D([i, i - .5], [j + .5, j + 1], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 5:
        # curr = Line2D([i, i+.5], [j-.5, j], color='b')
        curr = Line2D([i-.5, i], [j, j +.5], color='b')
        # curr2 = Line2D([i+.5, i+1], [j-1, j-.5], color='b')
        curr2 = Line2D([i-1, i - .5], [j + .5, j + 1], color='b')
        lines.append(curr)
        lines.append(curr2)
        ax.add_line(curr)
        ax.add_line(curr2)
    elif val == 6:
        # curr = Line2D([i+.5, i+.5], [j, j-1], color='b')
        curr = Line2D([i, i -1], [j + .5, j +.5], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 7:
        # curr = Line2D([i, i+.5], [j-.5, j], color='b')
        curr = Line2D([i-.5, i], [j, j+.5], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 8:
        # curr = Line2D([i, i+.5], [j-.5, j], color='b')
        curr = Line2D([i-.5, i], [j, j +.5], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 9:
        # curr = Line2D([i+.5, i+.5], [j, j-1], color='b')
        curr = Line2D([i, i-1], [j+.5, j+.5], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 10:
        # curr = Line2D([i, i+.5], [j-.5, j-1], color='b')
        curr = Line2D([i-.5, i -1], [j, j+.5], color='b')
        # curr2 = Line2D([i+.5, i+1], [j, j-.5], color='b')
        curr2 = Line2D([i, i - .5], [j + .5, j + 1], color='b')
        lines.append(curr)
        lines.append(curr2)
        ax.add_line(curr)
        ax.add_line(curr2)
    elif val == 11:
        # curr = Line2D([i+.5, i+1], [j, j-.5], color='b')
        curr = Line2D([i, i - .5], [j + .5, j + 1], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 12:
        #curr = Line2D([i, i+1], [j-.5, j-.5], color='b')
        curr = Line2D([i - .5, i - .5], [j, j + 1], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 13:
        # curr = Line2D([i+.5, i+1], [j-1, j-.5], color='b')
        curr = Line2D([i-1, i - .5], [j + .5, j + 1], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 14:
        # curr = Line2D([i, i+.5], [j-.5, j-1], color='b')
        curr = Line2D([i-.5, i - 1], [j, j +.5], color='b')
        lines.append(curr)
        ax.add_line(curr)


if __name__ == "__main__":
    main()