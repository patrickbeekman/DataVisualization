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

    X = X.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))

    x_pos = [0, 1, 2, 3]
    #x_pos = np.tile(x_pos, (len(X), 1))
    #x_pos = np.tile(x_pos, (2, 1))
    print(x_pos)
    print(X[0:2].values)
    plt.title("Iris Parallel coordinates")
    plt.plot(x_pos, X.iloc[0].values)

    plt.plot([0,0],[min(X.iloc[:,0]),max(X.iloc[:,0])])
    plt.plot([1,1],[min(X.iloc[:,1]),max(X.iloc[:,1])])
    plt.plot([2,2],[min(X.iloc[:,2]),max(X.iloc[:,2])])
    plt.plot([3,3],[min(X.iloc[:,3]),max(X.iloc[:,3])])


    plt.show()


if __name__ == "__main__":
    main()