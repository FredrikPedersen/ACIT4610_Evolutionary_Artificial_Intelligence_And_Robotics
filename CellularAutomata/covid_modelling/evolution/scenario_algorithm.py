import covid_modelling.variables as variables

counter: int = 0
benchmark_run: bool = True


def evolve() -> bool:
    """
    Evolve the the simulation by first disabling all preventive measures, and then implement them for 10% of the
    population at the time.

    For every run Mandatory Isolation is toggled on/off.
    Every second run Social Distancing is increased by 10%
    Every fourth run Social Distancing is reduced by 10% and mask usage increased by 10%.

    :return: boolean value indicating if all evolution scenarios have been completed
    """

    global counter

    if benchmark_run:
        __benchmark_run_complete()
        return False

    __toggle_isolation()

    if counter != 0 and counter % 2 == 0:
        variables.PERCENTAGE_SOCIAL_DISTANCING = round((variables.PERCENTAGE_SOCIAL_DISTANCING + 0.1), 2)

    if counter != 0 and counter % 4 == 0:
        variables.PERCENTAGE_USING_MASKS = round((variables.PERCENTAGE_USING_MASKS + 0.1), 2)
        variables.PERCENTAGE_SOCIAL_DISTANCING = round((variables.PERCENTAGE_SOCIAL_DISTANCING - 0.2), 2)

    if counter >= 6:
        counter = 0

    counter += 1
    return True if variables.PERCENTAGE_USING_MASKS == 1.0 and variables.PERCENTAGE_SOCIAL_DISTANCING == 1.0 and not variables.MANDATORY_ISOLATION else False


def __benchmark_run_complete():
    global benchmark_run
    """
    The default configuration of the simulation is set to give values roughly equal to the pandemic's behaviour in
    Norway. After the initial run (the benchmark run), set all values for preventive measures to 0 or false so we can
    work through all scenarios.
    """
    benchmark_run = False
    variables.PERCENTAGE_USING_MASKS = 0.0
    variables.PERCENTAGE_SOCIAL_DISTANCING = 0.0
    __toggle_isolation()


def __toggle_isolation():
    variables.MANDATORY_ISOLATION = not variables.MANDATORY_ISOLATION



