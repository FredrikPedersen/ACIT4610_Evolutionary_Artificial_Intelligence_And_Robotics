from covid_modelling.health_state import HealthState
from covid_modelling.infection import Infection


class Person:

    def __init__(self, state: HealthState, age: int, infection: Infection = None):
        self.__state: HealthState = state
        self.__age = age
        self.__infection: Infection = infection

    def become_infected(self):
        self.__state = HealthState.Infected
        self.__infection = Infection()

    def become_recovered(self):
        self.__state = HealthState.Recovered
        self.__infection = None

    def become_dead(self):
        self.__state = HealthState.Dead
        self.__infection = None

    def get_state(self) -> HealthState:
        return self.__state

    def get_age(self) -> int:
        return self.__age

    def get_infection(self) -> Infection:
        return self.__infection

    def set_state(self, state: HealthState):
        self.__state = state
