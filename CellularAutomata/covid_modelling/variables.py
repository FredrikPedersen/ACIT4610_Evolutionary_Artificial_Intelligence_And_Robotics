from covid_modelling.constants import DAYS_SINCE_OUTBREAK

STEP_LIMIT: int = DAYS_SINCE_OUTBREAK  # Limit number of steps the simulation takes before evolving.
ADJUSTMENTS_COMPLETE: bool = False

INFECTION_CHANCE: float = 0.2  # Percentage chance for a person to get infected when in contact with a sick person.
MORTALITY_CHANCE: float = 0.03  # Modifier for checking if a person in a risk group will die from the virus
RECOVERY_CHANCE: float = 0.2  # Arbitrary number used for deciding if a person becomes healthy
PERCENTAGE_USING_MASKS: float = 0.1  # Percentage using masks. This is a made up number.
PERCENTAGE_SOCIAL_DISTANCING: float = 0.1  # Percentage practicing social distance. This is a made up number.
MANDATORY_ISOLATION: bool = True  # All people with symptoms are put in mandatory isolation
