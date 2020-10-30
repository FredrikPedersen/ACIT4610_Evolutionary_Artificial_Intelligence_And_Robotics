from typing import List

import matplotlib.pyplot as pyplot
import covid_modelling.constants as constants

from covid_modelling.results.simulation_run import SimulationRun

figure_without_isolation:str = "Without Isolation"
figure_with_isolation: str = "With Isolation"
distancing_values: str = "Distancing Values"
mask_values: str = "Mask Values"


def draw_graphs(simulation_runs: List[SimulationRun]):

    __plot_benchmark_fitness_timestep(simulation_runs, [figure_with_isolation, figure_without_isolation])
    __draw_timestep_graphs(simulation_runs)
    __draw_mask_percentage_graphs(simulation_runs)
    __draw_distancing_percentage_graphs(simulation_runs)


def __draw_distancing_percentage_graphs(simulation_runs: List[SimulationRun]):
    with_isolation = []
    without_isolation = []

    for simulation_run in simulation_runs:
        if simulation_run.get_mandatory_isolation() is True:
            with_isolation.append(simulation_run)
        else:
            without_isolation.append(simulation_run)

    without_isolation.sort(key=lambda sim_run: sim_run.get_percentage_social_distancing())
    with_isolation.sort(key=lambda sim_run: sim_run.get_percentage_social_distancing())

    x: [str] = []
    without_isolation_y: [float] = []
    for simulation_run in without_isolation:
        x.append(f"{simulation_run.get_percentage_social_distancing() * 100}%")
        without_isolation_y.append(simulation_run.get_fitness_score()[constants.DAYS_SINCE_OUTBREAK])

    pyplot.figure(distancing_values)
    pyplot.plot(x, without_isolation_y, color="red", label="Without Isolation")

    with_isolation_y: [float] = []
    for simulation_run in with_isolation:
        with_isolation_y.append(simulation_run.get_fitness_score()[constants.DAYS_SINCE_OUTBREAK])

    pyplot.figure(distancing_values)
    pyplot.plot(x, with_isolation_y, color="blue", label="With Isolation")
    pyplot.legend()
    pyplot.xlabel("Social Distancing Percentage")
    pyplot.ylabel("Fitness Score")
    pyplot.title("Distancing Fitness")


def __draw_mask_percentage_graphs(simulation_runs: List[SimulationRun]):
    with_isolation = []
    without_isolation = []

    for simulation_run in simulation_runs:
        if simulation_run.get_mandatory_isolation() is True:
            with_isolation.append(simulation_run)
        else:
            without_isolation.append(simulation_run)

    x: [str] = []
    without_isolation_y: [float] = []
    for simulation_run in without_isolation:
        x.append(f"{simulation_run.get_percentage_masks() * 100}%")
        without_isolation_y.append(simulation_run.get_fitness_score()[constants.DAYS_SINCE_OUTBREAK])

    pyplot.figure(mask_values)
    pyplot.plot(x, without_isolation_y, color="red", label="Without Isolation")

    with_isolation_y: [float] = []
    for simulation_run in with_isolation:
        with_isolation_y.append(simulation_run.get_fitness_score()[constants.DAYS_SINCE_OUTBREAK])

    pyplot.figure(mask_values)
    pyplot.plot(x, with_isolation_y, color="blue", label="With Isolation")
    pyplot.legend()
    pyplot.xlabel("Mask Usage Percentage")
    pyplot.ylabel("Fitness Score")
    pyplot.title("Mask Usage Fitness")


def __draw_timestep_graphs(simulation_runs: List[SimulationRun]):
    counter: int = 0
    with_isolation = []
    without_isolation = []

    for simulation_run in simulation_runs:
        if simulation_run.get_mandatory_isolation():
            with_isolation.append(simulation_run)
        else:
            without_isolation.append(simulation_run)

    for simulation_run in with_isolation:
        counter += 1
        __plot_run_fitness_timestep(simulation_run, figure_with_isolation, counter)

    counter = 0

    for simulation_run in without_isolation:
        counter += 1
        __plot_run_fitness_timestep(simulation_run, figure_without_isolation, counter)


def __plot_run_fitness_timestep(simulation_run: SimulationRun, figure, counter):
    run_x = list(simulation_run.get_fitness_score().keys())
    run_y = list(simulation_run.get_fitness_score().values())
    pyplot.figure(figure)
    pyplot.plot(run_x, run_y, label=f"#{counter}")


def __plot_benchmark_fitness_timestep(simulation_runs: List[SimulationRun], figures: List[str]) -> None:
    benchmark_run: SimulationRun = simulation_runs[0]
    del simulation_runs[0]

    benchmark_x = list(benchmark_run.get_fitness_score().keys())
    benchmark_y = list(benchmark_run.get_fitness_score().values())

    for figure_name in figures:
        pyplot.figure(figure_name)
        pyplot.plot(benchmark_x, benchmark_y, color="red", linewidth=3, label="benchmark")
        pyplot.legend()
        pyplot.xlabel("Timestep")
        pyplot.ylabel("Fitness Score")
        pyplot.title(figure_name)

