from NetworkModel import *

"""
Run without visaulizing the graphs.
That allows to improve the scalability of the models.
The parameters of the simulation will be written to a file,
followed by the number of steps taken to eliminate the disease.
Parameters:
    :param filename: The file to write to.
    :param quarantine: Whether we run a simulation where we quarantine people.
    :param maximum_steps_per_simulation: The maximum "time" allowing the simulation to run.
    :param no_simulations_to_run:The number of times to run simulations, on different worlds with same parameters.
    :param infection_probability: The probability that someone starts as infected.
    :param detection_probability: The probability that someone with the disease is detected.
"""
def run_simulations(
        filename,
        quarantine=False,
        maximum_steps_per_simulation = 1_000_000_000,
        no_simulations_to_run = 100_000,
        infection_probability = 0.5,
        detection_probability = 0.1,
        world_size = 30
):
    with open(filename, "w") as data_file:
        no_simulations = 0
        data_file.write("We will run " +
                        str(no_simulations_to_run) +
                        " simulations \n with initial infection probability " +
                        str(infection_probability) +
                        "\n detection probability " +
                        str(detection_probability) +
                        " \n with the world size " +
                        str(world_size) +
                        ". \n"
                        )
        while no_simulations < no_simulations_to_run:
            graph_controller = GraphController()
            graph_controller.set_detection_probability(detection_probability)
            graph_controller.set_infection_probability(infection_probability)
            graph_controller.set_world_size(world_size)
            graph_controller.initialize()
            while graph_controller.no_infected and graph_controller.time_elapsed < maximum_steps_per_simulation:
                print("Running simulation number " + str(no_simulations) + " for " + filename[:-5] + " scenario " + filename[-5][-1]+"." )
                if quarantine:
                    graph_controller.update_assuming_quarantine()
                else:
                    graph_controller.update_assuming_no_quarantine()
            no_simulations += 1
            data_file.write(str(graph_controller.time_elapsed) +'\n')

"""
Get random parameters for the simulation
"""
infection_probability = random.random()
detection_probability = random.random()
world_size = random.randint(1,101)
print("The world_size is ", world_size)

"""
Count the number of scenarios with same parameters were run.
This will help in creating a new file for a new simulation,
so more data can be used.
"""
scenarios_run_so_far = str(
    len([name for name in os.listdir('.') if name.startswith("quarantine") and name.endswith(".txt")]))

run_simulations(quarantine=True,
                filename="quarantine" + scenarios_run_so_far +".txt",
                maximum_steps_per_simulation=1_000_000_000_000_000_000,
                no_simulations_to_run=1,
                infection_probability= infection_probability,
                detection_probability = detection_probability,
                world_size = world_size)

run_simulations(quarantine=False,
                filename="non-quarantine" + scenarios_run_so_far + ".txt",
                maximum_steps_per_simulation=1_000_000_000_000_000_000,
                no_simulations_to_run=1,
                infection_probability = infection_probability,
                detection_probability = detection_probability,
                world_size = world_size)