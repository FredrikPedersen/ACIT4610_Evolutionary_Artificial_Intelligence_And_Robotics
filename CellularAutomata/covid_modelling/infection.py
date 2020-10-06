class Infection:

    __INCUBATION: str = "Incubation"
    __SYMPTOMS: str = "Symptoms"
    __MAX_DURATION: int = 20
    __INFECTIOUS_START = 3
    __INCUBATION_PERIOD = 6

    def __init__(self):
        self.__duration: int = 0
        self.__infection_stage: str = self.__INCUBATION
        self.__infectious: bool = False

    def update(self) -> None:
        if self.__duration < self.__MAX_DURATION:
            self.__duration += 1
            self.__update_infection_stage()
            self.__update_infectious()

    def get_duration(self) -> int:
        return self.__duration

    def __update_infection_stage(self) -> None:
        if self.__duration > self.__INCUBATION_PERIOD:
            self.__infection_stage = self.__SYMPTOMS

        else:
            self.__infection_stage = self.__INCUBATION

    def __update_infectious(self) -> None:
        if self.__duration > self.__INFECTIOUS_START:
            self.__infectious = True

        else:
            self.__infectious = False
