import covid_modelling.variables as variables

counter: int = 1
benchmark_run: bool = True


def evolve() -> bool:
    global counter

    if benchmark_run:
        __benchmark_run_complete()
        return False

    if counter % 2 == 0:
        __adjust_social_distancing()

    if counter % 3 == 0:
        __adjust_mask_usage()
        counter += 1

    if counter % 5 == 0:
        __toggle_isolation()
        counter = 1

    counter += 1
    return True if variables.PERCENTAGE_USING_MASKS == 1.0 and variables.PERCENTAGE_SOCIAL_DISTANCING == 1.0 else False

    #PLAN! Print finished run data to a graph, displaying the fitness score of each run.
    #Create two graphs: one for isolation enabled, and for disabled. Have the fitness score as Y-value and
    # Percentage of social distancers and mask wearers as the X-value.


def __adjust_mask_usage():
    if variables.PERCENTAGE_USING_MASKS < 1.0:
        variables.PERCENTAGE_USING_MASKS = round((variables.PERCENTAGE_USING_MASKS + 0.1), 2)


def __adjust_social_distancing():
    if variables.PERCENTAGE_SOCIAL_DISTANCING < 1.0:
        variables.PERCENTAGE_SOCIAL_DISTANCING = round((variables.PERCENTAGE_SOCIAL_DISTANCING + 0.1), 2)


def __benchmark_run_complete():
    global benchmark_run
    """
    The default configuration of the simulation is set to give values roughly equal to the pandemic's behaviour in
    Norway. After the initial run (the benchmark run), set all values for preventive measures to 0 or false so we can
    work through all scenarios.
    :return:
    """

    benchmark_run = False
    variables.PERCENTAGE_USING_MASKS = 0.0
    variables.PERCENTAGE_SOCIAL_DISTANCING = 0.0
    __toggle_isolation()


def __toggle_isolation():
    variables.MANDATORY_ISOLATION = not variables.MANDATORY_ISOLATION



