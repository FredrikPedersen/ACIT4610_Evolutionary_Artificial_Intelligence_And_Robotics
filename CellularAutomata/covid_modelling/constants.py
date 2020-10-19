# Infection constants
AVERAGE_DURATION: int = 20  # On average, a person is recovered after 20 days of contracting the disease.
MAX_DURATION: int = 42  # Six weeks are the longest recorded cases of people being sick
INFECTIOUS_START: int = 3   # How many days after infection the disease becomes infectious
INCUBATION_DURATION: int = 6    # How many days before the virus gives symptoms
RECOVERY_CHANCE: float = 0.2    # Arbitrary number used for deciding if a person becomes healthy

# Simulation constants
AREA_DIMENSIONS: int = 100  # The simulation has nxn number of cells. AREA_DIMENSIONS = n.
DAYS_SINCE_OUTBREAK: int = 10
INIT_INFECTION_PROBABILITY: float = 0.01    # Arbitrary number for setting number of initially infected when the simulation starts.

INFECTION_CHANCE: float = 0.1   # Percentage chance for a person to get infected when in contact with a sick person.
MORTALITY_CHANCE: float = 0.03   # Modifier for checking if a person in a risk group will die from the virus

MASK_REDUCTION: float = 0.35    # Approx risk reduction of using a mask
DISTANCING_REDUCTION: float = 0.5   # Couldn't find any hard data on how much a 1m social distance reduces self risk of infection. Varies between 40 - 80% depending on source and age group.
MORTAL_RISK_AGE: int = 65    # People aged over 65 are considered a risk group
MORTAL_RISK_GROUP_PERCENTAGE: float = 0.34     # Approx 1.85mil out of 5.433mil are in the risk-group based on their health conditions. This is not including people aged > 65
