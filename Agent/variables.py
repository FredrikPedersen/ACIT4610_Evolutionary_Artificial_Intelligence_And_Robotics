face_mask_rate = 0.3 # Percentage of people refusing to wear mask

social_distance_rate = 0.2 # Percentage of people refusing to social distance

i_init = 0 # initial infected population

h_init = 0 # initial healthy population

run_ended = 0 # Goes to 1 when there are no more infected agents remaining

counter = 0 # counts amount of finished runs

step_counter = 0 # Counts current step

runs_to_avg = 3 #amount of runs to create an avg

infection_free_day = 0 # The step/day when there are no more infected remaining

final_death_rate = 0.0 # Final % death rate, amount infected / amount dead

new_infected = 0 # amount of new infected agents, total infected - initial infected

new_infected_percent = 0.0 # amount of new inferctions shown as a percentage

infection_free_list = [] # List containing days until infection free for each run

death_rate_list = [] # list containing death rates for each run

new_infected_list = [] # list containing new infected numbers for each run

adjustment_complete = 0 # goes to 1 if the adjustment is completed

mask_evolve_complete = 0 # goes to 1 if the mask evolution is complete
social_evolve_complete = 0 # goes to 1 if the social evolution is complete
evolve_complete = 0 # goes to 1 if the evolution is complete







# Lists for avg values
avg_infection_free = 0.0
avg_death_rate = 0.0
avg_new_infected = 0.0




# PYCX variables
test_counter = 0





