total_population = 400 # Total population

sick_rate = 0.8 # sick rate of healthy people when they face infected

movement_rate = 0.4 # magnitude of movement of people

recovery_time = 20 # recovery time in steps for an infected person 

death_rate = 0.01 # basic death rate constant 

high_risk = 0.35 # amount of the population in the high risk group

face_mask_effectivness = 0.35 # how much does wearing a face mask effect you getting infected


# Collision Detection
cd = 0.04 # radius for collision detection
cdsq = cd ** 2

# Social Distance when starting the simulation and social distancing being ON
social_rad = 0.10 # Social distance radius while setting up
social_distsq = social_rad ** 2


# If the distance to neighbour would be less than this number the agent practicing social distancing will not move
neighbor_distance_rad = 0.06 
neighbor_distance_sq = neighbor_distance_rad ** 2


# PYCX constants
maximum_steps = 150

amount_of_tests = 30