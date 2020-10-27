from typing import List
import covid_modelling.constants as constants
import covid_modelling.variables as variables
from covid_modelling.simulation_run import SimulationRun
from covid_modelling.preventive_measures import PreventiveMeasures
from covid_modelling.group import Group


class EvolutionaryAlgorithm:

    __previous_simulation: SimulationRun
    __preventive_measures: PreventiveMeasures = PreventiveMeasures.get_instance()

    def evolve(self, simulation_runs: List[SimulationRun]):
        self.__previous_simulation = simulation_runs[len(simulation_runs) - 1]
        fitness_score: float = self.__calculate_fitness()

        self.__previous_simulation.set_fitness_score(fitness_score)

        return

    def __calculate_fitness(self):
        return self.__calculate_inconvenience() + self.__previous_simulation.get_infected() + self.__previous_simulation.get_deaths()*2

    def __calculate_inconvenience(self) -> float:
        all_measures = self.__preventive_measures.get_preventive_measures()
        inconvenience_score = 0

        for measure in all_measures:
            affected_group = measure.get_group_affected()
            affected_people: int = self.__previous_simulation.get_total_people()

            if affected_group == Group.Healthy:
                affected_people -= self.__previous_simulation.get_infected() - self.__previous_simulation.get_deaths()
            elif affected_group == Group.Infected:
                affected_people = self.__previous_simulation.get_infected()

            measure_inconvenience = round(affected_people * measure.get_inconvenience_modifier(), 3)
            print(f"{measure.get_name()} score: {measure_inconvenience} percentage: {measure.get_percentage()}")
            inconvenience_score += measure_inconvenience

        return inconvenience_score

