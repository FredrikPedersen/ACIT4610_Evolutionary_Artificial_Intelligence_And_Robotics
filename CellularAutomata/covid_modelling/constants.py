# Infection Data Constants
AVERAGE_DURATION: int = 20  # On average, a person is recovered after 20 days of contracting the disease.
MAX_DURATION: int = 42  # Six weeks are the longest recorded cases of people being sick
INFECTIOUS_START: int = 3  # How many days after infection the disease becomes infectious
INCUBATION_DURATION: int = 5  # How many days before the virus gives symptoms

# Infection Class Constants
INCUBATION: str = "Incubation"
SYMPTOMS: str = "Symptoms"

# Simulation constants
AREA_DIMENSIONS: int = 100  # The simulation has nxn number of cells. AREA_DIMENSIONS = n.
DAYS_SINCE_OUTBREAK: int = 10  # We consider march 2nd as the pandemic start in Norway. Data was pulled 27.10.2020.
REPORTED_INFECTIONS: int = 17843
REPORTED_DEATHS: int = 279
INIT_INFECTION_PROBABILITY: float = 0.01  # Arbitrary number for setting number of initially infected when the simulation starts.
MASK_MEASURE: str = "Wearing Mask"
SOCIAL_DISTANCE_MEASURE: str = "Social Distancing"
ISOLATION_MEASURE: str = "Isolation"

MASK_REDUCTION: float = 0.35  # Approx risk reduction of using a mask
DISTANCING_REDUCTION: float = 0.5  # Couldn't find any hard data on how much a 1m social distance reduces self risk of infection. Varies between 40 - 80% depending on source and age group.
MORTAL_RISK_AGE: int = 65  # People aged over 65 are considered a risk group
MORTAL_RISK_GROUP_PERCENTAGE: float = 0.34  # Approx 1.85mil out of 5.433mil are in the risk-group based on their health conditions. This is not including people aged > 65
