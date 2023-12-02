import enum
from decimal import Decimal


class Variable(enum.Enum):
    HEALTH_EMPL_PERC = Decimal(
        1.75,
    )
    HEALTH_EMPLYR_PERC = Decimal(
        3.25,
    )
    HOUSING_PERC = Decimal(
        2.5,
    )
    NON_TAXABLE_VARIABLES = Decimal(
        88000,
    )
    FIRST_TAXABLE_VARIABLES = Decimal(
        300000,
    )
    SECOND_TAXABLE_VARIABLES = Decimal(
        500000,
    )
    THIRD_TAXABLE_VARIABLES = Decimal(
        1600000,
    )
    FOUR_TAXABLE_VARIABLES = Decimal(
        3200000,
    )
    THREE_K = Decimal(
        300000,
    )
    FIVE_K = Decimal(
        500000,
    )
    SIX_K = Decimal(
        600000,
    )
    ONE_ONE_M = Decimal(
        1100000,
    )
    ONE_SIX_M = Decimal(
        1600000,
    )
    THREE_TWO_M = Decimal(
        3200000,
    )
    SIX_FOUR_M = Decimal(
        6400000,
    )
    THREE_SIXTY = Decimal(360000)
    TWO_HUND = Decimal(200000)
    SEVENTY_K = Decimal(70000)
