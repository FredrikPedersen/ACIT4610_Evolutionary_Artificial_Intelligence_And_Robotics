from statistics import mean
import re

"""
Method used to return the variables associated with the scenario run by the algorithm.

Parameters:
    :param simulation_results_file:The name of the simulation result file we want to read.

Returns:
    :returns no_simulation: The number of simulation used to run.
    :returns initial_infection_probability: The initial probability of a person to be infected.
    :returns detection_probability: The probability that a person that is infected is detected.
    :returns world_size: The number of people in the scenario.
"""
def print_simulation_configuration_variables(simulation_results_file):
    lines_read = 0
    no_simulations = 0
    initial_infection_probability = 0
    detection_probability = 0
    world_size = 0
    with open(simulation_results_file) as quarantine_file:
        for line in quarantine_file:
            lines_read += 1
            if "We will run" in line:
                no_simulations = int(re.findall("\d+", line)[0])
            elif "initial infection probability" in line:
                initial_infection_probability = float(re.findall("\d+\.\d+", line)[0])
            elif "detection probability" in line:
                detection_probability = float(re.findall("\d+\.\d+", line)[0])
            elif "with the world size" in line:
                world_size = int(re.findall("\d+", line)[0])
            if lines_read == 4:
                break
    print("World size is " + str(world_size) )
    print("The number of simulations run on the file was " + str(no_simulations) )
    print("The initial infection probability was  " + str(initial_infection_probability) )
    print("The detection proabability was " + str(detection_probability))

"""
Will read the time data from the file and append.
Parameters:
    :param simulation_results_file:The file containing the time results about the simulation. 
Returns:
    :returns world_size,mean(times),no_simulations,initial_infection_probability,detection_probability:
    Returning the configuration of the test and how fast the world recovered.
"""
def construct_times_array(quarantine_file):
    global time_results
    for line in quarantine_file:
        try:
            if line[:-1].isdecimal():
                time = int(line[:-1])
                time_results.append(time)
        except Exception as e:
                print("The exception is",e)

'''
Compute the mean number of steps for the whole set and also for the subsamples. 
'''
def mean_number_of_steps():
    global time_results
    global samples_step_size_averages
    global step_size
    for sample_no in range(0,len(time_results) // step_size):
        print("Limits are:",str(sample_no*step_size),":",str((sample_no+1)*step_size))
        samples_step_size_averages.append(mean(time_results[sample_no*step_size:(sample_no+1)*step_size]))

"""
Print the main results of the simulation
Parameters:
    :param simulation_results_file:The file containing the time results about the simulation. 
"""
def analyze_results_from_file(results_file_path):
    global time_results
    global samples_step_size_averages

    #Clear the previous results
    time_results = []
    samples_step_size_averages = []

    with open(results_file_path) as results_file:
        construct_times_array(results_file)
        print("We added ", len(time_results), "results")
        print("The time results were", time_results)
        print("The average number of steps is", mean(time_results))
        mean_number_of_steps()
        print("The subsamples averages are", samples_step_size_averages)

time_results = []
samples_step_size_averages = []
scenario_number_to_analyze = 0
step_size = 3000

#Display time results when we apply quarantine.
print("With quarantine applied")
quarantine_file_path = "quarantine"+ str(scenario_number_to_analyze)+".txt"
print_simulation_configuration_variables(quarantine_file_path)
analyze_results_from_file(quarantine_file_path)

#Display time results when we don't apply quarantine
print("Without quarantine")
non_quarantine_file_path = "non-quarantine"+ str(scenario_number_to_analyze)+".txt"
print_simulation_configuration_variables(non_quarantine_file_path)
analyze_results_from_file(non_quarantine_file_path)