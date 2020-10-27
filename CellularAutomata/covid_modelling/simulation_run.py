import covid_modelling.variables as variables


class SimulationRun:

    def __init__(self, total_people: int, deaths: int, infected: int, reproduction_rate: float):
        self.__total_people: int = total_people
        self.__deaths: int = deaths
        self.__infected: int = infected
        self.__reproduction_rate: float = reproduction_rate
        self.__infection_chance: float = variables.INFECTION_CHANCE
        self.__mortality_chance: float = variables.MORTALITY_CHANCE
        self.__percentage_masks: float = variables.PERCENTAGE_USING_MASKS
        self.__percentage_social_distancing: float = variables.PERCENTAGE_SOCIAL_DISTANCING
        self.__fitness_score: float = 0

    def get_total_people(self) -> int:
        return self.__total_people

    def get_deaths(self) -> int:
        return self.__deaths

    def get_infected(self) -> int:
        return self.__infected

    def get_reproduction_rate(self) -> float:
        return self.__reproduction_rate

    def get_infection_chance(self) -> float:
        return self.__infection_chance

    def get_mortality_chance(self) -> float:
        return self.__mortality_chance

    def get_percentage_masks(self) -> float:
        return self.__percentage_masks

    def get_percentage_social_distancing(self) -> float:
        return self.__percentage_social_distancing

    def get_fitness_score(self) -> float:
        return self.__fitness_score

    def set_fitness_score(self, fitness_value: float):
        self.__fitness_score = fitness_value
