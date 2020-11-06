import variables
import constants
import matplotlib.pyplot as pyplot


fitness_list = []
mask_fitness_list = []
social_fitness_list = []
mask_ratio = []
social_ratio = []




def calculate_mask_fitness():
    global mask_fitness_list, mask_ratio
    
    fitness_function = constants.total_population * 5 * (150 - variables.avg_infection_free) * (1 - (variables.avg_death_rate/100)*10) * (1 - (variables.avg_new_infected/100)*1.3) - (1000 * (1-variables.face_mask_rate)+(1-variables.social_distance_rate))
    mask_fitness_list.append(fitness_function)
    mask_ratio.append((1 - variables.face_mask_rate)*100)
    
def calculate_social_fitness():
    global social_fitness_list, social_ratio
    
    fitness_function = constants.total_population* 5 * (150 - variables.avg_infection_free) * (1 - (variables.avg_death_rate/100)*10) * (1 - (variables.avg_new_infected/100)*1.3) - (1000 * (1-variables.face_mask_rate)+(1-variables.social_distance_rate))
    social_fitness_list.append(fitness_function)
    social_ratio.append((1 - variables.social_distance_rate)*100)
    
    
    
def run_fitness_benchmark():
    variables.face_mask_rate = 1.0
    variables.social_distance_rate = 1.0
    variables.runs_to_avg = 1
    constants.amount_of_tests = 6 * variables.runs_to_avg

def adjust_mask():
    if variables.mask_evolve_complete == 0:
    
        calculate_mask_fitness()
    
        if len(mask_ratio)>=6:
            variables.mask_evolve_complete = 1
            variables.evolve_complete = 1 
            return
        print("Finished run " + str(len(mask_ratio)) + " out of " + str(constants.amount_of_tests))
    
        variables.face_mask_rate -= 0.2
        
        if variables.face_mask_rate <= 0:
            variables.face_mask_rate = 0
    
    
    else:
        variables.mask_evolve_complete = 1
        variables.evolve_complete = 1
        
        
def adjust_social():
    if variables.social_evolve_complete == 0:
    
        calculate_social_fitness()
    
        if len(social_ratio) >= 6:
            variables.evolve_complete = 1
            variables.social_evolve_complete = 1
            return
        
        print("Finished run " + str(len(social_ratio)) + " out of " + str(constants.amount_of_tests))

    
        variables.social_distance_rate -= 0.2
        if variables.social_distance_rate <= 0:
            variables.social_distance_rate = 0
    
    else: 
        variables.social_evolve_complete = 1
        variables.evolve_complete = 1
        

def evolve_mask_graph():
    global mask_fitness_list, mask_ratio,social_fitness_list, social_ratio
    pyplot.figure("Mask Fitness Adjustment")
    pyplot.plot(mask_ratio, mask_fitness_list, label='Mask Fitness Adjustment')
    pyplot.ylabel("Mask Fitness")
    pyplot.xlabel("Percentage of population wearing masks")
 
def evolve_social_graph():    
    global social_fitness_list, social_ratio,social_fitness_list, social_ratio

    pyplot.figure("Social Distance Adjustment")
    pyplot.plot(social_ratio,social_fitness_list, label = 'Social Fitness Adjustment')
    pyplot.ylabel("Social Fitness")
    pyplot.xlabel("Percentage of population Social Distancing")
    
    
    
    

