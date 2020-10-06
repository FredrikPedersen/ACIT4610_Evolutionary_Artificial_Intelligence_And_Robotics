from typing import Tuple
from covid_modelling.infection_state import InfectionState


class Person:

    """
    def __init__(self, position: tuple, age: int, social_distancing: bool, wearing_mask: bool, infected: bool,
                 infection_duration: int, recovered: bool):
        self.position: tuple = position
        self.age: int = age
        self.social_distancing: bool = social_distancing
        self.wearing_mask: bool = wearing_mask
        self.infected: bool = infected
        self.infection_duration: int = infection_duration
        self.recovered: bool = recovered
    """

    def __init__(self, state: InfectionState, recovered: bool = False):
        self.__state: InfectionState = state  # 0 = Dead, 1 = Healthy, 2 = Infected
        self.__recovered: bool = recovered

    def get_state(self) -> InfectionState:
        return self.__state

    def get_recovered(self) -> bool:
        return self.__recovered

    def set_state(self, state: InfectionState):
        self.__state = state

    def set_recovered(self, recovered: bool):
        self.__recovered = recovered
