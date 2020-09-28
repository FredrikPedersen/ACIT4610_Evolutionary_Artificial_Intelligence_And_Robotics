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

    def __init__(self, position: tuple, infected: bool):
        self.position: tuple = position
        self.infected: bool = infected
