from typing import List
import covid_modelling.constants as constants
import covid_modelling.variables as variables
from covid_modelling.simulation_run import SimulationRun
from covid_modelling.preventive_measures import PreventiveMeasures


class EvolutionaryAlgorithm:

    __previous_simulation: SimulationRun
    __second_previous_simulation: SimulationRun
    __preventive_measures: PreventiveMeasures = PreventiveMeasures.get_instance()

    def evolve(self, simulation_runs: List[SimulationRun]):
        if len(simulation_runs) < 2:
            return

        self.__previous_simulation = simulation_runs[len(simulation_runs) - 1]
        self.__second_previous_simulation = simulation_runs[len(simulation_runs) - 2]

        return



