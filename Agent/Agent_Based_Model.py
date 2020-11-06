import matplotlib.pyplot as plt
import numpy as np
import time
import pycxsimulator
from pylab import *
import copy as cp
import variables
import constants
from evolve_model import run_fitness_benchmark
from evolve_model import adjust_mask
from evolve_model import adjust_social
from adjust_death_rate_constant import run_adjustment
from adjust_death_rate_constant import adjust_rate


face_mask = True # Face massk on/off
social_distance = True # Social distance on/off

adjust = False # Adjust death rate coefficient. (Will take a couple of min)
evolve_mask = False # Turn mask evolution ON/OFF, Cannot run together with adjustment or social evolve (would take a very long time)
evolve_social = False # Turn social evolution ON/OFF, Cannot run together with adjustment or mask evolve (would take a very long time)


if adjust and variables.adjustment_complete == 0:
    run_adjustment()

if evolve_mask or evolve_social and variables.evolve_complete == 0:
    run_fitness_benchmark()
    
    

class agent:
    pass

def initialize():
    global agents, total_nr_infected , total_nr_dead, total_nr_recovered,infection_free
    
    # Resets the values for the next run
    variables.infection_free_day = 0
    variables.final_death_rate = 0.0
    variables.new_infected = 0
    variables.new_infected_percent = 0.0
    variables.run_ended = 0
    agents = []
    
    # Chooses a random ratio of starting population to infect. Between 10 and 50 %
    amount_inf = uniform(0.1,0.5)
    variables.h_init = int(constants.total_population * (1-amount_inf)) # initial healthy population
    variables.i_init = int(constants.total_population * amount_inf) # initial infected population

    # Choosing random coordinates for each agent. Places agent further apart if social distancing is on
    for i in range(variables.h_init + variables.i_init):
        ag = agent()
        ag.type = 'h' if i < variables.h_init else 'i'
        if social_distance == False:
            ag.x = uniform(0,5)
            ag.y = uniform(0,5)
        elif social_distance == True:
            ag.x = uniform(0,5)
            ag.y = uniform(0,5)
            collision = [nbc for nbc in agents if (ag.x - nbc.x)**2 + (ag.y - nbc.y)**2 < constants.social_distsq]
            while len(collision)>0:
                ag.x = uniform(0,5)
                ag.y = uniform(0,5)
                collision = []
                collision = [nbc for nbc in agents if (ag.x - nbc.x)**2 + (ag.y - nbc.y)**2 < constants.social_distsq]
        
        # Chooses an age for each agent and places them in a risk group if necesarry
        ag.sickCount = 0
        ag.age = randint(18,100)
        if random() < constants.high_risk and ag.age < 65:
            ag.risk_group = 1
        elif ag.age >= 65 and ag.age < 75:
            ag.risk_group = 2
        elif ag.age >= 75 and ag.age < 85:
            ag.risk_group = 3
        elif ag.age >= 85:
            ag.risk_group = 4
        else:
            ag.risk_group = 0
        
        # Decides if and agent will agree to social distance and to wear a mask
        if social_distance == True and random() < variables.social_distance_rate:
            ag.agrees_to_social_distance = 0
        else:
            ag.agrees_to_social_distance = 1
            
        if face_mask == True and random() < variables.face_mask_rate:
            ag.agrees_to_wear_mask = 0
        else:
            ag.agrees_to_wear_mask = 1
        
        agents.append(ag)
        
        #resets statistics
        total_nr_dead = 0
        total_nr_infected = variables.i_init
        total_nr_recovered = 0
        variables.step_counter = 0
          

def observe():
    global agents, total_nr_dead, total_nr_recovered, total_nr_infected, total_nr_steps
    # Plots each agents on the board depending on their type
    cla()  #clear visualization space
    healthy = [ag for ag in agents if ag.type == 'h']
    if len(healthy) > 0:
        x = [ag.x for ag in healthy]
        y = [ag.y for ag in healthy]
        plot(x, y, 'bo', markersize = 2)
    infected = [ag for ag in agents if ag.type == 'i']
    if len(infected) > 0:
        x = [ag.x for ag in infected]
        y = [ag.y for ag in infected]
        plot(x, y, 'ro', markersize = 2)
    recovered = [ag for ag in agents if ag.type == 'r']
    if len(recovered) > 0:
        x = [ag.x for ag in recovered]
        y = [ag.y for ag in recovered]
        plot(x, y, 'go', markersize = 2)
    
    isolated = [ag for ag in agents if ag.type == 'id']
    if len(isolated) > 0:
        x = [ag.x for ag in isolated]
        y = [ag.y for ag in isolated]
        plot(x, y, 'ko', markersize = 2)
        
    # if there are no more infected or isolated agents remaining the statistics are gathered and a new round begins
    if len(infected) == 0 and len(isolated) == 0 and  variables.run_ended == 0:
        variables.infection_free_day = variables.step_counter
        variables.final_death_rate = round((total_nr_dead/total_nr_infected),2)
        variables.new_infected = total_nr_infected - variables.i_init
        variables.new_infected_percent = round((variables.new_infected/variables.i_init),2)
        add_to_avg_list(variables.infection_free_day, variables.final_death_rate, variables.new_infected_percent)
      
        variables.counter +=1
        print ("Run nr: " + str(variables.counter) +" of " + str(variables.runs_to_avg) + "\n")

        if variables.counter >= variables.runs_to_avg:
            create_avg()
            if adjust:
                adjust_rate(variables.avg_death_rate)
            
            elif evolve_mask and evolve_social == False:
                adjust_mask()
        
            elif evolve_social and evolve_mask == False:               
                adjust_social()
                
            
                
            variables.counter = 0
        
        variables.run_ended = 1

        
                
    if len(infected) != 0 or len(isolated) != 0:
        variables.step_counter +=1    

    
    axis('image')
    axis([0, 5, 0, 5])
    title('Infected = ' + str(total_nr_infected) + ' Recovered = ' + str(total_nr_recovered) + ' Dead = ' + str(total_nr_dead))


def update_one_agent():
    global agents, total_nr_dead, total_nr_recovered, total_nr_infected, total_nr_steps
    if agents == []:
        return
    
    ag = choice(agents)  #random agent from list
    
    if social_distance == False:
        # simulating random movement
        m = constants.movement_rate
        if ag.type != 'id':
            ag.x += uniform(-m, m)  #random value between m and -m
            ag.y += uniform(-m, m)
            ag.x = 5 if ag.x > 5 else 0 if ag.x < 0 else ag.x
            ag.y = 5 if ag.y > 5 else 0 if ag.y < 0 else ag.y
    
    elif social_distance == True:
        m = constants.movement_rate
        attempt_count = 0
        
        while True:
            tempx = ag.x + uniform(-m, m)
            tempy = ag.y + uniform(-m, m)
            tempx = 5 if tempx > 5 else 0 if tempx < 0 else tempx
            tempy = 5 if tempy > 5 else 0 if tempy < 0 else tempy
            
            collision = []
            collision = [nbc for nbc in agents if (tempx - nbc.x)**2 + (tempy - nbc.y)**2 < constants.neighbor_distance_sq]
            
            if ag.type == 'id':
                break
            
            if len(collision) > 0:
                if ag.agrees_to_social_distance == 0:
                    ag.x = tempx
                    ag.y = tempy
                    break
                else:    
                    attempt_count += 1
            
            if len(collision) == 0:
                ag.x = tempx
                ag.y = tempy
                break
            
            if attempt_count == 10:
                break
        

    # detecting collision and simulating death
    neighbors = [nb for nb in agents if nb.type != ag.type
                 and nb.type != 'r' 
                 and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < constants.cdsq]

    if ag.type == 'i' or ag.type == 'id':
        ag.sickCount += 1
        
        if ag.type != 'id' and random() < ag.sickCount * 0.05:
            ag.type = 'id'
            
            
        if ag.sickCount >= constants.recovery_time:
            
            
            if ag.risk_group != 0 and random() < constants.death_rate * ag.risk_group:
                agents.remove(ag)
                total_nr_dead += 1
                return
            

            else:
                if random() < ag.sickCount*0.03:
                    ag.type = 'r'
                    total_nr_recovered += 1
                    return
        
    if ag.type == 'h':
        if len(neighbors) > 0: # if there are infected nearby
            if ag.agrees_to_wear_mask == 0 and random() < constants.sick_rate:
                ag.type = 'i'
                total_nr_infected += 1
                return
            elif ag.agrees_to_wear_mask == 1 and random() < constants.sick_rate*constants.face_mask_effectivness:
                ag.type = 'i'
                total_nr_infected += 1
                return

def update():
    global agents
    t = 0.
    
    while t < 1. and len(agents) > 0:
        t += 1. / len(agents)
        update_one_agent()

    #adds values to the avg list
def add_to_avg_list(infection_free, final_death_rate, new_infected_percent):
    variables.infection_free_list.append(infection_free)
    variables.death_rate_list.append(final_death_rate)
    variables.new_infected_list.append(new_infected_percent)

    # prints out the avg after each day
def create_avg():
    variables.avg_infection_free = round(sum(variables.infection_free_list)/len(variables.infection_free_list),2)
    variables.avg_death_rate = round(100*(sum(variables.death_rate_list)/len(variables.death_rate_list)),2)
    variables.avg_new_infected = round(100*(sum(variables.new_infected_list)/len(variables.new_infected_list)),2)
    print("Infection free after = " + str(variables.avg_infection_free) +" days\nDeath rate % : " + str(variables.avg_death_rate) + "%\nNew infected % : " + str(variables.avg_new_infected) + " %")
    

pycxsimulator.GUI().start(func=[initialize, observe, update])


