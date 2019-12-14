#Loads the problem written in file f 
import numpy
import itertools
import probability as p
T, F = True, False

class Problem:
    def __init__(self, fh):
        self.propagationP = 0
        self.museum = []
        self.rooms = []
        self.sensors = {}
        self.measurements = []
        self.load(fh)
        self.net = None
    
    def solve(self, teste):

        (obs, time)=self.createNet()

        maxi=('',0)
        for room in self.rooms:
            if(teste):
                a=p.elimination_ask(time+':'+room.name, obs, self.net).show_approx( numfmt='{:.16g}')
            else:
                a=p.enumeration_ask(time+':'+room.name, obs, self.net).show_approx( numfmt='{:.16g}')

            P=a.split('True: ')
            if( float(P[1])>maxi[1] ):
                maxi = (room.name, float(P[1]))

        return maxi

    def createNet(self):
        firstNodes = []
        for room in self.rooms:
            firstNodes.append( ("0:"+room.name, '', 0.5) )
        
        self.net = p.BayesNet(firstNodes)

        obs={}
        for m in self.measurements:
            
            for k in range(len(self.rooms)):
                count = 0
                parents = ''
                dic= {}
                autoprob = 0
                for j in range(len(self.rooms)):
                    if(self.museum[k][j] == 1):
                        parents = parents + str(m.time-1) + ":" + self.rooms[j].name + " "
                        count = count + 1
                        if(k==j):
                            autoprob= count-1

                if(count==0):
                    dic=0.5
                elif count==1:
                    dic = {T: 1, F:0}
                else:
                    combinations = list(itertools.product( (F,T) , repeat=count))
                
                    for x in range(len(combinations)):
                        if x==0:
                            dic[combinations[x]]=0
                        elif  combinations[x][autoprob] :
                            dic[combinations[x]]=1
                        else:
                            dic[combinations[x]]=self.propagationP
                a=(str(m.time) + ":" + self.rooms[k].name, parents, dic)
                self.net.add( a ) 
                
            k=0
            for sensor in m.sensors:
                self.net.add( (str(m.time) + ":" + self.sensors[sensor].sensorID, str(m.time-1)+':'+ self.rooms[self.sensors[sensor].roomID].name, {T: self.sensors[sensor].tpr , F: self.sensors[sensor].fpr}) ) 
                obs[str(m.time) + ":" + self.sensors[sensor].sensorID]=m.states[k]
                k=k+1

        return (obs, str(m.time-1) )


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
        for k in range(nRooms):
            self.museum[k][k]=1

        for room in R:
            if(room != "R"):
                self.rooms.append( Room(room) )

        #Legs
        for line in C:
            for aux in line:
                if(aux != "C"):
                    connection = aux.split(",")

                    for k in range(len(self.rooms)):
                        if(self.rooms[k].name == connection[0]):
                            a=k
                        elif(self.rooms[k].name == connection[1]):
                            b=k

                    self.museum[a,b] = 1
                    self.museum[b,a] = 1
        
        for s in S:
            for sensor in s:
                if(sensor != "S"):
                    info = sensor.split(":")

                    for k in range(len(self.rooms)):
                            if(self.rooms[k].name == info[1]):
                                self.sensors[info[0]]=( Sensor( info[0], k, float(info[2]), float(info[3]) ) ) 
                                self.rooms[k].connectSensor( int(info[0][1]) )

        time = 1
        for s in M:
            m = Measurement( time )
            self.measurements.append( m )
            for aux in s:
                if(aux != "M"):
                    info = aux.split(":")
                    m.addSensor(info[0] , info[1])
            time = time +1

        a=1

def solver(input_file):
    return Problem(input_file,None).solve()

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
        self.sensors = [] #strings
        self.states = [] #boolean
        self.time = time #int

    def addSensor(self, sensor, state):
        self.sensors.append(sensor)

        if(state == "T"):
            self.states.append(True)
        if(state == "F"):
            self.states.append(False)


""" The modeled Network has several layers. Each one of this layers corresponds to a time instant in which a measurement of one or more sensors was taken. From now on the notation n:NAME will be used to reference the net's node where the room or sensor with name NAME that is responsible for generating said node in the time instant n.

The first layer contains the inicial conditions of each room, since there is not information about them, it is considered that the room has an equal probability of being, or not, on fire ( P(0:Ri)=0.5 ). This layer also has the first taken measurements which are a child node of the attached room's node with the following CPD: P( 0:Sj=True | 0:Ri = Fire)= TPR, P( 0:Sj=True ! 0:Ri = Not Fire) = FPR.

The N'th layer of the Bayesian Network contains nodes for each of the museums' rooms, corresponding to the Measurement taken in time instant N, which are child nodes of them rooms in layer N-1 that are physically connected to the room in layer N-1, as well as the node that corresponds to the same room in layer N-1 with the following CPD rules:

if Obs=All parent rooms and the room in layer N-1 are not on fire : P(N:Ri | Obs) = 0

if Obs= 1 or more parent rooms are on fire and the room in layer N-1 is not on fire: P(N:Ri | Obs) = P

if Obs= The room in layer N-1 is on fire: P(N:Ri | Obs) = 1

( P(N:Ri | Obs)=1 room Ri is on fire in time instant N )

The sensors read in the time instant N are also child nodes of the rooms they are connected to with the CPD showcased in the first layer.

Therefore, the Bayesian Network as a total of N*Nrooms + S nodes, where N is the number of measurements taken, Nrooms is the number of rooms in the museum and S is the number of sensor readings in all measurements. 

To solve the problem, the Variable elimination algorithm is used to compute each room's probability to be on fire in the last time instant, given the set of sensor readings, i.e P(N:Ri | 0:S1= T/F, ... , N:Sk=T/F) where k is the number of sensors.
 """