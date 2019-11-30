#Loads the problem written in file f 
import numpy
import probability as p
T, F = True, False


class Problem:
    def __init__(self, fh):
        self.propagationP = 0
        self.museum = []
        self.rooms = []
        self.sensors = []
        self.measurements = []
        self.load(fh)
    
    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference
        # burglary = p.BayesNet([
        # ('Burglary', '', 0.001),
        # ('Earthquake', '', 0.002),
        # ('Alarm', 'Burglary Earthquake',
        # {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001}),
        # ('JohnCalls', 'Alarm', {T: 0.90, F: 0.05}),
        # ('MaryCalls', 'Alarm', {T: 0.70, F: 0.01})])
        firstNodes = []
        for room in rooms:
            firstNodes.append( ("0:"+room, '', 0.5) )
        
        n = p.BayesNet(firstNodes)

        for m in self.measurements:
            for sensor in m.sensors:
                n.add( (m.time + ":" + self.sensors[m.sensorID].name, '', 0.5) ) 
            for k in range(len(self.rooms)):
                parents = ''
                for j in range(len(self.rooms)):
                    if(self.museum[k][j] == 1):
                        parents = parents + " " + m.time-1 + self.rooms.name

                n.add( m.time + ":" + self.rooms[k].name, parents, ) 

        a = p.elimination_ask()
        #return (room, likelihood)


    def load(self, f):

        R = []
        C = []
        S = []
        P = []
        M = []
        
        #Reads all the file lines
        for line in f:
            #Saves the file info to be processed in ordder
            line = line.strip()
            s=line.split(" ")
            if(s[0]== "R"):
                R=s
            elif(s[0] == "C"):
                C.append(s)
            elif(s[0] == "P"):
                self.propagationP = float(s[1])
            elif(s[0] == "S"):
                S.append(s)
            elif(s[0] == "M"):
                M.append(s)
        #Rooms 
        nRooms = len(R) - 1
        self.museum = numpy.zeros((nRooms,nRooms))      
        for room in R:
            if(room != "R"):
                self.rooms.append( Room(room) )

        #Legs
        for line in C:
            for aux in line:
                if(aux != "C"):
                    connection = aux.split(",")

                    for k in range(len(self.rooms)):
                        print(connection[0] , connection[1], self.rooms[k])
                        if(self.rooms[k] == connection[0]):
                            a=k
                        elif(self.rooms[k] == connection[1]):
                            b=k

                    self.museum[a,b] = 1
                    self.museum[b,a] = 1
        
        for s in S:
            for sensor in s:
                if(sensor != "S"):
                    info = sensor.split(":")

                    for k in range(len(self.rooms)):
                            if(self.rooms[k] == info[1]):
                                self.sensors.append( Sensor( info[0], k, float(info[2]), float(info[3]) ) ) 
                                self.rooms[k].connectSensor( int(info[0][1]) )

        time = 1
        for s in M:
            m = Measurement( time )
            self.measurements.append( m )
            for aux in s:
                if(aux != "M"):
                    info = aux.split(":")
                    m.addSensor(int(info[0][1]) , info[1])

def solver(input_file):
    return Problem(input_file).solve()

class Room:

    def __init__(self, name):
        self.name = name #string
        self.sensorID = -1 #int
    
    def connectSensor(self, sensorID):
        self.sensorID = sensorID 

class Sensor:

    def __init__(self, sensorID, roomID, tpr, fpr):
        self.sensorID = sensorID #string
        self.roomID = roomID #int 
        self.tpr = tpr #float
        self.fpr = fpr #float

class Measurement:

    def __init__(self, time):
        self.sensors = [] #sensors
        self.states = [] #boolean
        self.time = time #int

    def addSensor(self, sensor, state):
        self.sensors.append(sensor)

        if(state == "T"):
            self.states.append(True)
        if(state == "F"):
            self.states.append(False)


