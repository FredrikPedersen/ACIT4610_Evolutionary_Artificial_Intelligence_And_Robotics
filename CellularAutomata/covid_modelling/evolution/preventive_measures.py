import covid_modelling.constants as constants
import covid_modelling.variables as variables
from covid_modelling.evolution.group import Group


class PreventiveMeasures:
    __instance = None

    @staticmethod
    def get_instance():
        if PreventiveMeasures.__instance is None:
            PreventiveMeasures()

        return PreventiveMeasures.__instance

    def __init__(self):
        if PreventiveMeasures.__instance is not None:
            raise Exception("This is a Singleton class, do not try to instantiate it directly. Use get_instance method!")
        else:
            PreventiveMeasures.__instance = self

        self.update()

    def update(self):
        self.__preventive_measures = []
        self.__preventive_measures.append(
        self.PreventiveMeasure(constants.MASK_MEASURE, 0.5, Group.Everyone, variables.PERCENTAGE_USING_MASKS))
        self.__preventive_measures.append(self.PreventiveMeasure(constants.SOCIAL_DISTANCE_MEASURE, 0.4, Group.Everyone, variables.PERCENTAGE_SOCIAL_DISTANCING))

        if variables.MANDATORY_ISOLATION:
            self.__preventive_measures.append(self.PreventiveMeasure(constants.ISOLATION_MEASURE, 1.0, Group.Infected))

    def get_preventive_measures(self):
        return self.__preventive_measures

    class PreventiveMeasure:

        def __init__(self, name: str, inconvenience_weight: float, group_affected: Group, percentage: float = 1.0):
            if inconvenience_weight <= 0.1 or inconvenience_weight > 1.0:
                raise Exception("Inconvenience Weight may only be a floating point number between 0.1 and 1.0!")

            self.__name = name
            self.__inconvenience_weight = inconvenience_weight
            self.__group_affected = group_affected
            self.__percentage_of_population: float = percentage

        def get_inconvenience_modifier(self) -> float:
            return self.__percentage_of_population * self.__inconvenience_weight

        def get_name(self) -> str:
            return self.__name

        def get_inconvenience_weight(self) -> float:
            return self.__inconvenience_weight

        def get_group_affected(self) -> Group:
            return self.__group_affected

        def get_percentage(self) -> float:
            return self.__percentage_of_population
