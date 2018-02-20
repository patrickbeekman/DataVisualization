import sys
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

def main():
    df = pd.read_csv(sys.argv[1], sep=",", header=0)
    X = df.iloc[:, :4]
    Y = df.iloc[:, 4]

    maxes = X.max()
    mins = df.min(axis=0).values[:4]

    scaler = MinMaxScaler()
    scaler.fit(X)
    MinMaxScaler(feature_range=(1, 10))
    scaled_X = scaler.transform(X)

    x_pos = [0, 1, 2, 3]
    plt.title("Iris Parallel coordinates")
    for i in range(len(X)):
        if Y.iloc[i] == 'Iris-setosa':
            color = '#42b0f4'
        elif Y.iloc[i] == 'Iris-versicolor':
            color = '#9b41f4'
        else:
            color = '#f44149'
        plt.plot(x_pos, scaled_X[i], color=color)

    plt.plot([0,0],[0,1], color='k')
    plt.plot([1,1],[0,1], color='k')
    plt.plot([2,2],[0,1], color='k')
    plt.plot([3,3],[0,1], color='k')

    # 'sepal length', 'sepal width', 'petal length', 'petal width'
    plt.text(0, -.1, 'sepal length', horizontalalignment='center')
    plt.text(1, -.1, 'sepal width', horizontalalignment='center')
    plt.text(2, -.1, 'petal length', horizontalalignment='center')
    plt.text(3, -.1, 'petal width', horizontalalignment='center')

    plt.text(0, -0.05, mins[0], horizontalalignment='center')
    plt.text(1, -0.05, mins[1], horizontalalignment='center')
    plt.text(2, -0.05, mins[2], horizontalalignment='center')
    plt.text(3, -0.05, mins[3], horizontalalignment='center')

    plt.text(0, 1.02, maxes[0], horizontalalignment='center')
    plt.text(1, 1.02, maxes[1], horizontalalignment='center')
    plt.text(2, 1.02, maxes[2], horizontalalignment='center')
    plt.text(3, 1.02, maxes[3], horizontalalignment='center')

    plt.text(0, -0.175, 'Iris-setosa', bbox=dict(facecolor='#42b0f4'))
    plt.text(.6, -0.175, 'Iris-versicolor', bbox=dict(facecolor='#9b41f4'))
    plt.text(1.35, -0.175, 'Iris-virginica', bbox=dict(facecolor='#f44149'))


    # add a legend, scales and x/y labels (if necessary)
    plt.axis('off')
    plt.savefig(sys.argv[2])
    #plt.show()


if __name__ == "__main__":
    main()