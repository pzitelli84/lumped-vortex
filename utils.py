import numpy as np

# node class definition
class Node:
    def __init__(self, coord, name):
        self.coord = coord
        self.id = name

# panel class definition
class Panel:
    def __init__(self, nodes, name):
        self.velInd = []
        self.nodes = nodes
        self.id = name

        # tangent unit vector and panel length
        tVec = self.nodes[1].coord - self.nodes[0].coord
        self.len = np.linalg.norm(tVec)
        self.t = tVec/self.len

        # normal unit vector
        kVersor = np.array([0.0, 0.0, 1.0])
        nVec = np.cross(kVersor, self.t)
        nMag = np.linalg.norm(nVec)
        self.n = nVec/nMag

        # quarter chord point coordinates
        self.qPoint = self.nodes[0].coord + 0.25*tVec

        # collocation point coordinates
        self.cPoint = self.nodes[0].coord + 0.75*tVec

        # midpoint coordinates
        self.mPoint = self.nodes[0].coord + 0.5*tVec

    def velIndCalc(self, quarterPoint):
        vector =  self.cPoint - quarterPoint 
        r = np.linalg.norm(vector)
        u = (0.5/(np.pi*r**2))*vector[1]
        v = - (0.5/(np.pi*r**2))*vector[0]
        self.velInd.append(np.array([u, v, 0.0]))

    def setGamma(self, gamma):
        self.gamma = gamma

    def dCpCalc(self, velInf):
        self.dCp = 2*self.gamma/(velInf*self.len)

# airfoil class definition
class Airfoil:
    def __init__(self, coordFile):
        self.panels = []

        # nodes coordinates reading
        nodesFile = np.loadtxt(coordFile)

        # nodes creation
        nodes = []
        count = 1
        for i in nodesFile:
            nodes.append(Node(np.array([i[0], i[1], 0.0]), count))
            count = count + 1

        # panels creation
        for i in range(len(nodes)-1):
            self.panels.append(Panel([nodes[i], nodes[i+1]], i+1))

        self.panelNum = len(self.panels)

        # chord calculation
        cVec = self.panels[-1].nodes[1].coord - self.panels[0].nodes[0].coord
        self.c = np.linalg.norm(cVec) 

    # aerodynamic characteristics: Gamma, L and Cl
    def liftCalc(self, vInf):
        self.Gamma = 0.0
        for p in self.panels:
            self.Gamma = self.Gamma + p.gamma

        self.L = 1.2*vInf*self.Gamma
        self.Cl = 2.0*self.L/(1.2*vInf**2*self.c)
        
# write results to file and terminal
def writeResults(airfoils):
    with open('results.dat', 'w') as out:
        print(40*'=' + '\n')
        out.write(40*'=' + '\n')

        for a in airfoils:
            print('Airfoil #{0:d} aerodynamic characteristics:'.format(list(airfoils).index(a)+1))
            print('Gamma = {0:.4f} m2/s'.format(a.Gamma))
            print('L = {0:.4f} N/m'.format(a.L))
            print('Cl = {0:.4f}\n'.format(a.Cl))
            print(40*'=' + '\n')
            
            out.write('Airfoil #{0:d} aerodynamic characteristics:'.format(list(airfoils).index(a)+1))
            out.write('Gamma = {0:.4f} m2/s'.format(a.Gamma))
            out.write('L = {0:.4f} N/m'.format(a.L))
            out.write('Cl = {0:.4f}\n'.format(a.Cl))
            out.write(40*'=' + '\n')
