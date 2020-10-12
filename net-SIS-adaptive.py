import pycxsimulator
from pylab import *
import csv
import networkx as nx
from math import sin, cos, sqrt, atan2
import random

'''
Create a mapping between people and their coordinates.
:return: returns a dictionary mapping people's names to their coordinates(latitude,longitude).
'''
def create_people_mapping_to_coordinates():
    people = {}
    with open('people.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                try:
                    if row[1] and row[2]:
                        people[row[0]] = (row[1], row[2])
                        line_count += 1
                except:
                    print("Latitude and longitude not present.")
                    pass
    return people

'''
Create the nodes of the graph.
Since choosing a graph with a very big size can be infeasible,
it's good to take a sample out of it.
Further strategies on clustering and making smarter choices can be developed.
:param people: The people dictionary
:param size: The size we choose for our simulation
'''
def create_nodes(people,size = 10):
    global updated_graph
    global distance_graph
    for person, coordinates in random.sample(list(people.items()), size):
        updated_graph.add_node(person)
        distance_graph.add_node(person)
    updated_graph.pos = nx.spring_layout(updated_graph)

'''
It can be helpful to take into equation how much the distance between people
influences the spread of the virus.So I will create a weighted graph.
We will also keep track of the longest and shortest distances for normalization purposes.
:param size: The people dictionary
'''
def create_edges(people):
    global max_dist
    global min_dist
    global updated_graph
    global distance_graph
    max_dist = 0
    min_dist = 100
    for i in updated_graph.nodes:
        for j in updated_graph.nodes:
            if i != j:
                edge_length = calculate_distance(people[i],people[j])
                distance_graph.add_edge(i,j,length = edge_length)
                updated_graph.add_edge(i,j,length = edge_length)
                if edge_length > max_dist:
                    max_dist = edge_length
                if min_dist > edge_length:
                    min_dist = edge_length
    print("Maximum distance is ",max_dist)
    print("Minimum distance is ",min_dist)

def infect_random_people():
    global updated_graph
    for i in updated_graph.nodes:
        updated_graph.nodes[i]['state'] = 1 if random.random() < .5 else 0

'''
Initializing the 'world'.
I will use 2 graphs to keep track of the state.
One will represent distances between people 
and the other one will be the updated_graph 
following measures taken.
The difference is that when we quarantine a node 
we will remove all adjacent edges,
and put them back when the node is 'healed'.
This is helpful assuming we apply restrictions.
'''
def initialize():
    global updated_graph
    global distance_graph
    global quarantined_people
    quarantined_people = set()
    people = create_people_mapping_to_coordinates()
    updated_graph = nx.Graph()
    distance_graph = nx.Graph()
    create_nodes(people,100)
    create_edges(people)
    infect_random_people()

'''
This method will calculate the so-called haversine function.
This is useful to calculate the distance in km,by having the 
latitude and longitude of a person.
:param coord1: The pair of coordinates describing first location
:param coord2: The pair of coordinates describing second location
'''
def calculate_distance(coord1,coord2):
    lat1 = float(coord1[0])
    lon1 = float(coord1[1][:-1])
    lat2 = float(coord2[0])
    lon2 = float(coord2[1][:-1])
    lon1,lat1,lon2,lat2 = map(radians, [lon1, lat1, lon2, lat2])
    R = 6373.0

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def observe():
    global updated_graph
    cla()
    nx.draw(updated_graph, cmap = cm.Wistia, vmin = 0, vmax = 1,
            node_color = [updated_graph.nodes[i]['state'] for i in updated_graph.nodes],
            pos = updated_graph.pos)

detection_probability = 0.3 # detecting an infected person probability.
p_i = 0.5 # infection probability
p_r = 0.1 # recovery probability
p_s = 0.5 # severance probability

"""
Update process is also different.
We will select a random number to represent people's movements but 
we will give more weight to the distance between people.
Not removing the edges means with no quarantine.
"""
def update_assuming_no_quarantine():
    global updated_graph
    global min_dist
    global max_dist

    a = choice(list(updated_graph.nodes))
    if updated_graph.nodes[a]['state'] == 0: # if susceptible
        if updated_graph.degree(a) > 0:
            b = choice(list(updated_graph.neighbors(a)))
            if updated_graph.nodes[b]['state'] == 1: # if neighbor b is infected
                if (updated_graph[a][b]['length'] - min_dist ) / ( max_dist - min_dist ) * 3 + random.uniform( 0, 1 ) > 1 :
                    updated_graph.nodes[a]['state'] = 1
    else:
        if random.uniform(0, 1) < p_r:
            print("A person is healed")
            updated_graph.nodes[a]['state'] = 1

'''
We will assume quarantine is precisely followed.
We will reconnect a node to its neighbors when it's healed.
When reconnecting taking into account if the neighbor is 
also quarantined.
'''
def update_assuming_quarantine():
    global updated_graph
    global distance_graph
    global min_dist
    global max_dist
    global quarantined_people

    a = choice(list(updated_graph.nodes))
    all_people = list(updated_graph.neighbors(a))
    if updated_graph.nodes[a]['state'] == 0:  # if susceptible or recovered
        b = choice(all_people)
        if updated_graph.nodes[b]['state'] == 1:  # if neighbor b is infected
            if (updated_graph[a][b]['length'] - min_dist) / (max_dist - min_dist) * 3 + random.uniform(0, 1) > 1:
                print("A person got infected")
                updated_graph.nodes[a]['state'] = 1
                #If the person was detected,they should be quarantined.
                if random.uniform(0,1) < detection_probability:
                    print("A detection occured.Quarantine person")
                    quarantined_people.add(a)
                    for person in all_people:
                        updated_graph.remove_edge(a,person)
    else:
        '''
        For more realism,probably have to change this condition.
        It's noticeable recoveries taking long when running with few people.
        '''
        if random.random() < p_r:
            updated_graph.nodes[a]['state'] = 0
            if a in quarantined_people:
                print("A quarantined person was healed.Reconnecting to other people.Removal from quarantine.")
                all_people = list(distance_graph.neighbors(a))
                for person in all_people:
                    if person not in quarantined_people:
                        updated_graph.add_edge(a,person,length = distance_graph[a][person]['length'])
                quarantined_people.remove(a)
            else:
                print("A non detected person was healed")

#pycxsimulator.GUI().start(func=[initialize, observe, update_assuming_no_quarantine])
pycxsimulator.GUI().start(func=[initialize, observe, update_assuming_quarantine])