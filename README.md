# The Museum is one fire ! #
The modeled Bayesian Network has several layers. Each one of this layers corresponds to a time instant in which a measurement of one or more sensors was taken. From now on the notation n:NAME will be used to reference a net's node where the room or sensor with name NAME that is responsible for generating said node in the time instant n.

The first layer contains the inicial conditions of each room. Since there is no information about them, it is considered that all the rooms have equal probability of being, or not, on fire ( P(0:Ri)=0.5 ).

A layer n is composed of one node per room and one node per sensor measurement taken in that time instant. The layers are connected by edges from the rooms on n-1 to the adjacents rooms on n, this models the probability of a room being on fire given that previously it was on fire or one of the adjancet rooms were or not on fire.

Each layer has the correspondent(s) sensor(s) measurement(s) taken in that time instant, where the sensor node is a child of the room node, since what is known is the probability of the sensor measurement given the room state. This is modeled by the following CPD: P( 0:Sj=True | 0:Ri = Fire)= TPR, P( 0:Sj=True ! 0:Ri = Not Fire) = FPR.

The modeled Bayesian Network as a total of N*Nrooms + S nodes, where N is the number of measurements taken, Nrooms is the number of rooms in the museum and S is the number of sensor readings.

The n'th layer of the Bayesian Network contains nodes for each of the museums' rooms, corresponding to the Measurement taken in time instant N, which are child nodes of the rooms in layer N-1 that are physically connected to the room in layer N-1, as well as the node that corresponds to the same room in layer N-1, with the following CPD rules:
* if Obs=All parent rooms and the room in layer N-1 are not on fire : P(N:Ri | Obs) = 0
* if Obs= 1 or more parent rooms are on fire and the room in layer N-1 is not on fire: P(N:Ri | Obs) = P
* if Obs= The room in layer N-1 is on fire: P(N:Ri | Obs) = 1
( P(N:Ri | Obs)=1 room Ri is on fire in time instant N )

To solve the problem, the Variable elimination algorithm is used to compute each room's probability to be on fire in the last time instant, given the set of sensor readings, i.e P(N:Ri | 0:S1= T/F, ... , N:Sk=T/F) where k is the number of sensors.
 