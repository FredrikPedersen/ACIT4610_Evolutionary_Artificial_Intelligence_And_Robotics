from covid_modelling.health_state import HealthState
from covid_modelling.infection import Infection

class Person:

    def __init__(self, state: HealthState, age: int):
        self.__state: HealthState = state
        self.__age = age
        self.__infection: Infection = Infection()

    def become_infected(self):
        self.__state = HealthState.Infected

    def become_recovered(self):
        self.__state = HealthState.Recovered
        self.__infection.update(False)

    def become_dead(self):
        self.__state = HealthState.Dead
        self.__infection.update(False)

    def get_state(self) -> HealthState:
        return self.__state

    def get_age(self) -> int:
        return self.__age

    def get_infection(self) -> Infection:
        return self.__infection

    def set_state(self, state: HealthState):
        self.__state = state

    def __str__(self):
        return "Age: " + str(self.__age) + " Infection: " + str(self.__infection) + " State: " + str(self.__state.value)
