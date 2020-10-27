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

        return

    def __calculate_fitness(self) -> float:
        all_measures = self.__preventive_measures.get_preventive_measures()
        inconvenience_score = 0
        measure_scores = {}

        for measure in all_measures:
            measure_inconvenience_score = self.__calculate_inconvenience(measure)
            measure_scores[measure.get_name()] = measure_inconvenience_score
            inconvenience_score += measure_inconvenience_score

        fitness_score = inconvenience_score + self.__previous_simulation.get_infected() + self.__previous_simulation.get_deaths() * 2
        self.__previous_simulation.set_inconvenience_score(measure_scores)
        self.__previous_simulation.set_fitness_score(fitness_score)

        return fitness_score

    def __calculate_inconvenience(self, measure: PreventiveMeasures.PreventiveMeasure) -> float:
        affected_group = measure.get_group_affected()
        affected_people: int = self.__previous_simulation.get_total_people()

        if affected_group == Group.Healthy:
            affected_people -= self.__previous_simulation.get_infected() - self.__previous_simulation.get_deaths()
        elif affected_group == Group.Infected:
            affected_people = self.__previous_simulation.get_infected()

        return round(affected_people * measure.get_inconvenience_modifier(), 3)

