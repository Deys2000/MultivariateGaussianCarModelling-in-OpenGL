import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui
from PyQt5.QtOpenGL import *
from PyQt5 import QtCore, QtWidgets, QtOpenGL
import numpy as np
import matlab.engine
from scipy.io import loadmat

# creates the main window and calls the glWidget Class for contents
class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):


        #GUI and opengl
        super(Ui_MainWindow, self).__init__()
        self.widget = glWidget()  # calling glWidget for object creation
        self.widget.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        #        self.button = QtWidgets.QPushButton('Test', self)
        mainLayout = QtWidgets.QHBoxLayout()  # establishing the layout style
        mainLayout.addWidget(self.widget)  # adding items
        #        mainLayout.addWidget(self.button) # adding items
        self.setLayout(mainLayout)  # setting up the added items on the layout into window


class glWidget(QGLWidget):

    def __init__(self, parent=None):
        window_height = 800
        window_width = 800

        QGLWidget.__init__(self, parent)
        self.setMinimumSize(window_width, window_height)

        # #maltab calc
        self.eng = matlab.engine.start_matlab()
        self.eng.MultivariateNormalOf2021Cars(nargout=0)
        self.eng.quit()

        parameter_data = loadmat('ModellingData.mat')
        self.carDimensions =  parameter_data.get('X')

        # translation variables - inital values
        self.x = 20.0*10
        self.y = -30.0*10
        self.z = -100.0*10
        # rotation variables - initial values
        self.rotX = 0.0
        self.rotY = 45.0
        self.rotZ = 0.0
        # scaling variables
        self.zoom = 0

    # called before main program runs
    def initializeGL(self, mat_specular=None):
        window_height = 800
        window_width = 800

        # # Lighting
        # glEnable(GL_LIGHTING)
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, GLfloat_3(.8, .8, .3))
        # glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(1, 1, 3, 0))
        # glEnable(GL_LIGHT0)

        # mat_specular = { 1.0, 1.0, 1.0, 1.0}
        # mat_shininess = {50}
        # light_position = {1.0,1.0,1.0,0.0}
        # glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        # glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
        # glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        #
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)
        # glEnable(GL_DEPTH_TEST)

        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)

        #glLoadIdentity()
        gluPerspective(45.0, window_width / window_height, 0.1, 5000.0)
        glViewport(0,0,window_width,window_height) # corrects the y axis compression. Read more here: https://www.glprogramming.com/red/chapter03.html
        glMatrixMode(GL_MODELVIEW)

    # def initGeometry(self):
    #     glEnable(GL_LIGHTING)
    #     glLightfv(GL_LIGHT0, GL_DIFFUSE, GLfloat_3(.8, .8, .3))
    #     glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(0, 0, 0, 0))
    #     glEnable(GL_LIGHT2)
    #     glClearColor(0, 0, 0, 1)  # sets a black background
    #     glEnable(GL_DEPTH_TEST)




    # ------------- Car Modeling Happens Here -----------

    # this function is repeatedly called to update the frame
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # i am unable to use the lookat function properly here :(
        # gluLookAt(
        #     0,0,self.zoom, # camera position
        #     0,0,0, # camera direction
        #     0,1,0
        # )

        # rotations and translations must be done before rendering
        glTranslatef(self.x, self.y, self.z)
        glRotate(self.rotX, 1, 0, 0)
        glRotate(self.rotY, 0, 1, 0)
        glRotate(self.rotZ, 0, 0, 1)

        self.renderCoordinateArrows()

        #for multiple cars
        anchorStepsX = 0
        for dimensions in self.carDimensions:
            self.renderCar((anchorStepsX,0,0), dimensions )
            anchorStepsX += 300

    def renderCar(self, anchor, parameterData):
        # COLORS
        brown_dark = (130/256, 60/256, 0/256)
        brown_regular = (140/256, 67/256, 0/256)
        brown_light = (100/256, 75/256, 0/256)
        black = (0,0,0)
        near_black = (50/256,50/256,50/256)
        gray_dark = (160/256, 160/256, 160/256)
        gray_regular = (180/256,180/256,180/256)
        gray_light = (250/256, 250/256, 250/256)

        gray_regular= gray_light
        red = (1,0,0)
        blue = (0,0,1)
        green = (0,1,0)
        yellow = (1,1,0)
        purple = (1,0,1)
        blue_green = (0,1,1)

        #parameterData has the following information: [A1';C1';D1';E1';F1';G1';OH';OL';OW';TWF';TWR']
        a = parameterData[0]
        #b = parameterData[1] no longer using B, this variable is not stable
        c = parameterData[1]
        d = parameterData[2]
        e = parameterData[3]
        f = parameterData[4]
        g = parameterData[5]
        oh = parameterData[6]
        ol = parameterData[7]
        ow = parameterData[8]
        twf = parameterData[9]
        twr = parameterData[10]
        #wb = parameterData[11] no longer using wheelbase

        #tire_radius = oh-c-d
        ## tire_radius = 43.18 # according to https://autosphere.ca/tires/2018/02/16/north-american-market-overview-industry-snapshot/
        #tire_width = ow-twf
        ## tire_width = 22.5 + 15 # according to  https://autosphere.ca/tires/2018/02/16/north-american-market-overview-industry-snapshot/

        # ALL PASSED DIMENSIONS
        # ow = 30 # overall width
        # ol = 70 # overall length
        # oh = 40 # overall height
        # a = 15 # length of front hood
        # c = 10 # window height
        # d = 20 # door height
        # f = 10 # front tire clearance
        # g = 10 # back tire clearance
        # e = 25 # Width of roof

        # EXAMPLE VEHICLES

        # Chevrolet Malibu 4Dr Sedan
        # ow = 185; ol = 492; oh = 146; a = 129; c = 35; d = 83; e = 118; f = 97; g = 113; twf = 159;

        # Ford F-450 Crew Cab
        # ow = 203; ol = 670; oh = 206; a = 134; c = 47; d = 90; e = 141; f = 97; g = 126; twf = 190;

        # GMC Acadia SUV AWD
        # ow = 192; ol = 491; oh = 169; a = 119; c = 43; d = 82; e = 102; f = 94; g = 112; twf = 164;

        # Hyundai Venue SUV
        #ow = 177; ol = 404; oh = 159; a = 109; c = 36; d = 87; e = 92; f = 97; g = 74; twf = 154;

        # Mercedes S Class Sedan
        # ow = 190; ol = 529; oh = 150; a = 155; c = 36; d = 87; e = 114; f = 91; g = 113; twf = 160



        tire_radius = 43.18
        tire_width = ow-twf + 5 # plus 5 added purely for visual purposes

        # ALL  VERTICES
        v1  = (anchor[0] + (ow - e) / 2      , anchor[1] + (oh - c - d)           , anchor[2])
        v2  = (anchor[0] + (ow - e) / 2      , anchor[1] + (oh - c - d * (1 / 5)) , anchor[2])
        v3  = (anchor[0] + ow - (ow - e) / 2 , anchor[1] + (oh - c - d * (1 / 5)) , anchor[2])
        v4  = (anchor[0] + ow - (ow - e) / 2 , anchor[1] + (oh - c - d)           , anchor[2])
        v5  = (anchor[0]                     , anchor[1] + (oh - c - d)           , anchor[2] - a * (1 / 5))
        v6  = (anchor[0]                     , anchor[1] + (oh - c)               , anchor[2] - a * (1 / 5))
        v7  = (anchor[0] + ow                , anchor[1] + (oh - c)               , anchor[2] - a * (1 / 5))
        v8  = (anchor[0] + ow                , anchor[1] + (oh - c - d)           , anchor[2] - a * (1 / 5))
        v9  = (anchor[0]                     , anchor[1] + (oh - c)               , anchor[2] - a)
        v10 = (anchor[0] + ow                , anchor[1] + (oh - c)               , anchor[2] - a)
        v11 = (anchor[0] + (ow - e) / 2      , anchor[1] + oh                     , anchor[2] - a - (ol - a) * (2 / 10))
        v12 = (anchor[0] + ow - (ow - e) / 2 , anchor[1] + oh                     , anchor[2] - a - (ol - a) * (2 / 10))
        v13 = (anchor[0] + (ow - e) / 2      , anchor[1] + oh                     , anchor[2] - (ol - (ol - a) * (1 / 10)))
        v14 = (anchor[0] + ow - (ow - e) / 2 , anchor[1] + oh                     , anchor[2] - (ol - (ol - a) * (1 / 10)))
        v15 = (anchor[0]                     , anchor[1] + (oh - c)               , anchor[2] - ol)
        v16 = (anchor[0] + ow                , anchor[1] + (oh - c)               , anchor[2] - ol)
        v17 = (anchor[0]                     , anchor[1] + (oh - c - d)           , anchor[2] - ol)
        v18 = (anchor[0] + ow                , anchor[1] + (oh - c - d)           , anchor[2] - ol)
        # wheel centers
        v19 = (anchor[0] + ow - (ow-twf)/2   , anchor[1] + tire_radius           , anchor[2] - f)
        v20 = (anchor[0] + (ow-twf)/2        , anchor[1] + tire_radius           , anchor[2] - f)
        v21 = (anchor[0] + ow - (ow-twf)/2   , anchor[1] + tire_radius           , anchor[2] - (ol - g))
        v22 = (anchor[0] + (ow-twf)/2        , anchor[1] + tire_radius           , anchor[2] - (ol - g))

        # un-comment if you want to display or see values of vertices
        self.displayVertices((v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,v21,v22))
        # self.printVertices((v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,v21,v22))

        # Render Body
        self.renderQuad(v1,v2,v3,v4,        brown_light) # face 11
        self.renderQuad(v1,v2,v6,v5,        brown_light) # face 13
        self.renderQuad(v2,v3,v7,v6,        brown_light) # face 10
        self.renderQuad(v3,v4,v8,v7,        brown_light) # face 12
        self.renderQuad(v6, v7, v10, v9,    brown_light)  # face 9
        self.renderQuad(v9, v10, v12, v11,  near_black)  # face 8
        self.renderQuad(v11, v12, v14, v13, brown_light)  # face 1
        self.renderQuad(v13, v14, v16, v15, near_black)  # face 2
        self.renderQuad(v16, v15, v17, v18, brown_light)  # face 3
        self.renderQuad(v10, v12, v14, v16, near_black)  # face 4
        self.renderQuad(v8, v7, v16, v18,   brown_light)  # face 5
        self.renderQuad(v5, v6, v15, v17,   brown_light)  # face 7
        self.renderQuad(v9, v11, v13, v15,  near_black)  # face 6
        self.renderQuad(v5, v8, v18, v17,   brown_light)  # face 14
        #self.renderQuad(v3, v4, v8, v7)  # face 15

        # Render 4 Tires
        self.renderCylinder(gray_dark, [v19[0],v19[1],v19[2]],      tire_radius, tire_width)
        self.renderCylinder(gray_dark, [v20[0],v20[1],v20[2]],      tire_radius, tire_width)
        self.renderCylinder(gray_dark, [v21[0],v21[1],v21[2]],      tire_radius, tire_width)
        self.renderCylinder(gray_dark, [v22[0],v22[1],v22[2]],      tire_radius, tire_width)

        #Render Ground Plane
        self.renderGroundPlane(anchor, ow, ol)
        self.renderBackground(anchor, ow, ol, oh)
        glFlush()

    # ------------------------ Modeling Functions ------------------------------------

    def renderBackground(self, anchor, overall_width, overall_length, overall_height):
        #currently hardcoded
        right = -2000
        left = 2000
        front = -2000
        behind = 2000
        tall = 3000

        self.renderQuad( (left,0,behind), (left,0,front), (left,tall,front), (left,tall,behind), (0,0.5,0.5)) #left
        self.renderQuad( (right,0,behind), (right,0,front), (right,tall,front), (right,tall,behind), (0,0.5,0.5)) #right
        self.renderQuad( (right,0,behind), (right,tall,behind), (left,tall,behind), (left,0,behind), (0,0.5,0.5)) #behind
        self.renderQuad((right, 0,front), (right, tall, front), (left, tall, front), (left, 0, front),(0, 0.5, 0.5)) #front

    def renderGroundPlane(self, anchor, overall_width, overall_length):
        # xSharpness = 4
        # zSharpness = 4
        # zLength = overall_length * 3
        # xLength = overall_width * 3
        # xStart = anchor[0] - (xLength-overall_width)/2
        # zStart = anchor[2] - zLength + (zLength-overall_length)/2
        # xSteps = xLength/xSharpness
        # zSteps = zLength/zSharpness

        red = (1,0,0)
        blue = (0,1,0)
        green = (0,0,1)
        yellow = (1,1,0)
        purple = (1,0,1)
        blue_green = (0,1,1)
        brown_dark = (130 / 256, 60 / 256, 0 / 256)
        brown_regular = (140 / 256, 67 / 256, 0 / 256)
        brown_light = (150 / 256, 75 / 256, 0 / 256)
        black = (0, 0, 0)
        gray_dark = (100 / 256, 100 / 256, 100 / 256)
        gray_light = (200 / 256, 200 / 256, 200 / 256)

        # Dynamic checkered ground plane

        # for x in range ( 0 , xSharpness):
        #     for z in range ( 0, zSharpness):
        #         v1 = (xStart + x*xSteps ,           0, zStart + z*zSteps )
        #         v2 = (xStart + (x+1)*xSteps,        0, zStart + z*zSteps )
        #         v3 = (xStart + (x+1)*xSteps,        0, zStart + (z+1)*zSteps)
        #         v4 = (xStart + x*xSteps,            0, zStart + (z+1)*zSteps)
        #         if( np.mod(x+z,2) == 1):
        #             color = brown_dark
        #         else:
        #             color = brown_regular
        #         self.renderQuad(v1, v2, v3, v4, color)

        # Hardcoded Ground Plane
        xLength = 4000
        zLength = 6000
        xStart = overall_width/2 - xLength/2
        zStart = - overall_length/2 - zLength/2
        xSharpness = 50
        zSharpness = 75
        xSteps = xLength/xSharpness
        zSteps = zLength/zSharpness

        for x in range(0, xSharpness):
            for z in range ( 0, zSharpness):
                v1 = (xStart + x*xSteps ,           0, zStart + z*zSteps )
                v2 = (xStart + (x+1)*xSteps,        0, zStart + z*zSteps )
                v3 = (xStart + (x+1)*xSteps,        0, zStart + (z+1)*zSteps)
                v4 = (xStart + x*xSteps,            0, zStart + (z+1)*zSteps)
                if( np.mod(x+z,2) == 1):
                    color = gray_light
                else:
                    color = gray_dark
                self.renderQuad(v1, v2, v3, v4, color)


# This method makes a quad plane given 4 vertices and a color
# Its purpose is to shorten the length of the code although glBegin and glEnd repeatedly may not be efficient
    def renderQuad(self, v1, v2, v3, v4, color):
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_QUADS)
        glColor3f(color[0],color[1],color[2])
        glVertex3f(v1[0],v1[1],v1[2])
        glVertex3f(v2[0],v2[1],v2[2])
        glVertex3f(v3[0],v3[1],v3[2])
        glVertex3f(v4[0],v4[1],v4[2])
        glEnd()
        #glFlush()

# This Method is Responsible for Creating Cylinders, I use it for making tires
    def renderCylinder(self, color, centerTuple, r, t):
        center = (centerTuple[0], centerTuple[1], centerTuple[2])
        radius = r
        step = 15

        # FACE 1 OF CYLINDER
        glColor3f(color[0], color[1], color[2])
        glPolygonMode(GL_FRONT, GL_FILL)
        glBegin(GL_TRIANGLES)
        for theta in range(0, 360, step):
            glVertex3f(center[0]-(t/2), center[1], center[2])
            arc_start = theta * (np.pi / 180)
            arc_end = (theta + step) * (np.pi / 180)
            glVertex3f(center[0]-(t/2),center[1]+ radius * np.cos(arc_start),center[2]+ radius * np.sin(arc_start) )
            glVertex3f(center[0]-(t/2),center[1] + radius * np.cos(arc_end), center[2]+ radius * np.sin(arc_end) )
        glEnd()
        glFlush()

        # SIDE OF CYLINDER
        glColor3f(0,0,0) # BLACK
        glBegin(GL_QUAD_STRIP)
        for theta in range(0, 360, step):
            arc_start = theta * (np.pi / 180)
            arc_end = (theta + step) * (np.pi / 180)
            glVertex3f(center[0]-(t/2), center[1]+radius * np.cos(arc_start), center[2]+radius * np.sin(arc_start))
            glVertex3f(center[0]-(t/2), center[1]+radius * np.cos(arc_end), center[2]+ radius * np.sin(arc_end))
            glVertex3f(center[0]+(t/2), center[1]+radius * np.cos(arc_start), center[2]+radius * np.sin(arc_start))
            glVertex3f(center[0]+(t/2), center[1]+radius * np.cos(arc_end), center[2]+radius * np.sin(arc_end))
        glEnd()
        glFlush()

        # FACE 2 OF CYLINDER
        glColor3f(color[0], color[1], color[2])
        glPolygonMode(GL_FRONT, GL_FILL)
        glBegin(GL_TRIANGLES)
        for theta in range(0, 360, step):
            glVertex3f(center[0]+(t/2), center[1], center[2])
            arc_start = theta * (np.pi / 180)
            arc_end = (theta + step) * (np.pi / 180)
            glVertex3f(center[0]+(t/2),center[1]+ radius * np.cos(arc_start),center[2]+ radius * np.sin(arc_start) )
            glVertex3f(center[0]+(t/2),center[1] + radius * np.cos(arc_end), center[2]+ radius * np.sin(arc_end) )
        glEnd()
        glFlush()

# This method creates the 3 arrows that represent the coordinate axes for the viewers reference
    def renderCoordinateArrows(self):
        glBegin(GL_LINES)
        # RED ARROW - X DIRECTION
        glColor3f(1.0, 0.0, 0.0)
        # LINE
        glVertex3f(-4.0, 0.0, 0.0);
        glVertex3f(4.0, 0.0, 0.0)
        # ARROW
        glVertex3f(4.0, 0.0, 0.0);
        glVertex3f(3.0, 1.0, 0.0)
        glVertex3f(4.0, 0.0, 0.0);
        glVertex3f(3.0, -1.0, 0.0)
        # GREEN ARROW - Y DIRECTION
        glColor3f(0.0, 1.0, 0.0)
        # LINE
        glVertex3f(0.0, -4.0, 0.0);
        glVertex3f(0.0, 4.0, 0.0)
        # ARROW
        glVertex3f(0.0, 4.0, 0.0);
        glVertex3f(1.0, 3.0, 0.0)
        glVertex3f(0.0, 4.0, 0.0);
        glVertex3f(-1.0, 3.0, 0.0)
        # BLUE ARROW - Z DIRECTION
        glColor3f(0.0, 0.0, 1.0)
        # LINE
        glVertex3f(0.0, 0.0, -4.0);
        glVertex3f(0.0, 0.0, 4.0)
        # ARROW
        glVertex3f(0.0, 0.0, 4.0);
        glVertex3f(0.0, 1.0, 3.0)
        glVertex3f(0.0, 0.0, 4.0);
        glVertex3f(0.0, -1.0, 3.0)

        glEnd()
        glFlush()

    # ------------------- Variable Setter Methods -----------------

    def setXRotation(self, angle):
        self.rotX += angle
        self.update()

    def setYRotation(self, angle):
        self.rotY += angle
        self.update()

    def setZRotation(self, angle):
        self.rotZ += angle
        self.update()

    def setXTranslation(self, amount):
        self.x += amount
        self.update()

    def setYTranslation(self, amount):
        self.y += amount
        self.update()

    def setZTranslation(self, amount):
        self.z += amount
        self.update()

    def setZoom(self, amount):
        self.zoom += amount
        self.update()

    # ------------- Mouse and Keyboard Input Events ---------------

    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = (event.x() - self.lastPos.x()) / 10
        dy = (event.y() - self.lastPos.y()) / 10
        #if dx < 0:
        #    print('dx neg')
        if event.buttons() == QtCore.Qt.LeftButton:
            #self.setXRotation(dy) disabled vertical rotation
            self.setYRotation(dx)
            # print("ROTATE: " + "x = " + str(self.rotX) + "y = " + str(self.rotY) + "z = " + str(self.rotZ))
        elif event.buttons() == QtCore.Qt.RightButton:
            self.setZTranslation(dx*5)
            # print("ZOOM: " + "zoom = " + str(self.rotZ) + " -> + " + str(dx))
        self.lastPos = QtCore.QPoint(event.pos())

    def keyPressEvent(self, event):
        movement_speed = 20
        print("Key Pressed")
        if event.key() == QtCore.Qt.Key.Key_Left:
            print("+X")
            self.setXTranslation(movement_speed)
        elif event.key() == QtCore.Qt.Key.Key_Right:
            print("-X")
            self.setXTranslation(-movement_speed)
        elif event.key() == QtCore.Qt.Key.Key_Down:
            print("+Y")
            self.setYTranslation(movement_speed)
        elif event.key() == QtCore.Qt.Key.Key_Up:
            print("-Y")
            self.setYTranslation(-movement_speed)

        elif event.key() == QtCore.Qt.Key.Key_G:
            # GENERATE NEW CAR
            print("Generate Car")
            self.eng = matlab.engine.start_matlab() # starting engine takes lots of time, avoid if possible
            print("started matlab engine")
            self.eng.Sampler(nargout=0)
            print("ran sampling code")
            self.eng.quit()
            print("quit matlab engine")
            parameter_data = loadmat('ModellingData.mat')
            print("gathered parameter data")
            self.carDimensions = parameter_data.get('X')
            print(self.carDimensions)

    def printVertices(self, vertices):
        for x in vertices:
            print(x)

    def displayVertices(self, vertices):
        glEnable(GL_POINT_SMOOTH)
        glPointSize(20)
        glBegin(GL_POINTS)
        glColor3fv((1, 0, 0))
        for v in vertices:
            glVertex3d(v[0],v[1],v[2])
        glEnd()


        # elif event.key() == QtCore.Qt.Key.Key_S:
        #     print("-Z")
        #     self.setZTranslation(-movement_speed)


    # ########################
    #
    # def normalizeAngle(self, angle):
    #     while angle < 0:
    #         angle += 360
    #     while angle > 360:
    #         angle -= 360
    #     return angle
    #
    # def resetRotation(self):
    #     glTranslatef(-1.0, -1.0, -20)
    #     self.rotX = 0#260*16
    #     self.rotY = 0#200*16
    #     self.rotZ = 0#16
    #     self.update()
    #
    # #########################


# MAIN PROGRAM STARTS HERE

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(Form)
    ui.show()
    sys.exit(app.exec_())
