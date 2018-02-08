import pandas as pd
import json
import os
import sys


def main():
    print("Hello world!")
    chords = pd.read_csv(sys.argv[1], header=0)
    print(chords)


if __name__ == "__main__":
    main()

