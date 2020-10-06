import covid_modelling.constants as Constants


class Infection:

    __INCUBATION: str = "Incubation"
    __SYMPTOMS: str = "Symptoms"

    def __init__(self):
        self.__duration: int = 0
        self.__infection_stage: str = self.__INCUBATION
        self.__infectious: bool = False

    def update(self) -> None:
        self.__duration += 1
        self.__update_infection_stage()
        self.__update_infectious()

    def get_duration(self) -> int:
        return self.__duration

    def get_infectious(self) -> bool:
        return self.__infectious

    def __update_infection_stage(self) -> None:
        if self.__duration > Constants.INCUBATION_DURATION:
            self.__infection_stage = self.__SYMPTOMS

        else:
            self.__infection_stage = self.__INCUBATION

    def __update_infectious(self) -> None:
        if self.__duration > Constants.INFECTIOUS_START:
            self.__infectious = True

        else:
            self.__infectious = False
