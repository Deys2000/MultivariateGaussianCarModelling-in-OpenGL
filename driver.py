import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui
from PyQt5.QtOpenGL import *
from PyQt5 import QtCore, QtWidgets, QtOpenGL
import numpy as np


# creates the main window and calls the glWidget Class for contents
class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
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
        window_width = 800

        QGLWidget.__init__(self, parent)
        self.setMinimumSize(window_width, window_height)

        # rotation variables
        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0
        # translation variables
        self.x = 0.0
        self.y = 0.0
        self.z = -80.0
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
        gluPerspective(45.0, window_width / window_height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def initGeometry(self):
        glEnable(GL_LIGHT0)
        glClearColor(1, 0, 0, 1)  # sets a black background
        glEnable(GL_DEPTH_TEST)

    # ------------- Car Modeling Happens Here -----------

    # this function is repeatedly called to update the frame
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # i am unable to use the lookat function properly :(
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

        # functions for tire, body and then whole car

        # Rendering Begins Here
        self.renderCylinder( [1,0,0], [0,0,0] , 5)
        self.renderCylinder( [0,1,0], [0,0,-5] , 10)
        self.renderCylinder( [0,0,1], [0,0,-10], 15)

    def renderCylinder(self, color, centerTuple, r):
        glColor3f(color[0], color[1], color[2])
        glPolygonMode(GL_FRONT, GL_FILL)
        glBegin(GL_TRIANGLES)
        center = (centerTuple[0], centerTuple[1], centerTuple[2])
        radius = r
        step = 5
        for theta in range(0, 360, step):
            glVertex3f(center[0], center[1], center[2])
            arc_start = theta * (np.pi / 180)
            arc_end = (theta + step) * (np.pi / 180)
            glVertex3f(radius * np.cos(arc_start), radius * np.sin(arc_start), center[2])
            glVertex3f(radius * np.cos(arc_end), radius * np.sin(arc_end), center[2])
        glEnd()
        glFlush()

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

    # ------------------- Variable Setters -----------------

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
            self.setXTranslation(1)
        elif event.key() == QtCore.Qt.Key.Key_D:
            print("-X")
            self.setXTranslation(-1)
        elif event.key() == QtCore.Qt.Key.Key_Up:
            print("+Y")
            self.setYTranslation(1)
        elif event.key() == QtCore.Qt.Key.Key_Down:
            print("-Y")
            self.setYTranslation(-1)
        elif event.key() == QtCore.Qt.Key.Key_W:
            print("+Z")
            self.setZTranslation(1)
        elif event.key() == QtCore.Qt.Key.Key_S:
            print("-Z")
            self.setZTranslation(-1)

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(Form)
    ui.show()
    sys.exit(app.exec_())
