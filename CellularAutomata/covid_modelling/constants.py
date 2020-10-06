# Infection constants
AVERAGE_DURATION: int = 20  # On average, a person is recovered after 20 days of contracting the disease.
MAX_DURATION: int = 42  # Six weeks are the longest recorded cases of people being sick
INFECTIOUS_START: int = 3
INCUBATION_DURATION: int = 6
RECOVERY_CHANCE: float = 0.4    # Arbitrary number used for deciding if a person becomes healthy

# Simulation constants
AREA_DIMENSIONS: int = 50
INIT_INFECTION_PROBABILITY: float = 0.01
INFECTION_RATE: float = 0.5
MORTALITY_RATE: float = 0.018   # Approx. mortality rate in Norway
