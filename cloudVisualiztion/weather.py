from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

eye = [2, 2, 10]
target = [0, 0, 0]
up = [0, 1, 0]
fov_y = None
aspect = None
near = None
far = None
previous_point = None
window = None
button_down = None
all_points = []


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

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    threshold = 1

    #all_points = []
    for index in range(len(metadata)):
        degree_inc = 360 / metadata[index]['sweep']['num_radials']
        ii, jj = np.meshgrid(range(len(sweeps[index])), range(len(sweeps[index][0])), indexing='ij')
        xx = (ii + 1) * np.cos(np.deg2rad(jj * degree_inc))
        yy = (ii + 1) * np.sin(np.deg2rad(jj * degree_inc))
        xx = xx.reshape((-1,))
        yy = yy.reshape((-1,))
        elevations = [metadata[index]['radials'][0]['elevation']] * xx.shape[0]
        colors = sweeps[index].reshape((-1,))
        delete_indicies = []
        for i, val in enumerate(sweeps[index].reshape((-1,))):
            if val < threshold:
                delete_indicies.append(i)
        new_xx = np.delete(xx, delete_indicies)
        new_yy = np.delete(yy, delete_indicies)
        new_elv = np.delete(elevations, delete_indicies)
        dist = np.delete(ii.reshape((-1,)), delete_indicies)
        new_zz = np.zeros(len(new_elv))
        for ind in range(len(new_elv)):
            new_zz[ind] = dist[ind]+1 * np.sin(np.deg2rad(new_elv[ind]))
        #np.sqrt(np.square(new_xx[ind]) + np.square(new_yy[ind]))

        all_points.extend(list(zip(new_xx, new_yy, new_zz)))
        #all_points.extend(list(zip(xx, yy, zz)))
        new_colors = np.delete(colors, delete_indicies)
        #ax.scatter(new_xx, new_yy, new_zz, c=new_colors, cmap='viridis')

    #plt.scatter(xx, yy, zz)#, c=colors, cmap='viridis')
    #plt.savefig("CircularVisualization3D-correct.png")
    #plt.show()

    start()
    # Next step is visualizing in 3d using all 9 sweeps
    # z = r * sin(alpha) where alpha is the angle upwards from origin at sweep 0

    sweep = 0
    # plt.clf()
    # plt.imshow(sweeps[sweep])
    # plt.colorbar()
    # plt.xlabel('angle')
    # plt.ylabel('distance')
    # plt.show()


def mouse_func(button, state, x, y):
    global previous_point, button_down
    print(button_down, state, x, y)
    previous_point = (x * 2 / window[0], -y * 2 / window[1])
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            button_down = 'left'
        elif state == GLUT_UP:
            button_down = None
    elif button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            button_down = 'right'
        elif state == GLUT_UP:
            button_down = None


def motion_func(x, y):
    # this function modeled after modeler.PerspectiveCamera.orbit() function written by 'ags' here:
    # http://www.cs.cornell.edu/courses/cs4620/2008fa/asgn/model/model-fmwk.zip
    global previous_point, eye
    x *= 2 / window[0]
    y *= -2 / window[1]
    if button_down == 'left':
        mouse_delta = [x - previous_point[0], y - previous_point[1]]
        neg_gaze = [eye[0] - target[0], eye[1] - target[1], eye[2] - target[2]]
        dist = sum([a**2 for a in neg_gaze]) ** (1/2)
        neg_gaze = [a / dist for a in neg_gaze]
        azimuth = math.atan2(neg_gaze[0], neg_gaze[2])
        elevation = math.atan2(neg_gaze[1], (neg_gaze[0]**2 + neg_gaze[2]**2)**(1/2))
        azimuth = (azimuth - mouse_delta[0]) % (2 * math.pi)
        elevation = max(-math.pi * .495, min(math.pi * .495, elevation - mouse_delta[1]))
        neg_gaze[0] = math.sin(azimuth) * math.cos(elevation)
        neg_gaze[1] = math.sin(elevation)
        neg_gaze[2] = math.cos(azimuth) * math.cos(elevation)
        mag = sum([a**2 for a in neg_gaze]) ** (1/2)
        neg_gaze = [a / mag * dist for a in neg_gaze]
        new_eye = [a + b for a, b in zip(target, neg_gaze)]
        eye = new_eye
        glutPostRedisplay()
    elif button_down == 'right':
        mouse_delta_y = y - previous_point[1]
        neg_gaze = [eye[0] - target[0], eye[1] - target[1], eye[2] - target[2]]
        dist = sum([a**2 for a in neg_gaze]) ** (1/2)
        new_dist = dist - 5 * mouse_delta_y
        new_neg_gaze = [a / dist * new_dist for a in neg_gaze]
        new_eye = [a + b for a, b in zip(target, new_neg_gaze)]
        eye = new_eye
        glutPostRedisplay()

    previous_point = (x, y)


def start():
    global eye, target, up, fov_y, aspect, near, far, window

    window = (600, 600)
    fov_y = 100
    near = 1
    far = 200

    aspect = window[0] / window[1]
    light_position = [10., 4., 10., 1.]
    light_color = [0.8, 1.0, 0.8, 1.0]

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window[0], window[1])
    glutCreateWindow('WeatherPattern')

    glClearColor(0., 0., 0., 1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    glutDisplayFunc(display)

    glutMouseFunc(mouse_func)
    glutMotionFunc(motion_func)

    glutMainLoop()


def display():
    global eye, target, up, fov_y, aspect, near, far

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov_y, aspect, near, far)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(eye[0], eye[1], eye[2],
              target[0], target[1], target[2],
              up[0], up[1], up[2])

    color = [1.0, 0., 0., 1.]
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color)

    glEnable(GL_PROGRAM_POINT_SIZE)
    gl_PointSize = 10

    glBegin(GL_POINTS)
    for point in all_points:
        glVertex3fv(list(point))
    glEnd()

    # glBegin(GL_TRIANGLES)
    # for v, n in zip(vertices, normals):
    #     glNormal3fv(list(n))
    #     glVertex3fv(list(v))
    #
    # glEnd()

    glutSwapBuffers()

if __name__ == '__main__':
    main()
