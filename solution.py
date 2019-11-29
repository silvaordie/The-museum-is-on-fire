#Loads the problem written in file f 
import numpy

class Problem:
    def __init__(self, fh):
        self.propagationP = 0
        self.museum = []
        self.rooms = []
        self.sensors = []
        self.measurements = []
        self.load(fh)
    
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
                R.append(s)
            elif(s[0] == "C"):
                C.append(s)
            elif(s[0] == "P"):
                self.propagationP = float(s[1])
            elif(s[0] == "S"):
                S.append(s)
            elif(s[0] == "M"):
                M.append(s)
        #Rooms       
        for rooms in R:
            nRooms = len(rooms) - 1

            self.museum = numpy.zeros((nRooms,nRooms))

            for room in rooms:
                self.rooms.append(room)

        #Legs
        for aux in C:
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
            sens = s.split(" ")
            for sensor in sens:
                info = sensor.split(":")

                for k in range(len(self.rooms)):
                        if(self.rooms[k] == info[1]):
                            self.sensors.append( Sensor( info[0], k, float(info[3]), float(info[4]) ) ) 

        time = 1
        for s in M:
            m = self.measurements.append( Measurement( time ) )
            temp = s.split(" ")
            for aux in temp:
                info = aux.split(":")
                m.addSensor(int(info[0][1]) , info[1])


class Sensor:

    def __innit__(self, sensorID, roomID, tpr, fpr):
        self.sensorID = sensorID
        self.roomID = roomID
        self.tpr = tpr 
        self.fpr = fpr 

class Measurement:

    def __innit__(self, time):
        self.sensors = []
        self.states = []
        self.time = time

    def addSensor(self, sensor, state):
        self.sensors.append(sensor)

        if(state == "T"):
            self.states.append(True)
        if(state == "F"):
            self.states.append(False)


