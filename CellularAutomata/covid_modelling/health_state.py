import enum


class HealthState(enum.Enum):
    Recovered = 0
    Healthy = 1
    Infected = 2
    Dead = 3
