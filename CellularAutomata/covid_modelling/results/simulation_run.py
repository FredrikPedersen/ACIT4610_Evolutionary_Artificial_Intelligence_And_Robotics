import covid_modelling.variables as variables
from typing import Dict


class SimulationRun:

    # To be set when the evolutionary algorithm runs
    __inconvenience_scores: Dict[str, float]

    def __init__(self, total_people: int, deaths: int, infected: int):
        self.__total_people: int = total_people
        self.__deaths: int = deaths
        self.__infected: int = infected

        self.__infection_chance: float = variables.INFECTION_CHANCE
        self.__mortality_chance: float = variables.MORTALITY_CHANCE
        self.__percentage_masks: float = variables.PERCENTAGE_USING_MASKS
        self.__percentage_social_distancing: float = variables.PERCENTAGE_SOCIAL_DISTANCING
        self.__mandatory_isolation: bool = variables.MANDATORY_ISOLATION
        self.__fitness_scores: Dict[int, float] = {}

    def get_total_people(self) -> int:
        return self.__total_people

    def get_deaths(self) -> int:
        return self.__deaths

    def get_infected(self) -> int:
        return self.__infected

    def get_infection_chance(self) -> float:
        return self.__infection_chance

    def get_mortality_chance(self) -> float:
        return self.__mortality_chance

    def get_percentage_masks(self) -> float:
        return self.__percentage_masks

    def get_percentage_social_distancing(self) -> float:
        return self.__percentage_social_distancing

    def get_mandatory_isolation(self) -> bool:
        return self.__mandatory_isolation

    def get_fitness_score(self) -> Dict[int, float]:
        return self.__fitness_scores

    def get_inconvenience_scores(self) -> Dict[str, float]:
        if self.__inconvenience_scores is None:
            raise Exception("Inconvenience Score was never set!")

        return self.__inconvenience_scores

    def set_infected(self, infected: int):
        self.__infected = infected

    def set_deaths(self, deaths: int):
        self.__deaths = deaths

    def set_total_people(self, total_people: int):
        self.__total_people = total_people

    def set_fitness_score(self, fitness_scores: Dict[int, float]):
        self.__fitness_scores = fitness_scores

    def set_inconvenience_score(self, inconvenience_scores: Dict[str, float]):
        self.__inconvenience_scores = inconvenience_scores
