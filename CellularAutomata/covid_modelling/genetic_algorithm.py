import covid_modelling.constants as constants
from typing import List
from covid_modelling.simulation_run import SimulationRun


# Data taken from FHI 19.10.2020.
# Is based on the outbreak starting in week 10 in 2020 (2nd - 8th of March).

TOTAL_POPULATION: int = 5328000
REPORTED_CASES: int = 16456
DEATHS: int = 278


def calculate_simulation_fitness(total_infected: int, total_deaths: int) -> int:
    """
    Calculates the fitness of the simulation run. A result closer to zero is better.

    :param total_infected: Number of infection cases in the simulation
    :param total_deaths: Number of deaths in the simulation
    :return: difference between reported real numbers and simulation numbers.
    """

    return __calculate_value_fitness(total_infected, REPORTED_CASES) + __calculate_value_fitness(total_deaths, DEATHS)


def __calculate_value_fitness(value: int, benchmark_value: int, absolute=True) -> int:
    if absolute:
        return abs(value - benchmark_value)
    else:
        return value - benchmark_value


def evolve_simulation(simulation_runs: List[SimulationRun]) -> List[SimulationRun]:

    # We should a few sample runs before starting the optimization
    if len(simulation_runs) > 2:

        # Sort simulation_run list based on their fitness and keep only the two best parents.
        for value in simulation_runs:
            print(value.get_fitness())

        simulation_runs = sorted(simulation_runs, key=lambda parent: parent.get_fitness())[:2]

        # Almost perfect simulation values found, no need to optimize.
        if simulation_runs[0].get_fitness() < 200:
            print("DONE")
            return simulation_runs

        best_simulation_deaths = simulation_runs[0].get_deaths()
        best_simulation_infected = simulation_runs[0].get_infected()
        second_best_simulation_deaths = simulation_runs[1].get_deaths()
        second_best_simulation_infected = simulation_runs[1].get_infected()

        print(f"{simulation_runs[0].get_fitness()} and {simulation_runs[1].get_fitness()}")

        # If the fitness value of the best simulation run is worse than that of the second best simulation run, MORTALITY_CHANCE must be changed
        if __calculate_value_fitness(best_simulation_deaths, DEATHS) > __calculate_value_fitness(second_best_simulation_deaths, DEATHS):

            # The fitness is worse and the death count is higher, reduce MORTALITY_CHANCE.
            if best_simulation_deaths > second_best_simulation_deaths:
                constants.MORTALITY_CHANCE -= 0.001

            # The fitness is worse and the death count is lower, increase MORTALITY_CHANCE.
            else:
                constants.MORTALITY_CHANCE += 0.001

        # If the fitness value of the best simulation run is worse than that of the second best simulation run, INFECTION_CHANCE must be changed
        elif __calculate_value_fitness(best_simulation_infected, REPORTED_CASES) > __calculate_value_fitness(second_best_simulation_infected, REPORTED_CASES):

            # The fitness is worse and the infection count is higher, reduce INFECTION_CHANCE.
            if best_simulation_infected > second_best_simulation_infected:
                constants.INFECTION_CHANCE -= 0.01

            # The fitness is worse and the infection count is lower, increase INFECTION_CHANCE.
            else:
                constants.INFECTION_CHANCE += 0.01

        # Best simulation run performs better than second best simulation run on both accounts, but is still not perfect
        else:
            # By checking whether the infected and death rates are higher or lower than the benchmark values, increase
            #or decrease INFECTION_CHANCE and/or MORTALITY_CHANCE accordingly.

            if __calculate_value_fitness(best_simulation_infected, REPORTED_CASES, False) < 0:
                constants.INFECTION_CHANCE += 0.01
            else:
                constants.INFECTION_CHANCE -= 0.01

            if __calculate_value_fitness(best_simulation_deaths, DEATHS, False) < 0:
                constants.MORTALITY_CHANCE += 0.001
            else:
                constants.MORTALITY_CHANCE -= 0.001

    else:
        constants.INFECTION_CHANCE += 0.01
        constants.MORTALITY_CHANCE += 0.001
        return simulation_runs
