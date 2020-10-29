from enum import Enum


class HealthState(Enum):
    Recovered = 0
    Healthy = 1
    Infected = 2
    Dead = 3
