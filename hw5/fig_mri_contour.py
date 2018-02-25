import sys
import os
import matplotlib
import pandas as pd


def main():
    mri_path = os.path.dirname(__file__) + "/mri/14.pgm"
    with open(mri_path, 'r') as file:
        file_format = file.readline()
        width = file.read(3)
        file.read(1)
        height = file.read(3)
        file.read(1)
        max = file.read(2)
        file.read(1)

    df = pd.read_csv(mri_path, delim_whitespace=True, header=3)
    print(df)



if __name__ == "__main__":
    main()