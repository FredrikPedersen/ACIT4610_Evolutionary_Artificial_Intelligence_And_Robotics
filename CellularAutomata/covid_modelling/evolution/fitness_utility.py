from typing import Dict
from covid_modelling.results.simulation_run import SimulationRun
from covid_modelling.evolution.preventive_measures import PreventiveMeasures
from covid_modelling.evolution.group import Group


class FitnessUtility:

    __preventive_measures = PreventiveMeasures.get_instance()

    def calculate_and_update_fitness(self, simulation_run: SimulationRun, time_step: int) -> SimulationRun:
        all_measures = self.__preventive_measures.get_preventive_measures()
        inconvenience_score: int = 0
        measure_scores: Dict[str, float] = {}
        run_scores: Dict[int, float] = simulation_run.get_fitness_score()

        for measure in all_measures:
            measure_inconvenience_score = self.__calculate_inconvenience(measure, simulation_run)
            measure_scores[measure.get_name()] = measure_inconvenience_score
            inconvenience_score += measure_inconvenience_score

        fitness_score = round(inconvenience_score + (simulation_run.get_infected() * 30) + (simulation_run.get_deaths() * 50), 2)
        run_scores[time_step] = fitness_score

        simulation_run.set_inconvenience_score(measure_scores)
        simulation_run.set_fitness_score(run_scores)

        return simulation_run

    def __calculate_inconvenience(self, measure: PreventiveMeasures.PreventiveMeasure, simulation_run: SimulationRun) -> float:
        affected_group = measure.get_group_affected()
        affected_people: int = simulation_run.get_total_people()

        if affected_group == Group.Healthy:
            affected_people -= simulation_run.get_infected() - simulation_run.get_deaths()
        elif affected_group == Group.Infected:
            affected_people = simulation_run.get_infected()

        return round(affected_people * measure.get_inconvenience_modifier(), 3)