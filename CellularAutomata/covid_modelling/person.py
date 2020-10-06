from covid_modelling.infection_state import InfectionState


class Person:

    def __init__(self, state: InfectionState):
        self.__state: InfectionState = state

    def get_state(self) -> InfectionState:
        return self.__state

    def set_state(self, state: InfectionState):
        self.__state = state
