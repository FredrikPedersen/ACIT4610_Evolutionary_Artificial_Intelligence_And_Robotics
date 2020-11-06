import variables
import constants
import matplotlib.pyplot as pyplot

# finds the death_rate coefficient that makes the simulation match real world data.
actual_death_rate = [] 
tested_death_rate = []    
def adjust_rate(dr):
    global actual_death_rate, tested_death_rate
    actual_death_rate.append(dr * 100)
    tested_death_rate.append(constants.death_rate)
    constants.death_rate -= 0.01
    if constants.death_rate <= 0:
        constants.death_rate = 0.1
    if len(actual_death_rate) >= 10:
        variables.adjustment_complete = 1
    
    
def run_adjustment():
    constants.amount_of_tests = 10 # should be 100 for higher accurecy but will take a long time
    constants.death_rate = 0.1
    
def adjustment_graph():
    global actual_death_rate, tested_death_rate
    pyplot.figure("Death Rate Adjustment")
    pyplot.plot(tested_death_rate, actual_death_rate, label='Death Rate Adjustment')
    pyplot.xlim((0.01,0.1))

    pyplot.xlabel("Death Rate coefficient")
    pyplot.ylabel("Actual Death Rate in %")
