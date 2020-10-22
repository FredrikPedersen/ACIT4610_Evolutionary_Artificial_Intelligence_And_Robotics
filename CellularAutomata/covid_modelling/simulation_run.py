import covid_modelling.genetic_algorithm as ga
import covid_modelling.constants as constants


class SimulationRun:

    def __init__(self, deaths: int, infected: int):
        self.__deaths: int = deaths
        self.__infected: int = infected
        self.__infection_chance: float = constants.INFECTION_CHANCE
        self.__mortality_chance: float = constants.MORTALITY_CHANCE

    def get_deaths(self) -> int:
        return self.__deaths

    def get_infected(self) -> int:
        return self.__infected

    def get_infection_chance(self) -> float:
        return self.__infection_chance

    def get_mortality_chance(self) -> float:
        return self.__mortality_chance
