import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui
from PyQt5.QtOpenGL import *
from PyQt5 import QtCore, QtWidgets, QtOpenGL
import numpy as np
import matlab.engine
from scipy.io import loadmat
import transformations as transform

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
        window_height = 1000
        window_width = 1000

        QGLWidget.__init__(self, parent)
        self.setMinimumSize(window_width, window_height)
        print("Initialized Window")

        # #maltab calc
        print("Starting MATLAB Engine")
        self.eng = matlab.engine.start_matlab()
        print("MATLAB Engine Started")
        self.eng.MultivariateNormalOf2021Cars(nargout=0)
        print("Multivariate Model Created")
        print("Ending MATLAB Engine")
        self.eng.quit()
        print("MATLAB Engine Ended")

        parameter_data = loadmat('ModellingData.mat')
        self.carDimensions =  parameter_data.get('X')
        print("Data Gathered, Rendering Vehicle")

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
        window_height = 1000
        window_width = 1000

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
        #glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)
        # glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        # glEnable(GL_COLOR_MATERIAL)
        # glEnable(GL_DEPTH_TEST)

        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH) # OPTION 1 - filled in plane model
        #glShadeModel(GL_LINES) # OPTION 2 - wirefrace model (not working rn, maybe just trun all the quads to lines..? no)
        glMatrixMode(GL_PROJECTION)

        #glLoadIdentity()
        gluPerspective(45.0, window_width / window_height, 0.1, 7000.0)
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

        red = (1,0,0)
        blue = (0,0,1)
        green = (0,1,0)
        yellow = (1,1,0)
        purple = (1,0,1)
        cyan = (0,1,1)

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
        # self.displayVertices((v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,v21,v22))
        #self.printVertices((v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,v21,v22))


        # Render Body
        n1 = self.renderQuad(v1,v2,v3,v4,        brown_light, True) # face 11
        n2 = self.renderQuad(v1,v2,v6,v5,        brown_light, True) # face 13
        n3 = self.renderQuad(v2,v3,v7,v6,        brown_light, True) # face 10
        n4 = self.renderQuad(v3,v4,v8,v7,        brown_light, True) # face 12
        n5 = self.renderQuad(v6, v7, v10, v9,    brown_light, True)  # face 9
        n6 = self.renderQuad(v9, v10, v12, v11,  near_black, True)  # face 8
        n7 = self.renderQuad(v11, v12, v14, v13, brown_light, True)  # face 1
        n8 = self.renderQuad(v13, v14, v16, v15, near_black, True)  # face 2
        n9 = self.renderQuad(v16, v15, v17, v18, brown_light, True)  # face 3
        n10= self.renderQuad(v10, v12, v14, v16, near_black, True)  # face 4
        n11= self.renderQuad(v8, v7, v16, v18,   brown_light, True)  # face 5
        n12= self.renderQuad(v5, v6, v15, v17,   brown_light, True)  # face 7
        n13= self.renderQuad(v9, v11, v13, v15,  near_black, True)  # face 6
        n14= self.renderQuad(v5, v8, v18, v17,   brown_light, True)  # face 14
        #self.renderQuad(v3, v4, v8, v7)  # face 15

        # Render 4 Tires
        self.renderCylinder(gray_dark, [v19[0],v19[1],v19[2]],      tire_radius, tire_width)
        self.renderCylinder(gray_dark, [v20[0],v20[1],v20[2]],      tire_radius, tire_width)
        self.renderCylinder(gray_dark, [v21[0],v21[1],v21[2]],      tire_radius, tire_width)
        self.renderCylinder(gray_dark, [v22[0],v22[1],v22[2]],      tire_radius, tire_width)

        #Render Ground Plane
        self.renderGroundPlane(anchor, ow, ol)
        self.renderBackground()

        #Mimicking an Annotated Point Cloud
        annotated_point_cloud = self.getAnnotatedPointCloud((400,0,0))
        #Output of the ICP formula
        #transformed_points = self.example_transformed()

        transformed_points2 = self.example_transformed2()

        #self.renderRandomAnnotatedPointCloud( (0,0,0) , red, (v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18))
        self.renderRandomAnnotatedPointCloud( (0,0,0), green, annotated_point_cloud)
        #self.renderRandomAnnotatedPointCloud( (0,0,0), blue, transformed_points)
        self.renderRandomAnnotatedPointCloud( (0,0,0), cyan, transformed_points2)


        # print("annotated point cloud")
        # for p in annotated_point_cloud:
        #     print(str(p[0])+" "+str(p[1])+" "+str(p[2]))
        #
        # n = (n1,n3, n5,n6,n7,n8,n9)
        # print("points and normals")
        # for np in n:
        #     print(str(np[0])+" "+str(np[1])+" "+str(np[2])+" "+str(np[3])+" "+str(np[4])+" "+str(np[5]))
        # # temporary code for front right tire
        # print(str(v20[0])+" "+str(v20[1])+" "+str(v20[2])+" -1.0 0.0 0.0" )
        # print(str(v19[0])+" "+str(v19[1])+" "+str(v19[2])+" 1.0 0.0 0.0" )

        # the final flush before each new frame
        glFlush()

    # ------------------------ Modeling Functions ------------------------------------
    def example_transformed(self):

        p1 = (254.3542673487756, 42.67290433167794, -0.44380498792993106)
        p2 = (255.3874971870351, 114.64929265857823, 1.0832704904211523)
        p3 = (358.8399538630042, 112.3725333535903, 38.398221579413715)
        p4 = (357.80672402474494, 40.39614502668998, 36.87114610106257)
        p5 = (228.55292115733914, 133.9387477269009, -41.25846367899658)
        p6 = (407.24352814310356, 130.00616347283082, 23.19463365653609)
        p7 = (270.6576878198879, 135.80852977512737, -157.87618334193812)
        p8 = (449.34829480565276, 131.8759455210572, -93.42308600640563)
        p9 = (334.9247293586584, 171.13021374033917, -215.9806239098986)
        p10 = (438.3771860346277, 168.8534544353513, -178.66567282090602)
        p11 = (426.43468593573056, 175.19397391773475, -469.43607108056614)
        p12 = (529.8871426117001, 172.91721461274673, -432.1211199915734)
        p13 = (401.3861972157051, 141.61390145712068, -519.9553935857491)
        p14 = (580.0768042014695, 137.68131720305055, -455.5022962502161)
        p15 = (400.09465991788124, 51.64341604849545, -521.8642379336881)

        points = (p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15)

        return points

    def example_transformed2(self):

        p1 = (39.36990187005112, 69.31848315670558, -24.777673256403467)
        p2 = (39.319052319241564, 141.2514661328648, -21.67229494212815)
        p3 = (149.26403908636723, 141.17905109467384, -18.194559926515996)
        p4 = (149.31488863717675, 69.24606811851463, -21.299938240791366)
        p5 = (0.30640164029253203, 160.5981060053039, -53.11622301494445)
        p6 = (190.2113787835096, 160.47302548479226, -47.10922616979616)
        p7 = (4.2266292274886, 165.9463515542596, -176.93878996141294)
        p8 = (194.13160637070564, 165.821271033748, -170.93179311626466)
        p9 = (46.61624075658513, 204.2085290550282, -251.05441994127588)
        p10 = (156.56122752371076, 204.13611401683727, -247.5766849256638)
        p11 = (55.13641281101533, 215.83233692150858, -520.168789232189)
        p12 = (165.081399578141, 215.7599218833177, -516.691054216577)
        p13 = (16.398303590960325, 182.5517913635174, -561.3878889484319)
        p14 = (206.30328073417735, 182.42671084300574, -555.3808921032835)
        p15 = (16.4618655294723, 92.63556264331844, -565.2696118412758)
        p16 = (206.3668426726893, 92.51048212280678, -559.2626149961278)
        p17 = (17.245387446131467, 48.2400020441176, -116.51754188227436)

        points = (p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17)

        return points


    def renderRandomAnnotatedPointCloud(self, translation, color, vertices):
        # points below chosen by hand mimicking annotation
        # point
        glEnable(GL_POINT_SMOOTH)
        glPointSize(20)
        glBegin(GL_POINTS)
        glColor3fv(color)
        for p in vertices:
            glVertex3d(translation[0] + p[0],translation[1] + p[1], translation[2] + p[2])
        glEnd()


    def renderBackground(self):
        #currently hardcoded
        right = -2000
        left = 2000
        front = -3000
        behind = 3000
        tall = 3000

        blue = (0,0.5,0.5)

        self.renderQuad( (left,0,behind), (left,0,front), (left,tall,front), (left,tall,behind), blue, False) #left
        self.renderQuad( (right,0,behind), (right,0,front), (right,tall,front), (right,tall,behind), blue, False) #right
        self.renderQuad( (right,0,behind), (right,tall,behind), (left,tall,behind), (left,0,behind), blue, False ) #behind
        self.renderQuad( (right, 0,front), (right, tall, front), (left, tall, front), (left, 0, front),blue, False) #front

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
        zLength = xLength*1.5
        xStart = overall_width/2 - xLength/2
        zStart = - overall_length/2 - zLength/2
        xSharpness = 50
        zSharpness = (int)(xSharpness*1.5)
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
                self.renderQuad(v1,v2,v3,v4,color,False) #the false prevents normals from being created for each


# This method makes a quad plane given 4 vertices and a color
# Its purpose is to shorten the length of the code although glBegin and glEnd repeatedly may not be efficient
    def renderQuad(self, v1, v2, v3, v4, color, addNormal):
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_QUADS)
        glColor3f(color[0],color[1],color[2])
        glVertex3f(v1[0],v1[1],v1[2])
        glVertex3f(v2[0],v2[1],v2[2])
        glVertex3f(v3[0],v3[1],v3[2])
        glVertex3f(v4[0],v4[1],v4[2])
        glEnd()

        if (addNormal):

            #midpoint
            x = (v1[0] + v2[0] + v3[0] + v4[0]) / 4
            y = (v1[1] + v2[1] + v3[1] + v4[1]) / 4
            z = (v1[2] + v2[2] + v3[2] + v4[2]) / 4

            # Normal (by taking cross product of v1-v2 and v1-v4)
            u = (v2[0]-v1[0], v2[1]-v1[1], v2[2]-v1[2])
            v = (v4[0]-v1[0], v4[1]-v1[1], v4[2]-v1[2])

            normalX = u[1]*v[2] - u[2]*v[1]
            normalY = -u[0]*v[2] + u[2]*v[0]
            normalZ = u[0]*v[1] - u[1]*v[0]

            magnitude = np.sqrt(normalX*normalX + normalY*normalY + normalZ*normalZ)

            scale = 30 #length of the normal vectors
            normal = (normalX*scale/magnitude,normalY*scale/magnitude,normalZ*scale/magnitude)

            # uncomment to print xyz data 14x6 matrix of xyz points and xyz for normal vectors (the plane information in point to plane icp)
            # print(str(x) + "," + str(y)  + "," + str(z) + "," + str(normal[0]) + "," + str(normal[1]) + "," + str(normal[2]))

            # below is the same data as above, just a bit more readable
            # print("X:" + str(x) + ", Y:" + str(y)  + ", Z:" + str(z) + ", Normals: " + str(normal[0]) + ", " + str(normal[1]) + ", " + str(normal[2]))

            #draw normal line
            glEnable(GL_LINE_SMOOTH)
            glLineWidth(3)
            glBegin(GL_LINES)
            glColor3f(0.0,0.0,1.0)
            glVertex3f(x+normal[0], y+normal[1], z+normal[2])
            glVertex3f(x-normal[0], y-normal[1], z-normal[2])
            glEnd()

            return (x,y,z,normal[0]/scale,normal[1]/scale,normal[2]/scale)
            # point
            # glEnable(GL_POINT_SMOOTH)
            # glPointSize(20)
            # glBegin(GL_POINTS)
            # glColor3fv((0, 1, 0))
            # glVertex3d(x,y,z)
            # glVertex3d(x+normal[0], y+normal[1], z+normal[2])
            # glVertex3d(x-normal[0], y-normal[1], z-normal[2])
            # glEnd()
        # glFlush()

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
            self.setXRotation(dy) #disable vertical rotation
            self.setYRotation(dx)
            # print("ROTATE: " + "x = " + str(self.rotX) + "y = " + str(self.rotY) + "z = " + str(self.rotZ))
        elif event.buttons() == QtCore.Qt.RightButton:
            self.setZTranslation(dx*5)
            # print("ZOOM: " + "zoom = " + str(self.rotZ) + " -> + " + str(dx))
        self.lastPos = QtCore.QPoint(event.pos())

    def keyPressEvent(self, event):
        movement_speed = 5
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

        elif event.key() == QtCore.Qt.Key.Key_X:
            self.setXRotation(5)
        elif event.key() == QtCore.Qt.Key.Key_Y:
            self.setYRotation(5)
        elif event.key() == QtCore.Qt.Key.Key_Z:
            self.setZRotation(5)

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
        glPointSize(5)
        glBegin(GL_POINTS)
        glColor3fv((1, 0, 0))
        for v in vertices:
            glVertex3d(v[0],v[1],v[2])
        glEnd()

    def getAnnotatedPointCloud(self, anchor):
        # Mercedes S Class Sedan
        # ow = 190; ol = 529; oh = 150; a = 155; c = 36; d = 87; e = 114; f = 91; g = 113; twf = 160

        ow = 190.0
        ol = 540.0
        oh = 150.0
        a = 155.0
        c = 35.0
        d = 90.0
        e = 110.0
        f = 90.0
        g = 115.0
        twf = 160.0

        v1 = (anchor[0] + (ow - e) / 2, anchor[1] + (oh - c - d), anchor[2])
        v2 = (anchor[0] + (ow - e) / 2, anchor[1] + (oh - c - d * (1 / 5)), anchor[2])
        v3 = (anchor[0] + ow - (ow - e) / 2, anchor[1] + (oh - c - d * (1 / 5)), anchor[2])
        v4 = (anchor[0] + ow - (ow - e) / 2, anchor[1] + (oh - c - d), anchor[2])
        #v5 = (anchor[0], anchor[1] + (oh - c - d), anchor[2] - a * (1 / 5))
        v6 = (anchor[0], anchor[1] + (oh - c), anchor[2] - a * (1 / 5))
        v7 = (anchor[0] + ow, anchor[1] + (oh - c), anchor[2] - a * (1 / 5))
        #v8 = (anchor[0] + ow, anchor[1] + (oh - c - d), anchor[2] - a * (1 / 5))
        v9 = (anchor[0], anchor[1] + (oh - c), anchor[2] - a)
        v10 = (anchor[0] + ow, anchor[1] + (oh - c), anchor[2] - a)
        v11 = (anchor[0] + (ow - e) / 2, anchor[1] + oh, anchor[2] - a - (ol - a) * (2 / 10))
        v12 = (anchor[0] + ow - (ow - e) / 2, anchor[1] + oh, anchor[2] - a - (ol - a) * (2 / 10))
        v13 = (anchor[0] + (ow - e) / 2, anchor[1] + oh, anchor[2] - (ol - (ol - a) * (1 / 10)))
        v14 = (anchor[0] + ow - (ow - e) / 2, anchor[1] + oh, anchor[2] - (ol - (ol - a) * (1 / 10)))
        v15 = (anchor[0], anchor[1] + (oh - c), anchor[2] - ol)
        v16 = (anchor[0] + ow, anchor[1] + (oh - c), anchor[2] - ol)
        v17 = (anchor[0], anchor[1] + (oh - c - d), anchor[2] - ol)
        v18 = (anchor[0] + ow, anchor[1] + (oh - c - d), anchor[2] - ol)
        # tire, front right
        tfr = (anchor[0] + ((ow-twf)/2), anchor[1], anchor[2]-f)
        #tire, fron left
        tfl = (anchor[0] + (ow-(ow-twf)/2), anchor[1], anchor[2]-f)

        u = (v1,v2,v3,v4,v6,v7,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,tfr,tfl)
        v = ()
        v_list = list(v)
        # essentially rotating 90 degress about z axis
        for point in u:
            v_list.append((-point[2], point[1], point[0]))
        v = tuple(v_list)

        return v

    def icp_point_to_plane(self, source_points, dest_points, loop):
        """
        Point to plane matching using least squares

        source_points:  nx3 matrix of n 3D points
        dest_points: nx6 matrix of n 3D points + 3 normal vectors, which have been obtained by some rigid deformation of 'source_points'
        """

        A = []
        b = []

        for i in range(0, dest_points.shape[0] - 1):
            # print dest_points[i][3],dest_points[i][4],dest_points[i][5]
            dx = dest_points[i][0]
            dy = dest_points[i][1]
            dz = dest_points[i][2]
            nx = dest_points[i][3]
            ny = dest_points[i][4]
            nz = dest_points[i][5]

            sx = source_points[i][0]
            sy = source_points[i][1]
            sz = source_points[i][2]

            # seems like the cross product is happening here...why?
            _a1 = (nz * sy) - (ny * sz)
            _a2 = (nx * sz) - (nz * sx)
            _a3 = (ny * sx) - (nx * sy)

            # creates a 1x6 array, of cross product values and normal values
            _a = np.array([_a1, _a2, _a3, nx, ny, nz])

            # i dont know what this is, perhaps its the formula to minimize
            _b = (nx * dx) + (ny * dy) + (nz * dz) - (nx * sx) - (ny * sy) - (nz * sz)

            # here we append the relation of each source point to destination point
            A.append(_a)
            b.append(_b)

        # the loop ends having gone through all 510 points and created A and B
        # A is a 510 by 6 matrix
        # B is a 510 by 1 vector

        A1 = np.array(A)
        b1 = np.array(b)
        # made them into arrays again?...perhaps there was some formatting issue

        # computes the calculates the generalized inverse of a matrix using SVD
        A_ = np.linalg.pinv(A1)

        # computes the dot product of two arrays
        # since A in a N-D array and B is a 1D array, it is a sum product over the last axis of A and B
        tr = np.dot(A_, b)
        # tr seems to be the translation matrix and R seems to be the rotation matrix

        # print(str(tr[0])+','+str(tr[1])+','+str(tr[2])+','+str(tr[3])+','+str(tr[4])+','+str(tr[5]))

        R = transform.euler_matrix(tr[0], tr[1], tr[2])
        # Return homogeneous rotation matrix from Euler angles and axis sequence.

        R[0, 3] = tr[3]
        R[1, 3] = tr[4]
        R[2, 3] = tr[5]
        # it seams like we are creating a 3by4 matrix, where the 3by3 is R above and the 4th column is the 3 values in tr

        source_transformed = []

        # loop goes from 0 to 509
        for i in range(0, dest_points.shape[0] - 1):
            # getting the values of the source points and putting in a 4th value of 1 so its a 4by1 matrix
            ss = np.array([(source_points[i][0]), (source_points[i][1]), (source_points[i][2]), (1)])
            # applying the transformation contained in R to the source point, output maybe 4by1 or 3by1
            p = np.dot(R, ss)
            source_transformed.append(p)

        source_points = np.array(source_transformed)

        loop = loop + 1

        if (loop < 3):  # although this should converge in one step (which it does), you might want to reiterate over and over, just for the fun of it!
            return self.icp_point_to_plane(source_points, dest_points, loop)
        else:
            return source_points


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
