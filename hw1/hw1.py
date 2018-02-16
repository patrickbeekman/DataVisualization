import sys
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
import pandas as pd


def main():
    cars = pd.read_csv(sys.argv[1] )
    cars.columns = ['VehicleName','SmallSporty','SportsCar','SUV','Wagon','Minivan','Pickup', 'AWD',
                    'RWD','RetailPrice','DealerCost','EngineSize(l)','Cyl','HP','CityMPG','HwyMPG','Weight','WheelBase','Len','Width']

    cars['Type'] = 0

    # set the Type value based on the car
    cars.loc[cars.SmallSporty == 1, 'Type'] = 1
    cars.loc[cars.SportsCar == 1, 'Type'] = 2
    cars.loc[cars.SUV == 1, 'Type'] = 3
    cars.loc[cars.Wagon == 1, 'Type'] = 4
    cars.loc[cars.Minivan == 1, 'Type'] = 5
    cars.loc[cars.Pickup == 1, 'Type'] = 6

    # clean the data removing any '*' and converting str to ints
    cars = cars[cars.CityMPG != '*']
    cars = cars[cars.Weight != '*']
    cars.Weight = pd.to_numeric(cars.Weight, errors='coerce')

    # create and display the scatterplot
    num = 1
    fig, ax = plt.subplots()
    for color in ['red','green','blue','magenta','cyan','yellow']:
        X = cars['HP'].where(cars['Type'] == num).dropna()
        Y = cars['CityMPG'].where(cars['Type'] == num).dropna()
        size = cars['Weight'] / 50
        ax.scatter(X, Y, c=color, s=size, marker='s', edgecolors=(0,0,0), label=cars.columns[num])
        num = num + 1

    at = AnchoredText("*Size of marker is Weight",
                      prop=dict(size=9), frameon=True,
                      loc=7,
                      )
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)
    ax.legend()
    plt.xlabel("HP")
    plt.ylabel("City MPG")
    plt.title("Horse Power vs City MPG")
    plt.savefig("fig_1_47.png")
    #plt.show()



if __name__ == "__main__":
    main()