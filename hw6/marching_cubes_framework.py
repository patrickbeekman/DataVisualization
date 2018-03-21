from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math
import numpy as np
from math import cos, sin


eye = None
target = None
up = None
fov_y = None
aspect = None
near = None
far = None
previous_point = None
window = None
button_down = None
vertices = []
normals = None
triangles = None
points = None
image_width = None
image_height = None
image_depth = None
win_id = None


def make_cubes():
    grid_size = 16
    x = np.zeros((grid_size * 3, grid_size * 3, 2))
    m, n, p = x.shape

    ii = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    jj = np.array([0, 0, 1, 1, 0, 0, 1, 1])
    kk = np.array([0, 1, 0, 1, 0, 1, 0, 1])

    for h in range(256):
        i = (h % 16) * 3
        j = int(h / 16) * 3
        x[ii+i, jj+j, kk] = [int(a)*255 for a in list('{0:08b}'.format(h))]

    for k in range(p):
        file_name = './data/cubes/%02d.pgm' % (k + 1)
        with open(file_name, 'w') as fp:
            fp.write('P2\n')
            fp.write('%d %d\n' % (n, m))
            fp.write('%d\n' % np.max(x[:, :, k]))
            for i in range(m):
                for j in range(n):
                    fp.write('%d ' % x[i, j, k])
                fp.write('\n')

    m, n, p = 2, 2, 2
    x = np.zeros((2, 2, 2))
    for h in range(256):
        x[ii, jj, kk] = [int(a)*255 for a in list('{0:08b}'.format(h))]
        file_dir = './data/cubes/%03d' % h
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)
        for k in range(2):
            file_name = '%s/%02d.pgm' % (file_dir, k + 1)
            with open(file_name, 'w') as fp:
                fp.write('P2\n')
                fp.write('%d %d\n' % (n, m))
                fp.write('%d\n' % np.max(x[:, :, k]))
                for i in range(m):
                    for j in range(n):
                        fp.write('%d ' % x[i, j, k])
                    fp.write('\n')


#make_cubes()


def mouse_func(button, state, x, y):
    global previous_point, button_down
    # print(button_down, state, x, y)
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
    global win_id
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
        new_dist = dist * 2 ** (mouse_delta_y)
        new_neg_gaze = [a / dist * new_dist for a in neg_gaze]
        new_eye = [a + b for a, b in zip(target, new_neg_gaze)]
        eye = new_eye
        glutPostRedisplay()

    # print(eye)
    previous_point = (x, y)


def read_pgm(file_name):
    image = []
    with open(file_name, 'r') as fp:
        s = fp.readline().strip()
        assert s == 'P2'
        width, height = [int(x) for x in fp.readline().strip().split()]
        max_intensity = int(fp.readline().strip())

        max_int = float('-inf')
        for line in fp.readlines():
            row = [int(x) for x in line.strip().split()]
            assert len(row) == width
            image.append(row)
            max_int = max(max(row), max_int)

        assert len(image) == height
        assert max_int == max_intensity

    return image


def rot(a, x, y, z):
    # based on http://3dengine.org/Rotate_arb
    c = cos(a*np.pi/180)
    s = sin(a*np.pi/180)
    t = 1 - c
    return np.array([
        [t*x*x+c,    t*x*y-s*z,  t*x*z+s*y],
        [t*x*y+s*z,  t*y*y+c,    t*y*z-s*x],
        [t*x*z-s*y,  t*y*z+s*x,  t*z*z+c]
    ])


unit_cube = np.array([[2*int(b)-1 for b in list('{0:03b}'.format(a))] for a in range(8)])


def rotate(r, h):
    powers = [2**i for i in range(7, -1, -1)]
    i = np.argsort(((unit_cube.dot(r)+1)/2).dot(powers[-3:]))
    return np.array([int(a) for a in list('{0:08b}'.format(h))])[i].dot(powers[::-1])


def create_mesh():
    global vertices, normals, triangles, points, rotations, image_height, image_width, image_depth

    image_directory = sys.argv[1]
    num_images = int(sys.argv[2])
    threshold = float(sys.argv[3])

    x = []
    for i in range(1, num_images+1):
        img = read_pgm('%s/%02d.pgm' % (image_directory, i))
        x.append(img)
    x = np.array(x)
    x = np.transpose(x, (1, 2, 0))

    image_width, image_height, image_depth = x.shape
    print(image_width, image_height, image_depth)

    x = (x > threshold).astype(int)

    points = []
    for i in range(image_width):
        for j in range(image_height):
            for k in range(image_depth):
                if x[i, j, k]:
                    print(i, j, k)
                    points.append(([i, j, k], [0, 1, 0]))
                else:
                    points.append(([i, j, k], [1, 0, 0]))
    points = np.array(points)

    # using rotations here: http://www.euclideanspace.com/maths/geometry/rotations/axisAngle/examples/index.htm
    sq33 = 3 ** (1/2) / 3
    sq22 = 2 ** (1/2) / 2
    rotations = [
        rot(0, 1, 0, 0),       # identity
        rot(90, 1, 0, 0),      # 90 deg about x
        rot(180, 1, 0, 0),     # 180 deg about x
        rot(-90, 1, 0, 0),     # 270 deg about x
        rot(90, 0, 1, 0),      # 90 deg about y
        rot(180, 0, 1, 0),     # 180 deg about y
        rot(-90, 0, 1, 0),     # 270 deg about y
        rot(90, 0, 0, 1),      # 90 deg about z
        rot(180, 0, 0, 1),     # 180 deg about z
        rot(-90, 0, 0, 1),     # 270 deg about z
        rot(120, sq33, sq33, sq33),     # 120 deg about ( 1, 1, 1) corner 7
        rot(-120, sq33, sq33, sq33),    # 120 deg about (-1,-1,-1) corner 0
        rot(120, sq33, sq33, -sq33),    # 120 deg about ( 1, 1,-1) corner 6
        rot(-120, sq33, sq33, -sq33),   # 120 deg about (-1,-1, 1) corner 1
        rot(120, sq33, -sq33, sq33),    # 120 deg about ( 1,-1, 1) corner 5
        rot(-120, sq33, -sq33, sq33),   # 120 deg about (-1, 1,-1) corner 2
        rot(120, sq33, -sq33, -sq33),   # 120 deg about ( 1,-1,-1) corner 4
        rot(-120, sq33, -sq33, -sq33),  # 120 deg about (-1, 1, 1) corner 3
        rot(180, sq22, sq22, 0),     # 180 deg about ( 1, 1, 0) edge 23
        rot(180, 0, sq22, sq22),     # 180 deg about ( 0, 1, 1) edge 02
        rot(180, -sq22, sq22, 0),    # 180 deg about (-1, 1, 0) edge 01
        rot(180, 0, sq22, -sq22),    # 180 deg about ( 0, 1,-1) edge 13
        rot(180, sq22, 0, sq22),     # 180 deg about ( 1, 0, 1) edge 26
        rot(180, -sq22, 0, sq22),    # 180 deg about (-1, 0, 1) edge 04
    ]

    missed = 0
    vertices = []
    normals = [] #[[1,0,0],[1,0,0],[1,0,0]]

    triangle_cases =[]
    num = get_num_from_points()
    for r in rotations:
        if rotate(r, num) == 2:
            print("case 1")
            triangle_cases = [np.array([(-1, 0, 1), (0, -1, 1), (-1, -1, 0)])]
            break
        elif rotate(r, num) == 34:
            print("case 2")
            triangle_cases = [np.array([(-1,-1,0),(-1,0,1),(1,-1,0)]),
                              np.array([(-1,0,1),(1,-1,0),(1,0,1)])]
            break
        elif rotate(r, num) == 130:
            print("case 3")
            triangle_cases = [np.array([(-1,0,1), (-1,-1,0), (0,-1,1)]),
                              np.array([(1,0,1),(0,1,1),(1,1,0)])]
            break
        elif rotate(r, num) == 49:
            print("case 4")
            triangle_cases = [np.array([(1,0,1), (-1,-1,0), (0,-1,1)]),
                              np.array([(1,0,1), (-1,-1,0), (-1,0,-1)]),
                              np.array([(1, 0, 1), (-1, 0, -1), (1,0,-1)])]
            break
        elif rotate(r, num) == 51:
            print("case 5")
            triangle_cases = [np.array([(-1,0,1), (-1,0,-1), (1,0,-1)]),
                              np.array([(-1,0,1),(1,0,-1),(1,0,1)])]
            break
        elif rotate(r, num) == 57:
            print("case 6")
            triangle_cases = [np.array([(1,0,1), (-1,-1,0), (0,-1,1)]),
                              np.array([(1,0,1), (-1,-1,0), (-1,0,-1)]),
                              np.array([(1, 0, 1), (-1, 0, -1), (1,0,-1)]),
                              np.array([(-1,0,1),(-1,1,0),(0,1,1)])]
            break
        elif rotate(r, num) == 70:
            print("case 7")
            triangle_cases = [np.array([(-1,0,1), (-1,-1,0), (0,-1,1)]),
                              np.array([(1,0,1),(0,1,1),(1,1,0)]),
                              np.array([(-1,1,0),(0,1,-1),(-1,0,-1)]),
                              np.array([(1,-1,0),(0,-1,-1),(1,0,-1)])]
            break
        elif rotate(r, num) == 23:
            print("case 8")
            triangle_cases = [np.array([(-1, 1,0), (-1,0,1), (0,1,-1)]),
                              np.array([(-1,0,1),(0,1,-1),(0,-1,1)]),
                              np.array([(0,1,-1),(0,-1,1),(1,0,-1)]),
                              np.array([(1,0,-1),(0,-1,1),(1,-1,0)])]
            break
        elif rotate(r, num) == 53:
            print("case 9")
            triangle_cases = [np.array([(-1,-1,0),(-1,1,0),(0,-1,1)]),
                              np.array([(-1,1,0),(0,-1,1),(1,0,-1)]),
                              np.array([(-1,1,0),(1,0,-1),(0,1,-1)]),
                              np.array([(0,-1,1),(1,0,-1),(1,0,1)])] ### LAST ARGUMENT MIGHT BE WRONG
            break
        elif rotate(r, num) == 66:
            print("case 10")
            triangle_cases = [np.array([(-1, 0, 1), (0, -1, 1), (-1, -1, 0)]),
                              np.array([(0,1,-1),(1,1,0),(1,0,-1)])]
            break
        elif rotate(r, num) == 98:
            print("case 11")
            triangle_cases = [np.array([(-1, -1, 0), (-1, 0, 1), (1, -1, 0)]),
                              np.array([(-1, 0, 1), (1, -1, 0), (1, 0, 1)]),
                              np.array([(0, 1, -1), (1, 1, 0), (1, 0, -1)])]
            break
        elif rotate(r, num) == 104:
            print("case 12")
            triangle_cases = [np.array([(0,1,-1),(1,1,0),(1,0,-1)]),
                              np.array([(-1,1,0),(0,1,1),(-1,0,1)]),
                              np.array([(0,-1,1),(1,0,1),(1,-1,0)])]
            break
        elif rotate(r, num) == 90:
            print("case 13")
            triangle_cases = [np.array([(-1,-1,0),(-1,1,0),(0,-1,1)]),
                              np.array([(-1,1,0),(0,-1,1),(0,1,1)]),
                              np.array([(1,1,0),(0,1,-1),(1,-1,0)]),
                              np.array([(0,1,-1),(1,-1,0),(0,-1,-1)])]
            break
        elif rotate(r, num) == 83:
            print("case 14")
            triangle_cases = [np.array([(-1,0,1),(-1,0,-1),(0,-1,1)]),
                              np.array([(-1,0,-1),(1,1,0),(0,-1,1)]),
                              np.array([(-1,0,-1),(1,1,0),(0,1,-1)]),
                              np.array([(1,1,0),(0,-1,1),(1,-1,0)])]
            break

    for triangle_case in triangle_cases:
        # invert rotation
        triangle_rot = triangle_case.dot(r.T)
        # convert from x,y,z to i,j,k
        triangle_rot = (triangle_rot + 1) / 2
        for t in triangle_rot:
            vertices.append(t)
            normals.append([1,0,0])

    vertices = np.array(vertices)
    normals = np.array(normals)

def get_num_from_points():
    return points[:,1][:,1].dot([128, 64, 32, 16, 8, 4, 2, 1])

def any_rotation(i, num):
    for r in rotations:
        temp = rotate(r, num)
        if temp == i:
            return True
    return False

def main():
    global eye, target, up, fov_y, aspect, near, far, window, image_width, image_height, image_depth, win_id
    create_mesh()

    eye = [(image_width-1)/2, (image_height-1)/2, 2*image_depth]
    target = [(image_width-1)/2, (image_height-1)/2, (image_depth-1)/2]
    up = [0, 1, 0]

    window = (800, 800)
    fov_y = 40
    near = .1
    far = 1000

    aspect = window[0] / window[1]
    light_position = eye
    light_color = [100.0, 100.0, 100.0, 1.0]

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window[0], window[1])
    win_id = glutCreateWindow('cubes')

    glClearColor(0., 0., 0., 1.)
    glShadeModel(GL_SMOOTH)
    # glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0)

    glEnable(GL_PROGRAM_POINT_SIZE)

    glEnable(GL_LIGHT0)

    # callbacks
    glutDisplayFunc(display)
    glutMouseFunc(mouse_func)
    glutMotionFunc(motion_func)

    glutMainLoop()


def display():
    global eye, target, up, fov_y, aspect, near, far, vertices, points, normals

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov_y, aspect, near, far)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(eye[0], eye[1], eye[2],
              target[0], target[1], target[2],
              up[0], up[1], up[2])

    glLightfv(GL_LIGHT0, GL_POSITION, eye)

    color = [1.0, 1.0, 0.0, 1.]
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, color)
    # glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, color)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0)

    glDisable(GL_LIGHTING)
    glBegin(GL_TRIANGLES)
    for i in range(len(vertices)):
        glColor3fv([1, 1, 1])
        glNormal3fv(normals[i, :])
        glVertex3fv(vertices[i, :])

    glEnd()

    glPointSize(10)
    glBegin(GL_POINTS)
    for point, c in points:
        glColor3fv(c)
        glVertex3fv(point)
    glEnd()
    glEnable(GL_LIGHTING)

    glutSwapBuffers()



if __name__ == '__main__':
    main()
