# The Museum is on fire ! #
In September 2nd of 2018 a huge fire consumed more than 93% of the National Museum of Brasil collection, built over a period of two centuries. It is believed that the bad condition of the electrical system was the major cause of this tragic event. Moreover, there were plans to reform the fire prevention system, which were not implemented in due time.
This mini-project addresses the problem of fire detection in a museum, taking into account a simple fire propagation model and the uncertainty associated with the fire detectors spread over the building.
The problem is formulated as follows. Let the museum building be modeled by an undirected graph, where the nodes are the rooms, R = {r1, . . . , rN }, and the edges are the doors/stars connecting adjacent rooms, C = {(ri , rj ), . . .} where ri, rj ∈ R. Some of these rooms are equipped with sensors, S = {s1, . . . , sM}, M ≤ N, where the map l : S → R specifies the room covered by each sensor. Each one of these sensors is characterized by two parameters:
TPR — True Positive Rate, also known as hit rate or recall, is the probability of detecting a fire in case of a real fire, and
FPR — False Positive Rate, also known as false alarm rate, is the probability of detecting a fire in case of no fire.
Consider a set of discrete time steps, T = {1, . . . , T}, where for each time step, the output of only a subset of the sensors is known (e.g., due to poor sensor network). Moreover, we consider the following fire propagation law:
if room ri ∈ R is on fire at time step t, it will continue on fire at t + 1;
or else , it will catch fire with probability P at time step t + 1 when any of the adjacent rooms was on fire at t, and 0 otherwise.
Finally, assume that at the first time instant, t = 1, we have absolutely no information (in a probabilistic sense) about which room(s) is(are) on fire.


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

# Enumeration vs Elimination # 

The elapsed time to solve 3 public problems were taken for both Variable Elimination and Enumeration algorithms, and these were the results

* P3_3_2: 3 rooms, no connections between them and 2 Measures taken   
    Elimination: 0.01096s

    Enumeration: 0.11868s
* P3_1_4: 3 rooms 1 connection and 4 Measures    
    Elimination: 0.04687s

    Enumeration: 7.81533s
* P5_1_2: 5 rooms 2 connections and 2 Measures
    Elimination: 0.09028s

    Enumeration: 11.3393s   

It is evident that the variable elimination algorithm is much more efficient and computationaly cheap than the varaible enumeration algorithm. This is due to the fact that the first one uses the Net's architecture, storing intermediate results (factors) to avoid repetition, reducing the number of computed probabilities, where the enumeration algorithm enumerates all the possible probabilities (just like building a tree), including repeated ones.
