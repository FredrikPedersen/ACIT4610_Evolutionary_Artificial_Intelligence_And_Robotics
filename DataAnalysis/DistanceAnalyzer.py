from statistics import mean
import re

"""
Print statistics about distances.

Parameters:
    :param simulation_results_file:The file containing the results about the simulation. 
Returns:
    :returns world_size,mean(times),no_simulations,initial_infection_probability,detection_probability:
    Returning the configuration of the test and how fast the world recovered.
"""
def statistics_about_data(simulation_results_file):
    quarantine_file = open(simulation_results_file,"r")
    results_with_distances = []
    times = []
    time = 0
    no_simulations = 0
    initial_infection_probability = 0.0
    for line in quarantine_file.readlines():
        if '[' in line:
            distances = [float(s) for s in line[1:-2].split(',')]
            results_with_distances.append((time,distances))
        elif "We will run" in line:
            no_simulations = int(re.findall("\d+", line)[0])
        elif "initial infection probability" in line:
            initial_infection_probability = float(re.findall("\d+\.\d+", line)[0])
        elif "detection probability" in line:
            detection_probability = float(re.findall("\d+\.\d+", line)[0])
        elif "with the world size" in line:
            world_size = int(re.findall("\d+", line)[0])
        else:
            time = int(line)
            times.append(time)

    for time,distances_array in results_with_distances:\
        print("It took",time,"steps to beat covid.\n",
              "Some stats about the distance in this case:"
              "\n   minimum distance:",min(distances_array),
              "\n   average distance:",mean(distances_array),
              "\n   sorted_distances:",sorted(distances_array),
              "\n   maximum distance",max(distances_array),
              "\n")
    return world_size,mean(times),no_simulations,initial_infection_probability,detection_probability

quarantine_world_size,quarantine_average_steps,quarantine_no_simulations,\
quarantine_initial_infection_probability,quarantine_detection_probability = \
    statistics_about_data("quarantine0.txt")

non_quarantine_world_size,non_quarantine_average_steps,non_quarantine_no_simulations,\
non_quarantine_initial_infection_probability,non_quarantine_detection_probability = \
    statistics_about_data("non-quarantine0.txt")

print("I will present the results for both applying quarantine and not.\n")

print("If I applied quarantine.",
      "The following variables were set:\n",
      "Initial world size:",quarantine_world_size,"\n",
      "Initial infection probability:",quarantine_initial_infection_probability,"\n",
      "Detection probability of an infected person:",quarantine_detection_probability,'\n'
      "The results are:\n We run",quarantine_no_simulations,
      "simulations and the average number of steps was",quarantine_average_steps,'\n')

print("If I did not apply quarantine.",
      "The following variables were set:\n",
      "Initial world size:",non_quarantine_world_size,"\n",
      "Initial infection probability:",non_quarantine_initial_infection_probability,"\n",
      "Detection probability of an infected person:",non_quarantine_detection_probability,'\n'
      "The results are:\n We run",non_quarantine_no_simulations,
      "simulations and the average number of steps was",non_quarantine_average_steps)