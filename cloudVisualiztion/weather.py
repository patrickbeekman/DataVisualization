import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def read_reflectivity(file_name):
    sweeps = []
    metadata = []
    with open(file_name, 'rb') as fp:
        for sweep in range(1, 10):
            # read sweep delimiter
            line = fp.readline().strip().decode('utf-8')
            header = 'SWEEP%dRFLCTVTY' % sweep
            if line != header:
                print('Error: Failed to find "%s" in "%s"' % (header, line))
                return

            # print('Sweep %d' % sweep)

            # read latitude, longitude, height
            line = fp.readline().strip().decode('utf-8')
            # print(line)
            tokens = line.split()
            if len(tokens) != 6 or tokens[0] != 'Latitude:' or tokens[2] != 'Longitude:' or tokens[4] != 'Height:':
                print('Error: Failed to find Lat, Lon, Ht in %s' % tokens)
                return
            latitude = float(tokens[1])
            longitude = float(tokens[3])
            height = float(tokens[5])
            # print('lat', latitude, 'lon', longitude, 'height', height)

            # read number of radials
            num_radials = int(fp.readline().strip().decode('utf-8'))
            # print(num_radials, 'radials')

            gate_dist = float(fp.readline().strip().decode('utf-8'))
            # print(gate_dist, 'meters to gate')

            sweep_data = {
                'latitude': latitude,
                'longitude': longitude,
                'height': height,
                'num_radials': num_radials,
                'gate_dist': gate_dist
            }

            data = []
            radial_data = []
            for radial in range(num_radials):
                # print('for radial %d out of %d' % (radial, num_radials))
                tokens = fp.readline().strip().split()
                current_radial, num_gates, gate_width = (int(t) for t in tokens[:3])
                beam_width, azimuth, elevation = [float(t) for t in tokens[3:-1]]
                start_time = int(tokens[-1])
                # print(current_radial, num_gates, gate_width, beam_width, azimuth, elevation, start_time)
                empty_line = fp.readline().strip().decode('utf-8')
                if empty_line != '':
                    raise (Exception('Error: no empty line'))

                seconds_since_epoch = fp.readline().strip().decode('utf-8')
                if seconds_since_epoch != 'seconds since epoch':
                    raise (Exception('Error: no "seconds since epoch"'))

                x = np.fromfile(fp, dtype='>f', count=num_gates)
                x[x < 0] = 0
                data.append(x)
                radial_data.append({
                    'beam_width': beam_width,
                    'azimuth': azimuth,
                    'elevation': elevation,
                    'start_time': start_time,
                })
            data = np.array(data)
            data = data.T
            sweeps.append(np.array(data))
            metadata.append({
                'sweep': sweep_data,
                'radials': radial_data
            })

        sweeps = np.array(sweeps)
        for i in range(len(sweeps)):
            print('sweep %d: [%g, %g], %g +/- %g' % (
                i, sweeps[i].min(), sweeps[i].max(), sweeps[i].mean(), sweeps[i].std()))

    return sweeps, metadata


def main():
    index = 121
    file_name = './data/weather/%d.RFLCTVTY' % index
    sweeps, metadata = read_reflectivity(file_name)

    # 367 different points, divide by 360 to separate them equally.
    # degree_inc = 360/367
    # ii, jj = np.meshgrid(range(len(sweeps[0])), range(len(sweeps[0][0])), indexing='ij')
    # xx = (ii + 1) * np.cos(np.deg2rad(jj * degree_inc))
    # yy = (ii + 1) * np.sin(np.deg2rad(jj * degree_inc))
    # xx = xx.reshape((-1,))
    # yy = yy.reshape((-1,))
    # zz = [metadata[index]['radials'][0]['elevation']] * xx.shape[0]

    all_xx = []
    all_yy = []
    all_zz = []
    colors = []

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    threshold = 1

    for index in range(len(metadata)):
        degree_inc = 360 / 367
        ii, jj = np.meshgrid(range(len(sweeps[index])), range(len(sweeps[index][0])), indexing='ij')
        xx = (ii + 1) * np.cos(np.deg2rad(jj * degree_inc))
        yy = (ii + 1) * np.sin(np.deg2rad(jj * degree_inc))
        xx = xx.reshape((-1,))
        yy = yy.reshape((-1,))
        zz = [metadata[index]['radials'][0]['elevation']] * xx.shape[0]
        colors = sweeps[index].reshape((-1,))
        delete_indicies = []
        for i, val in enumerate(sweeps[index].reshape((-1,))):
            if val < threshold:
                delete_indicies.append(i)
        new_xx = np.delete(xx, delete_indicies)
        new_yy = np.delete(yy, delete_indicies)
        new_zz = np.delete(zz, delete_indicies)
        new_colors = np.delete(colors, delete_indicies)
        ax.scatter(new_xx, new_yy, new_zz, c=new_colors, cmap='viridis')

    #plt.scatter(xx, yy, zz)#, c=colors, cmap='viridis')
    plt.savefig("CircularVisualization3D-all.png")
    #plt.show()

    # Next step is visualizing in 3d using all 9 sweeps
    # z = r * sin(alpha) where alpha is the angle upwards from origin at sweep 0

    sweep = 0
    # plt.clf()
    # plt.imshow(sweeps[sweep])
    # plt.colorbar()
    # plt.xlabel('angle')
    # plt.ylabel('distance')
    # plt.show()


if __name__ == '__main__':
    main()
