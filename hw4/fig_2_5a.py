import sys
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv(sys.argv[1], sep=",", header=0)
    print("file saved to: ", sys.argv[2])
    X = df.iloc[:, :4]
    Y = df.iloc[:, 4]

    #X = X.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))

    mins = df.min(axis=0).values[:4]
    X = X - mins

    x_pos = [0, 1, 2, 3]
    #x_pos = np.tile(x_pos, (len(X), 1))
    #x_pos = np.tile(x_pos, (2, 1))
    print(x_pos)
    plt.title("Iris Parallel coordinates")
    for i in range(len(X)):
        if Y.iloc[i] == 'Iris-setosa':
            color = '#42b0f4'
        elif Y.iloc[i] == 'Iris-versicolor':
            color = '#9b41f4'
        else:
            color = '#f44149'
        plt.plot(x_pos, X.iloc[i].values, color=color)

    plt.plot([0,0],[min(X.iloc[:,0]),max(X.iloc[:,0])], color='k')
    plt.plot([1,1],[min(X.iloc[:,1]),max(X.iloc[:,1])], color='k')
    plt.plot([2,2],[min(X.iloc[:,2]),max(X.iloc[:,2])], color='k')
    plt.plot([3,3],[min(X.iloc[:,3]),max(X.iloc[:,3])], color='k')


    plt.show()


if __name__ == "__main__":
    main()