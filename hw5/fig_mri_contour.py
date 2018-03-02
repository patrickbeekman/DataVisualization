import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

threshold = 40
lines = []
points = []
values = []
fig = plt.figure()
ax = fig.add_subplot(111)


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
    #ct = thresholded.reshape((-1,))
    #ax.scatter(j, i, c=c, cmap='gray')
    ax.imshow(image, cmap='gray')

    for n in range(width-1):
        for m in range(height-1):
            #bit = bit_pattern(thresholded[n,m], thresholded[n+1,m], thresholded[n+1, m-1], thresholded[n, m-1])
            bit = bit_pattern(thresholded[n,m-1], thresholded[n+1,m-1], thresholded[n+1, m], thresholded[n, m])
            lookup(bit, m, n)



    #plt.show()
    plt.savefig('contour_14.png')

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
        points.append([i, j-.5])
        values.append(image[j,i])
        points.append([i+.5, j-1])
        values.append(image[j-1,i])
        curr = Line2D([i, i+.5], [j-.5, j-1], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 2:
        points.append([i+.5, j-1])
        values.append(image[j-1,i])
        points.append([i+1, j-.5])
        values.append(image[j,i+1])
        curr = Line2D([i+.5, i+1], [j-1, j-.5], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 3:
        points.append([i, j-.5])
        values.append(image[j,i])
        points.append([i+1, j-.5])
        values.append(image[j,i+1])
        curr = Line2D([i, i+1], [j-.5, j-.5], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 4:
        points.append([i+.5, j])
        values.append(image[j,i])
        points.append([i+1, j-.5])
        values.append(image[j,i+1])
        curr = Line2D([i+.5, i+1], [j, j-.5], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 5:
        points.append([i, j-.5])
        values.append(image[j,i])
        points.append([i+.5, j])
        values.append(image[j,i])

        points.append([i+.5, j-1])
        values.append(image[j-1,i])
        points.append([i+1, j-.5])
        values.append(image[j,i+1])
        curr = Line2D([i, i+.5], [j-.5, j], color='b')
        curr2 = Line2D([i+.5, i+1], [j-1, j-.5], color='b')
        lines.append(curr)
        lines.append(curr2)
        ax.add_line(curr)
        ax.add_line(curr2)
    elif val == 6:
        points.append([i+.5, j])
        values.append(image[j,i])
        points.append([i+.5, j-1])
        values.append(image[j-1,i])
        curr = Line2D([i+.5, i+.5], [j, j-1], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 7:
        points.append([i, j-.5])
        values.append(image[j,i])
        points.append([i+.5, j])
        values.append(image[j,i])
        curr = Line2D([i, i+.5], [j-.5, j], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 8:
        points.append([i, j-.5])
        values.append(image[j,i])
        points.append([i+.5, j])
        values.append(image[j,i])
        curr = Line2D([i, i+.5], [j-.5, j], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 9:
        points.append([i+.5, j])
        values.append(image[j,i])
        points.append([i+.5, j-1])
        values.append(image[j-1,i])
        curr = Line2D([i+.5, i+.5], [j, j-1], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 10:
        points.append([i, j-.5])
        values.append(image[j,i])
        points.append([i+.5, j-1])
        values.append(image[j-1,i])

        points.append([i+.5, j])
        values.append(image[j,i])
        points.append([i+1, j-.5])
        values.append(image[j,i+1])
        curr = Line2D([i, i+.5], [j-.5, j-1], color='b')
        curr2 = Line2D([i+.5, i+1], [j, j-.5], color='b')
        lines.append(curr)
        lines.append(curr2)
        ax.add_line(curr)
        ax.add_line(curr2)
    elif val == 11:
        points.append([i+.5, j])
        values.append(image[j,i])
        points.append([i+1, j-.5])
        values.append(image[j,i+1])
        curr = Line2D([i+.5, i+1], [j, j-.5], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 12:
        points.append([i, j-.5])
        values.append(image[j,i])
        points.append([i+1, j-.5])
        values.append(image[j,i+1])
        curr = Line2D([i, i+1], [j-.5, j-.5], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 13:
        points.append([i+.5, j-1])
        values.append(image[j-1,i])
        points.append([i+1, j-.5])
        values.append(image[j,i+1])
        curr = Line2D([i+.5, i+1], [j-1, j-.5], color='b')
        lines.append(curr)
        ax.add_line(curr)
    elif val == 14:
        points.append([i, j-.5])
        values.append(image[j,i])
        points.append([i+.5, j-1])
        values.append(image[j-1,i])
        curr = Line2D([i, i+.5], [j-.5, j-1], color='b')
        lines.append(curr)
        ax.add_line(curr)


if __name__ == "__main__":
    main()