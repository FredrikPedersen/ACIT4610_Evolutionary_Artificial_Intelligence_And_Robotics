from covid_modelling.health_state import HealthState
from covid_modelling.infection import Infection
import covid_modelling.constants as constants
import covid_modelling.variables as variables
import random


class Person:

    def __init__(self, state: HealthState):
        self.__state: HealthState = state

        self.__social_distancing: bool = bool(random.getrandbits(1))
        self.__age = int(random.random() * 100)
        self.__infection: Infection = Infection()
        self.__in_isolation: bool = False

        #  Random check to see if the person is wearing a mask
        if random.random() < variables.PERCENTAGE_USING_MASKS:
            self.__wearing_mask = True
        else:
            self.__wearing_mask = False

        #  Random check to see if the person belongs in a risk group
        if random.random() < constants.MORTAL_RISK_GROUP_PERCENTAGE:
            self.__risk_group = True
        else:
            self.__risk_group = False

        #  Determine whether the virus would be lethal to this person
        if self.__risk_group or self.__age > constants.MORTAL_RISK_AGE:
            if random.random() < variables.MORTALITY_CHANCE:
                self.__infection.set_lethal(True)

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

    def get_social_distancing(self) -> bool:
        return self.__social_distancing

    def get_wearing_mask(self) -> bool:
        return self.__wearing_mask

    def get_age(self) -> int:
        return self.__age

    def get_infection(self) -> Infection:
        return self.__infection

    def get_risk_group(self) -> bool:
        return self.__risk_group

    def get_in_isolation(self) -> bool:
        return self.__in_isolation

    def set_state(self, state: HealthState):
        self.__state = state

    def set_in_isolation(self, in_isolation: bool):
        self.__in_isolation = in_isolation

    def __str__(self):
        return "Age: " + str(self.__age) + " Infection: " + str(self.__infection) + " State: " + str(self.__state.value)

