from covid_modelling.constants import DAYS_SINCE_OUTBREAK

STEP_LIMIT: int = DAYS_SINCE_OUTBREAK  # Limit number of steps the simulation takes before evolving.

INFECTION_CHANCE: float = 0.3  # Percentage chance for a person to get infected when in contact with a sick person.
MORTALITY_CHANCE: float = 0.05  # Modifier for checking if a person in a risk group will die from the virus
RECOVERY_CHANCE: float = 0.2  # Arbitrary number used for deciding if a person becomes healthy
PERCENTAGE_USING_MASKS: float = 0.3  # Percentage using masks. This is a made up number.
