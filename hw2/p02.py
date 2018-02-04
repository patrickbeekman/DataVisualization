import sys
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np

def main():
    iris = pd.read_csv(sys.argv[1], header=0)
    X = iris.loc[:,:'petal width']
    X_norm = normalize(X)
    Y = iris.loc[:,'class']

    pca = PCA(n_components=4)
    pca.fit(X)
    X = pca.transform(X)

    plt.scatter(-X[:,0], -X[:,2], marker=(4,2,0))
    plt.xlabel("Negative PC1")
    plt.ylabel("Negative PC3")
    plt.title("Clustering the iris dataset")
    plt.savefig("fig_2_4.png")
    #plt.show()


if __name__ == "__main__":
    main()