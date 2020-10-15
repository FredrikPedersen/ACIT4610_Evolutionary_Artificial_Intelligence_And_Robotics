import pycxsimulator
from pylab import *
import csv
import networkx as nx
from math import sin, cos, sqrt, atan2
import random

"""
Functions that can be used when working with probabilities 
,computing distances and data normalization.
Examples include haversine,linear,inversed logarithmic
functions.
"""
class UsefulMathematicalFunctions:

    """
    Mapping the user distance to [0,1] range.
    The closer 2 people live,the more it should influence the chances
    of getting the virus.This will be a linear normalizer.

    Parameters:
        :param max_dist:The maximum observed distance.
        :param min_dist:The minimum observed distance.
        :param dist:The given distance.

    Returns:
        :returns The user distance mapped to [0,1] range.
    """

    @staticmethod
    def distance_linear_normalizer(max_dist,min_dist,dist):
        if dist == min_dist:
            return 1.0
        return ( max_dist - dist ) / ( dist - min_dist )

    """
    Calculates the haversine distance between 2 locations.
    
    Parameters:
        :param coord1:The coordinates of the first person (latitude,longitude).
        :param coord2:The coordinates of the second person (latitude,longitude).
        
    Returns:
        :returns The distance between 2 people expressed in km.
    """

    @staticmethod
    def calculate_distance_haversine(coord1,coord2):
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

    """
    Calculate a possible recovery probability for each person.
    Here I'm assuming that time passing affects the person recovery chances on
    a logarithmical scale.

    Parameters:
        :param current_time:The step number in the current simulation.
        :param infection_time:The step number when the person got infected.

    Returns:
        :returns A probability that a person recovers.
    """

    @staticmethod
    def recovery_probability_with_inverse_logarithmic(current_time,infection_time):
        return 1 - 2 / math.log( current_time + 1.73 - infection_time)

    """
    Calculates a possible recovery probability for each person.
    Here I'm assuming that time passing affects the person recovery chances on
    a linear scale.

    Parameters:
        :param current_time:The step number in the current simulation.
        :param infection_time:The step number when the person got infected.
        The following condition always holds: current_time - infection_time >= 1,
        so no need to worry about division by 0.
        
    Returns:
        :returns A probability that a person recovers.
    """

    @staticmethod
    def recovery_probability_with_inverse_linear(current_time, infection_time):
        return 1 - 1 / (current_time - infection_time)

    """
    Calculates a possible recovery probability for each person.
    Here I'm assuming that time passing does not affect someone's recover.

    Parameters:
        :param current_time:The step number in the current simulation.
        :param infection_time:The step number when the person got infected.
    
    Returns:
            :returns A constant.
    """

    @staticmethod
    def recovery_probability_with_constant(current_time, infection_time):
        return 0.7

"""
Applying MVC pattern to be easier to create simulations.
This will decouple the graph data structure from the UI.
"""
class GraphController:

    distance_graph = nx.Graph() #the distances between people
    relationships_dynamics_graph = nx.Graph() # as restrictions are applied,dynamics between people change.
    p_i = 0.5  # infection probability
    p_r = 0.1  # recovery probability
    p_s = 0.5  # severance probability
    detection_probability = 0.1  # the probability of detecting the virus.
    quarantined_people = set()
    distances = set() # will contain the distances for data analysis
    time_elapsed = 0
    max_dist = 0
    min_dist = 100
    infected = 0

    """
    It's useful to know how long a person has been infected.
    The probability of recovery should increase the longer that happened.
    I will keep track of the last time a person was infected.
    """
    time_infected = {}

    """
    Create a mapping between people and their coordinates.
    :return: returns a dictionary mapping people's names to their coordinates(latitude,longitude).
    """
    def create_people_mapping_to_coordinates(self):
        people = {}
        with open('people.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            try:
                for row in csv_reader:
                    if line_count == 0 :
                        print(f'Column names are {", ".join(row)}')
                        line_count += 1
                    else:
                        if row[1] and row[2]:
                            people[row[0]] = (row[1], row[2])
                        line_count += 1
            except:
                print("There was a problem while reading the file.")
        return people

    """
    Create the nodes of the graph.
    Since choosing a graph with a very big size can be infeasible,
    it's good to take a sample out of it.
    Further strategies on clustering and making smarter choices can be developed.
            
    Parameters:
            :param people: The people dictionary
            :param size: The size we choose for our simulation
    """
    def create_nodes(self,people,size = 10):
        for person, coordinates in random.sample(list(people.items()), size):
            self.relationships_dynamics_graph.add_node(person)
            self.distance_graph.add_node(person)

    """
    It can be helpful to take into equation how much the distance between people
    influences the spread of the virus.So I will create a weighted graph.
    We will also keep track of the longest and shortest distances for normalization purposes.
    
    Parameters:
            :param people:The people dictionary
    """
    def create_edges(self,people):
        for i in self.relationships_dynamics_graph.nodes:
            for j in self.relationships_dynamics_graph.nodes:
                if i != j:
                    edge_length = UsefulMathematicalFunctions.calculate_distance_haversine(people[i],people[j])
                    self.distances.add(edge_length)
                    self.distance_graph.add_edge(i,j,length = edge_length)
                    self.relationships_dynamics_graph.add_edge(i,j,length = edge_length)
                    if edge_length > self.max_dist:
                        self.max_dist = edge_length
                    if self.min_dist > edge_length:
                        self.min_dist = edge_length
        print("Maximum distance is ",self.max_dist)
        print("Minimum distance is ",self.min_dist)

    """
    Infect people randomly at the beginning of the simulation.
    """
    def infect_random_people(self):
            for person in self.relationships_dynamics_graph.nodes:
                if random.random() < .5:
                    self.relationships_dynamics_graph.nodes[person]['state'] = 1
                    self.infected += 1
                    self.time_infected [person] = 0
                else:
                    self.relationships_dynamics_graph.nodes[person]['state'] = 0
    """
    Initializing the 'world'.
    I will use 2 graphs to keep track of the state.
    One will represent distances between people 
    and the other one will be the updated_graph 
    following measures taken.
    The difference is that when we quarantine a node 
    we will remove all adjacent edges,
    and put them back when the node is 'healed'.
    This is helpful assuming we apply restrictions.
    """
    def initialize(self):
        people = self.create_people_mapping_to_coordinates()
        self.create_nodes(people,100)
        self.create_edges(people)
        self.infect_random_people()

    """
    Update the world based on whether we apply quarantine or not.
    
    Parameters:
    :param apply_quarantine:Indicator whether we are currently applying quarantine measure or not.
    """
    def update_world(self,apply_quarantine):
        a = choice(list(self.relationships_dynamics_graph.nodes))
        all_neighbours = list(self.relationships_dynamics_graph.neighbors(a))
        if self.relationships_dynamics_graph.nodes[a]['state'] == 0:  # if susceptible or recovered
            b = choice(all_neighbours)
            if self.relationships_dynamics_graph.nodes[b]['state'] == 1:  # if neighbor b is infected
                if UsefulMathematicalFunctions.distance_linear_normalizer(self.max_dist, self.min_dist , self.relationships_dynamics_graph[a][b]['length'])  * 3 + random.uniform(0, 1) > 2:
                    print("A person got infected")
                    self.time_infected[a] = self.time_elapsed
                    self.infected += 1
                    self.relationships_dynamics_graph.nodes[a]['state'] = 1
                    if apply_quarantine:
                        # If the person was detected,they should be quarantined.
                        if random.uniform(0, 1) < self.detection_probability:
                            print("A detection occured.Quarantine person")
                            self.quarantined_people.add(a)
                            for person in all_neighbours:
                                self.relationships_dynamics_graph.remove_edge(a, person)
        else:
            '''
            The longer a person has been infected,the higher the probability of recovery.
            '''
            recovery_probability = UsefulMathematicalFunctions.recovery_probability_with_inverse_logarithmic(self.time_elapsed,self.time_infected[a])
            print("Probability of recovery", recovery_probability )
            if random.random() < recovery_probability  :
                self.relationships_dynamics_graph.nodes[a]['state'] = 0
                self.infected -= 1
                if apply_quarantine:
                    if a in self.quarantined_people:
                        print("A quarantined person was healed.Reconnecting to other people.Removal from quarantine.")
                        all_neighbours = list(self.distance_graph.neighbors(a))
                        for person in all_neighbours:
                            if person not in self.quarantined_people:
                                self.relationships_dynamics_graph.add_edge(a, person, length=self.distance_graph[a][person]['length'])
                        self.quarantined_people.remove(a)
                    else:
                        print("A non detected person was healed")
                else:
                    print("A person was healed.")
    """
    Update process is also different.
    We will select a random number to represent people's movements but 
    we will give more weight to the distance between people.
    Not removing the edges means with quarantine.
    """
    def update_assuming_no_quarantine(self):
        if self.infected:
            self.time_elapsed += 1
            self.update_world(False)
        else:
            print("Congrats!Covid was beaten after",self.time_elapsed,"steps")
            time.sleep(1)
    """
    We will assume quarantine is precisely followed.
    We will reconnect a node to its neighbors when it's healed.
    When reconnecting taking into account if the neighbor is 
    also quarantined.
    """
    def update_assuming_quarantine(self):
        if self.infected:
            self.time_elapsed += 1
            self.update_world(True)
        else:
            print("Congrats!Covid was beaten after",self.time_elapsed,"steps")
            self.covid_beaten = True
            time.sleep(1)

class Visualizer:
    graph_controller = GraphController()

    """
    Initialize the world.
    """
    def initialize(self):
        self.graph_controller.initialize()
        self.graph_controller.relationships_dynamics_graph.pos = nx.spring_layout(self.graph_controller.relationships_dynamics_graph)

    """
    Observe the changes in the world.
    """
    def observe(self):
        cla()
        nx.draw(self.graph_controller.relationships_dynamics_graph, cmap=cm.Wistia, vmin=0, vmax=1,
                node_color=[self.graph_controller.relationships_dynamics_graph.nodes[i]['state'] for i in self.graph_controller.relationships_dynamics_graph.nodes],
                pos=self.graph_controller.relationships_dynamics_graph.pos)

    """
    Update the world when we apply quarantine restrictions.
    """
    def update_assuming_quarantine(self):
        self.graph_controller.update_assuming_quarantine()

    """
    Update the world when we don't apply quarantine restrictions.
    """
    def update_assuming_no_quarantine(self):
        self.graph_controller.update_assuming_no_quarantine()

"""
Run the simulations of the world and write some useful information 
from that to the file.
Parameters:
    :param filename: The file to write to.
    :param quarantine: Whether we run a simulation where we quarantine people.
    :param maximum_steps_per_simulation: The maximum "time" allowing the simulation to run.
    :param no_simulations_to_run:The number of different random worlds to experiment.
"""
def run_simulations(
        filename,
        quarantine=False,
        maximum_steps_per_simulation = 1_000_000_000,
        no_simulations_to_run = 100_000
):
    with open(filename, "w") as data_file:
        numbers_steps_each_simulation = []
        no_simulations = 0
        while no_simulations < no_simulations_to_run:
            graph_controller = GraphController()
            graph_controller.initialize()
            while graph_controller.infected and graph_controller.time_elapsed < maximum_steps_per_simulation:
                print("Running simulation number ", no_simulations, "for", filename[:-4])
                if quarantine:
                    graph_controller.update_assuming_quarantine()
                else:
                    graph_controller.update_assuming_no_quarantine()
            numbers_steps_each_simulation.append(graph_controller.time_elapsed)
            no_simulations += 1
        data_file.write(str(numbers_steps_each_simulation))
"""
visualizer = Visualizer()
pycxsimulator.GUI().start(func=[visualizer.initialize, visualizer.observe, visualizer.update_assuming_quarantine])
"""


run_simulations(quarantine=True,
                filename="quarantine.txt",
                maximum_steps_per_simulation=1_000_000_000_000_000_000,
                no_simulations_to_run=1000)

run_simulations(
                filename="non-quarantine.txt",
                maximum_steps_per_simulation=1_000_000_000_000_000_000,
                no_simulations_to_run=1000)