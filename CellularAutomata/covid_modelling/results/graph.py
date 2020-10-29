from typing import List

import matplotlib.pyplot as pyplot

from covid_modelling.results.simulation_run import SimulationRun



def draw_result_graphs(simulation_runs: List[SimulationRun]):
    figure_without_isolation: str = "Without Isolation"
    figure_with_isolation: str = "With Isolation"
    counter: int = 0

    #simulation_runs.sort(key=lambda x: x.get_mandatory_isolation())

    __plot_benchmark_fitness_timestep(simulation_runs, [figure_without_isolation, figure_with_isolation])
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
    pyplot.legend()

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
