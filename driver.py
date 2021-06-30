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
        window_height = 600
        window_width = 1000

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
    def initializeGL(self):
        window_height = 600
        window_width = 800

        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, window_width / window_height, 0.1, 10000.0)
        glMatrixMode(GL_MODELVIEW)

    # def initGeometry(self):
    #     glEnable(GL_LIGHTING)
    #     glEnable(GL_LIGHT0)
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
        anchorStepsX = 0
        for dimensions in self.carDimensions:
            self.renderCar((anchorStepsX,0,0), dimensions )
            anchorStepsX += 300

    def renderCar(self, anchor, parameterData):
        # COLORS
        brown_dark = (130/256, 60/256, 0/256)
        brown_regular = (140/256, 67/256, 0/256)
        brown_light = (150/256, 75/256, 0/256)
        black = (0,0,0)
        gray_dark = (40/256, 40/256, 40/256)
        gray_light = (200/256, 200/256, 200/256)
        red = (1,0,0)
        blue = (0,1,0)
        green = (0,0,1)
        yellow = (1,1,0)
        purple = (1,0,1)
        blue_green = (0,1,1)

        #dataTable = [A1';B1';C1';D1';E1';F1';G1';OH';OL';OW';TWF';TWR';WB']
        a = parameterData[0]
        b = parameterData[1]
        c = parameterData[2]
        d = parameterData[3]
        e = parameterData[4]
        f = parameterData[5]
        g = parameterData[6]
        oh = parameterData[7]
        ol = parameterData[8]
        ow = parameterData[9]
        twf = parameterData[10]
        twr = parameterData[11]
        wb = parameterData[12]
        tire_radius = oh-c-d
        tire_width = ow-twf

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
        # tire_radius = oh - c  - d
        # tire_width = ow-e

        # ALL CALCULATED VERTICES
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
        v11 = (anchor[0] + (ow - e) / 2      , anchor[1] + oh                     , anchor[2] - a - (ol - a) * (2 / 8))
        v12 = (anchor[0] + ow - (ow - e) / 2 , anchor[1] + oh                     , anchor[2] - a - (ol - a) * (2 / 8))
        v13 = (anchor[0] + (ow - e) / 2      , anchor[1] + oh                     , anchor[2] - (ol - (ol - a) * (1 / 8)))
        v14 = (anchor[0] + ow - (ow - e) / 2 , anchor[1] + oh                     , anchor[2] - (ol - (ol - a) * (1 / 8)))
        v15 = (anchor[0]                     , anchor[1] + (oh - c)               , anchor[2] - ol)
        v16 = (anchor[0] + ow                , anchor[1] + (oh - c)               , anchor[2] - ol)
        v17 = (anchor[0]                     , anchor[1] + (oh - c - d)           , anchor[2] - ol)
        v18 = (anchor[0] + ow                , anchor[1] + (oh - c - d)           , anchor[2] - ol)
        v19 = (anchor[0] + ow                , anchor[1] + (oh - c - d)           , anchor[2] - f)
        v20 = (anchor[0]                     , anchor[1] + (oh - c - d)           , anchor[2] - f)
        v21 = (anchor[0] + ow                , anchor[1] + (oh - c - d)           , anchor[2] - (ol - g))
        v22 = (anchor[0]                     , anchor[1] + (oh - c - d)           , anchor[2] - (ol - g))


        # Render Body
        self.renderQuad(v1,v2,v3,v4,        brown_dark ) # face 11
        self.renderQuad(v1,v2,v6,v5,        brown_regular) # face 13
        self.renderQuad(v2,v3,v7,v6,        brown_regular) # face 10
        self.renderQuad(v3,v4,v8,v7,        brown_regular) # face 12
        self.renderQuad(v6, v7, v10, v9,    brown_light)  # face 9
        self.renderQuad(v9, v10, v12, v11,  gray_dark)  # face 8
        self.renderQuad(v11, v12, v14, v13, brown_light)  # face 1
        self.renderQuad(v13, v14, v16, v15, gray_dark)  # face 2
        self.renderQuad(v16, v15, v17, v18, brown_dark)  # face 3
        self.renderQuad(v10, v12, v14, v16, gray_dark)  # face 4
        self.renderQuad(v8, v7, v16, v18,   brown_light)  # face 5
        self.renderQuad(v5, v6, v15, v17,   brown_light)  # face 7
        self.renderQuad(v9, v11, v13, v15,  gray_dark)  # face 6
        self.renderQuad(v5, v8, v18, v17,   gray_light)  # face 14
        #self.renderQuad(v3, v4, v8, v7)  # face 15

        # Render 4 Tires
        self.renderCylinder(gray_dark, [v19[0],v19[1],v19[2]],      tire_radius, tire_width)
        self.renderCylinder(gray_dark, [v20[0],v20[1],v20[2]],      tire_radius, tire_width)
        self.renderCylinder(gray_dark, [v21[0],v21[1],v21[2]],      tire_radius, tire_width)
        self.renderCylinder(gray_dark, [v22[0],v22[1],v22[2]],      tire_radius, tire_width)

    # ------------------------ Modeling Functions ------------------------------------

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
        glFlush()

# This Method is Responsible for Creating Cylinders, I use it for making tires
    def renderCylinder(self, color, centerTuple, r, t):
        center = (centerTuple[0], centerTuple[1], centerTuple[2])
        radius = r
        step = 5

        # FACE 1 OF CYLINDER
        glColor3f(color[0], color[1], color[2])
        glPolygonMode(GL_FRONT, GL_FILL)
        glBegin(GL_TRIANGLES)
        for theta in range(0, 360, step):
            glVertex3f(center[0], center[1], center[2])
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
            glVertex3f(center[0], center[1], center[2])
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
        if dx < 0:
            print('dx neg')
        if event.buttons() == QtCore.Qt.LeftButton:
            self.setXRotation(dy)
            self.setYRotation(dx)
            print("ROTATE: " + "x = " + str(self.rotX) + "y = " + str(self.rotY) + "z = " + str(self.rotZ))
        elif event.buttons() == QtCore.Qt.RightButton:
            self.setZoom(dx)
            print("ZOOM: " + "zoom = " + str(self.zoom) + " -> + " + str(dx))
        self.lastPos = QtCore.QPoint(event.pos())

    def keyPressEvent(self, event):
        print("Key Pressed")
        if event.key() == QtCore.Qt.Key.Key_A:
            print("+X")
            self.setXTranslation(20)
        elif event.key() == QtCore.Qt.Key.Key_D:
            print("-X")
            self.setXTranslation(-20)
        elif event.key() == QtCore.Qt.Key.Key_Up:
            print("+Y")
            self.setYTranslation(20)
        elif event.key() == QtCore.Qt.Key.Key_Down:
            print("-Y")
            self.setYTranslation(-20)
        elif event.key() == QtCore.Qt.Key.Key_W:
            print("+Z")
            self.setZTranslation(20)
        elif event.key() == QtCore.Qt.Key.Key_S:
            print("-Z")
            self.setZTranslation(-20)


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
