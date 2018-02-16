import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

# initialize basic variables
n = 24
m = 12
p = 20
c = 20
alpha = 0.02

def main():
    with open(sys.argv[1], newline='') as csvfile:
        chords = list(csv.reader(csvfile))

    # Create 3d matrix 'W' of size p x p x m aka 20 x 20 x 12
    W = np.zeros((p, c, m))

    # Initialize W
    for i in range(p):
        for j in range(c):
            for k in range(m):
                W[i, j, k] = np.random.random_sample()
    
    for my_lambda in range(360):
        for t in range(24):
            r_t = chords[np.random.random_integers(1,24)]
            index_i, index_j = similar(r_t, W)
            for x in range(p):
                for y in range(p):
                    sigma = (1/3)*(p - 1 - (my_lambda/c))
                    theta = np.power(np.e, -(np.power(distance(index_i, index_j, x, y),2)/(2 * sigma * sigma)))
                    new_r_t = list(map(float, r_t[1:]))
                    W[x][y] = W[x][y] + theta*alpha*(new_r_t - W[x][y])

    plot_all(chords, W)
    plot_heat_CM(chords[1][1:], W)
    plot_heat_Cm(chords[13][1:], W)


def plot_all(chords, w):
    plt.figure(0)
    plt.title("Chords plot")
    plt.axis([-1, 21, -1, 21])
    for i in range(1, len(chords)):
        cur_chord = list(map(float, chords[i][1:]))
        max_mag = 0
        best_x = 0
        best_y = 0
        for j in range(p):
            for k in range(c):
                # find the neuron in w that is most similar to the cur chord
                #mag = w[j][k].dot(cur_chord)
                cur_chord = np.array(cur_chord, dtype=np.float)
                mag = cur_chord.dot(w[j][k])
                if mag > max_mag:
                    max_mag = mag
                    best_x = j
                    best_y = k
        plt.text(best_x, best_y, s=(chords[i][0]+""))
    plt.grid(True)
    plt.savefig(sys.argv[2])


def plot_heat_CM(CM, w):
    plt.figure(1)
    plt.title("CM heat map")
    heat = np.zeros((20, 20))
    for i in range(p):
        for j in range(c):
            heat[i][j] = np.array(CM, dtype=np.float).dot(w[i][j])
    plt.imshow(heat, cmap='summer', interpolation='nearest')
    plt.savefig(sys.argv[3])


def plot_heat_Cm(Cm, w):
    plt.figure(2)
    plt.title("Cm heat map")
    heat = np.zeros((20, 20))
    for i in range(p):
        for j in range(c):
            heat[i][j] = np.array(Cm, dtype=np.float).dot(w[i][j])
    plt.imshow(heat, cmap='winter', interpolation='nearest')
    plt.savefig(sys.argv[4])


# Torus distance function
def distance(index_i, index_j, x, y):
    # sqrt(min(|x1 - x2|, w - |x1 - x2|)^2 + min(|y1 - y2|, h - |y1-y2|)^2)
    val1 = np.abs(index_i - x)
    val2 = np.abs(index_j - y)
    return np.sqrt(np.power(min(val1, p - val1), 2) + np.power(min(val2, c - val2), 2))


def similar(r_t, w):
    min_dist = 99999999
    index_i = 0
    index_j = 0
    # convert the r_t into a list of floats without the 'Note' at index 0
    r_t = list(map(float, r_t[1:]))
    for ind_i in range(p):
        for ind_j in range(c):
            vec = (w[ind_i][ind_j] - r_t)
            dist = np.sqrt(vec.dot(vec))
            if dist <= min_dist:
                min_dist = dist
                index_i = ind_i
                index_j = ind_j
    return index_i, index_j

if __name__ == "__main__":
    main()

