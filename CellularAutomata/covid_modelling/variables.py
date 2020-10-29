from covid_modelling.constants import DAYS_SINCE_OUTBREAK

STEP_LIMIT: int = DAYS_SINCE_OUTBREAK  # Limit number of steps the simulation takes before evolving.
ADJUSTMENTS_ENABLED: bool = False
EVOLUTION_COMPLETE: bool = False

# These numbers have been calculating using the simulation_adjustments algorithm, and are set to give a result as close
# as possible to the real-world number of infected and dead people when MANDATORY_ISOLATION is enabled,
# PERCENTAGE_USING_MASKS = 0.22 and PERCENTAGE_SOCIAL_DISTANCING = 0.3.
INFECTION_CHANCE: float = 0.1953  # Percentage chance for a person to get infected when in contact with a sick person.
MORTALITY_CHANCE: float = 0.0275  # Modifier for checking if a person in a risk group will die from the virus
RECOVERY_CHANCE: float = 0.2  # Arbitrary number used for deciding if a person becomes healthy

PERCENTAGE_USING_MASKS: float = 0.22  # Percentage using masks. This is based on the number of people observed using face masks on public transport by FHI at 04.09.2020
PERCENTAGE_SOCIAL_DISTANCING: float = 0.3  # Percentage practicing social distance. This is a made up number as we found no data regarding how many are able to practice social distancing.
MANDATORY_ISOLATION: bool = True  # All people with symptoms are put in mandatory isolation
