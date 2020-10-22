import covid_modelling.constants as constants


class Infection:

    def __init__(self):
        self.__duration: int = 0
        self.__infection_stage: str = constants.INCUBATION
        self.__infectious: bool = False
        self.__lethal: bool = False

    def update(self, active_infection=True) -> None:
        if active_infection:
            self.__duration += 1
            self.__update_infection_stage()
            self.__update_infectious()
        else:
            self.__duration = 0
            self.__infection_stage = constants.INCUBATION
            self.__infectious = False

    def get_duration(self) -> int:
        return self.__duration

    def get_infection_stage(self) -> str:
        return self.__infection_stage

    def get_infectious(self) -> bool:
        return self.__infectious

    def get_lethal(self) -> bool:
        return self.__lethal

    def set_lethal(self, lethal: bool) -> None:
        self.__lethal = lethal

    def __update_infection_stage(self) -> None:
        if self.__duration > constants.INCUBATION_DURATION:
            self.__infection_stage = constants.SYMPTOMS

        else:
            self.__infection_stage = constants.INCUBATION

    def __update_infectious(self) -> None:
        if self.__duration > constants.INFECTIOUS_START:
            self.__infectious = True

        else:
            self.__infectious = False

    def __str__(self):
        return "Duration: " + str(self.__duration) + " Stage: " + str(self.__infection_stage) + " Infectious: " + str(self.__infectious)
