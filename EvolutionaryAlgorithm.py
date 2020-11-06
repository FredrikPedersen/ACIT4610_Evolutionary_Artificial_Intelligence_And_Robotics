from NetworkModel import *

"""
Run more simulations and return the average time taken to beat the disease.
Parameters:
    :param quarantine: Whether we run a simulation where we quarantine people.
    :param maximum_steps_per_simulation: The maximum "time" allowing the simulation to run.
    :param no_simulations_to_run:The number of times to run simulations, on different worlds with same parameters.
    :param infection_probability: The probability that someone starts as infected.
    :param detection_probability: The probability that someone with the disease is detected.
    :param world_size: How big the world in the simulation is
"""
def run_simulation_and_return_time(
        quarantine=False,
        maximum_steps_per_simulation=1_000_000_000,
        no_simulations_to_run=100_000,
        infection_probability=0.5,
        detection_probability=0.1,
        world_size=30
):
    no_simulations = 0
    times = []
    while no_simulations < no_simulations_to_run:
        graph_controller = GraphController()
        graph_controller.set_detection_probability(detection_probability)
        graph_controller.set_infection_probability(infection_probability)
        graph_controller.set_world_size(world_size)
        graph_controller.initialize()
        while graph_controller.no_infected and graph_controller.time_elapsed < maximum_steps_per_simulation:
            if quarantine:
                graph_controller.update_assuming_quarantine()
            else:
                graph_controller.update_assuming_no_quarantine()
        no_simulations += 1
        times.append(graph_controller.time_elapsed)
    return mean(times)


'''
The algorithm will optimize for finding the best detection_probability,as described in the report.
'''
infection_probability = random.random()
detection_probability = random.random()
world_size = random.randint(2, 50)

'''
How many steps to evolve the algorithm.
'''
evolutionary_steps = 50

print("The world_size is ", world_size)
quarantine_winning_scenarios = 0

'''
At each step,3 scenarios will be run,as described in the report.
The average of the time taken to beat the covid will be the criteria 
for assessing how well the model are doing.
Found out,as described in the report,it is needed to run 3000 simulations to have significant results.
'''
for i in range(evolutionary_steps):
    new_detection_probability = random.random()
    print("New tried detection probability", new_detection_probability)
    print("Previous detection probability", detection_probability)
    steps_new_detection_probability_with_quarantine = run_simulation_and_return_time(quarantine = True,
                                                                                        no_simulations_to_run = 3000,
                                                                                        detection_probability = new_detection_probability,
                                                                                        infection_probability = infection_probability,
                                                                                        world_size=world_size
                                                                                        )

    print("With detection probability",new_detection_probability,"and quarantine on average there were made",steps_new_detection_probability_with_quarantine,"steps")
    steps_old_detection_probability_with_quarantine = run_simulation_and_return_time(
                                                                                     quarantine = True ,
                                                                                     no_simulations_to_run = 3000,
                                                                                     detection_probability = detection_probability,
                                                                                     infection_probability = infection_probability,
                                                                                     world_size=world_size)
    print("With detection probability",detection_probability,"and quarantine on average there were made",steps_old_detection_probability_with_quarantine,"steps")
    steps_for_non_quarantine = run_simulation_and_return_time(quarantine = False,
                                                              no_simulations_to_run = 3000,
                                                              detection_probability=detection_probability,
                                                              infection_probability = infection_probability,
                                                              world_size=world_size)
    print("Without quarantine,there were made",steps_for_non_quarantine,"steps")
    min_steps = \
        min([steps_new_detection_probability_with_quarantine,
             steps_old_detection_probability_with_quarantine,
             steps_for_non_quarantine])
    if steps_new_detection_probability_with_quarantine == min_steps:
        quarantine_winning_scenarios += 1
        detection_probability = new_detection_probability
    elif steps_old_detection_probability_with_quarantine == min_steps:
        quarantine_winning_scenarios += 1

print("There were ", quarantine_winning_scenarios, "quarantine winning scenarios and",
      evolutionary_steps - quarantine_winning_scenarios, "winning scenarios without quarantine")
print("The selected detection probability is " , detection_probability )