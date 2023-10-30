from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from configs import Variable as var  # noqa: N813

month_date = datetime.strftime(datetime.now(), "%B")


@dataclass
class Grade:
    """This class calculate the"""

    gross: Decimal = field(default=0.0)  # type: ignore
    water_fee: Decimal = field(default=150)  # type: ignore
    health_ins: bool | None = field(default=False)
    contrib: bool | None = field(default=False)

    def get_annual_gross(self) -> Decimal:
        return Decimal(self.gross * 12)

    def _get_basic(self) -> int:
        return self.get_annual_gross() * 40 / 100  # type: ignore

    def _get_transport(self) -> int:
        return self.get_annual_gross() * 10 / 100  # type: ignore

    def _get_housing(self) -> int:
        return self.get_annual_gross() * 10 / 100  # type: ignore

    def get_health_empl(
        self,
    ) -> Decimal:
        if self.health_ins:
            return self.gross * var.HEALTH_EMPL_PERC.value / 100
        return Decimal(0.0)

    def get_health_emplyr(
        self,
    ) -> Decimal:
        if self.health_ins:
            return self.gross * var.HEALTH_EMPLYR_PERC.value / 100
        return Decimal(0.0)

    def get_health_ins(
        self,
    ) -> Decimal:
        return self.get_health_empl() + self.get_health_emplyr()

    def get_bht(self) -> Decimal:
        return self._get_basic() + self._get_housing() + self._get_transport()  # type: ignore

    def get_pension_employees(self) -> Decimal:
        if self.get_annual_gross() <= var.THREE_SIXTY.value:
            return 0.0  # type: ignore
        if self.contrib is True:
            return self.get_bht() * 8 / 100
        return self.get_bht() * 18 / 100  # type: ignore

    def get_pension_employer(self) -> Decimal:
        if self.get_annual_gross() <= var.THREE_SIXTY.value:
            return 0.0  # type: ignore
        if self.contrib is True:
            return self.get_bht() * 10 / 100  # type: ignore
        return Decimal(0.0)  # type: ignore

    def get_total_pension(self) -> Decimal:
        return self.get_pension_employees() + self.get_pension_employer()

    def pension_logic(self) -> Decimal:
        if self.get_annual_gross() <= var.THREE_SIXTY.value:
            return 0.0  # type: ignore
        return self.get_pension_employees()

    def get_housing(self):
        return self.gross * var.HOUSING_PERC.value / 100

    def get_gross_income(self) -> Decimal:
        return Decimal(self.get_annual_gross()) - Decimal(self.pension_logic())

    def _twenty_percents(self) -> Decimal:
        return self.get_gross_income() * 20 / 100

    def get_consolidated(self) -> Decimal:
        if self.get_gross_income() * 1 / 100 > var.TWO_HUND.value:
            return self.get_gross_income() * 1 / 100
        return var.TWO_HUND.value  # type: ignore

    def get_consolidated_relief(self) -> Decimal:
        return self.get_consolidated() + self._twenty_percents()

    def get_taxable_income(self) -> Decimal:
        calc = (
            Decimal(self.get_annual_gross())
            - Decimal(self.get_consolidated_relief())
            - Decimal(self.get_pension_employees())
        )
        if calc <= 0:
            return Decimal(0.0)
        return calc

    """
        ----------------------------------------------------------------------------------------------------------
        THis Part of the code calculate for the Payee of,
        employee according to the New Finance act
        first #300,000 == 7%
        next #300,000 == 11%
        next #500,000 == 15%
        next #500,000 == 19%
        next #1,600,000 == 21%
        above #3,200,000 == 24%
        ----------------------------------------------------------------------------------------------------------
    """

    # calculate for employee who earn #30,000 and below,
    #  who are not eligible for Income tax deduction
    def first_taxable(self) -> Decimal:  # type: ignore
        if self.get_taxable_income() <= var.NON_TAXABLE_VARIABLES.value:
            return 0  # type: ignore
        return Decimal(0.0)

    # calculate for the first #300,000:00 or less of taxable income
    def second_taxable(self) -> Decimal:  # type: ignore
        if self.get_taxable_income() < var.FIRST_TAXABLE_VARIABLES.value:
            return Decimal(self.get_taxable_income()) * 7 / 100
        elif (  # noqa: RET505
            self.get_taxable_income() >= var.FIRST_TAXABLE_VARIABLES.value
        ):  # noqa: RET505
            return Decimal(var.FIRST_TAXABLE_VARIABLES.value * 7 / 100)
        return Decimal(0.0)

    # calculate for the second #300,000:00 or less of taxable income
    def third_taxable(self) -> Decimal:  # type: ignore
        if (
            self.get_taxable_income() - var.FIRST_TAXABLE_VARIABLES.value
        ) >= var.FIRST_TAXABLE_VARIABLES.value:
            return Decimal(300000 * 11 / 100)

        elif (  # noqa: RET505
            self.get_taxable_income() - var.FIRST_TAXABLE_VARIABLES.value
        ) <= var.FIRST_TAXABLE_VARIABLES.value:
            return (
                Decimal(self.get_taxable_income() - var.FIRST_TAXABLE_VARIABLES.value)
                * 11
                / 100
            )
        return Decimal(0)

    # calculate for taxable income reminning after the #600,000 deduction,
    # #500,000:00 or less of taxable income
    def fourth_taxable(self) -> Decimal:  # type: ignore
        if (self.get_taxable_income() - var.SIX_K.value) >= var.FIVE_K.value:
            return Decimal(var.SIX_K.value * 15 / 100)

        elif (  # noqa: RET505
            self.get_taxable_income() - var.SIX_K.value
        ) <= var.FIVE_K.value:  # noqa: RET505
            return Decimal(self.get_taxable_income() - var.SIX_K.value) * 15 / 100
        return None  # type: ignore

    # calculate for taxable income reminning after the #1,100,000 deduction,
    # second #500,000:00 or less of taxable income
    def fifth_taxable(self) -> Decimal:  # type: ignore
        if self.get_taxable_income() - var.ONE_ONE_M.value >= var.SIX_K.value:
            return Decimal(var.SIX_K.value * 19 / 100)
        elif (  # noqa: RET505
            self.get_taxable_income() - var.ONE_ONE_M.value
        ) < var.SIX_K.value:  # noqa: RET505
            return Decimal(self.get_taxable_income() - var.ONE_ONE_M.value) * 19 / 100
        return None  # type: ignore

    # calculate for taxable income reminning after the #1,600,000 deduction,
    # #1,600,000:00 or less of taxable income
    def sixth_taxable(self) -> Decimal:  # type: ignore
        if self.get_taxable_income() - var.ONE_SIX_M.value >= var.ONE_SIX_M.value:
            return Decimal(var.ONE_SIX_M.value * 21 / 100)

        elif (  # noqa: RET505
            self.get_taxable_income() - var.ONE_SIX_M.value
        ) < var.ONE_SIX_M.value:  # noqa: RET505
            return Decimal(self.get_taxable_income() - var.ONE_SIX_M.value) * 21 / 100
        elif Decimal(self.get_taxable_income() - var.ONE_SIX_M.value) <= 0:
            return 0  # type: ignore
        return None  # type: ignore

    # calculate for taxable income reminning after the #3,200,000 deduction,
    # #3,200,000:00 or less of taxable income
    def seventh_taxable(self) -> Decimal:  # type: ignore
        if self.get_taxable_income() - var.THREE_TWO_M.value > var.THREE_TWO_M.value:
            return Decimal(
                (self.get_taxable_income() - var.THREE_TWO_M.value) * 24 / 100
            )
        elif (  # noqa: RET505
            self.get_taxable_income() - var.THREE_TWO_M.value
        ) < var.THREE_TWO_M.value:
            return Decimal(
                (self.get_taxable_income() - var.THREE_TWO_M.value) * 24 / 100
            )
        return None  # type: ignore

    def payee_logic(self) -> Decimal:  # type: ignore  # noqa: PLR0911
        if self.get_taxable_income() <= var.NON_TAXABLE_VARIABLES.value:
            return Decimal(0.0)
        elif (  # noqa: RET505
            self.get_taxable_income() <= var.FIRST_TAXABLE_VARIABLES.value
        ):  # noqa: RET505
            return self.second_taxable()
        elif (
            self.get_taxable_income() >= var.FIRST_TAXABLE_VARIABLES.value
            and self.get_taxable_income() < var.SIX_K.value
        ):
            return round(self.second_taxable() + self.third_taxable(), 2)
        elif (
            self.get_taxable_income() >= var.FIRST_TAXABLE_VARIABLES.value
            and self.get_taxable_income() >= var.SIX_K.value
            and self.get_taxable_income() < var.ONE_ONE_M.value
        ):
            return round(
                self.second_taxable() + self.third_taxable() + self.fourth_taxable(),
                2,
            )
        elif (
            self.get_taxable_income() >= var.ONE_ONE_M.value
            and self.get_taxable_income() < var.ONE_SIX_M.value
        ):
            return round(
                self.second_taxable()
                + self.third_taxable()
                + self.fourth_taxable()
                + self.fifth_taxable(),
                2,
            )
        elif (
            self.get_taxable_income() >= var.ONE_SIX_M.value
            and self.get_taxable_income() < var.THREE_TWO_M.value
        ):
            return round(
                self.second_taxable()
                + self.third_taxable()
                + self.fourth_taxable()
                + self.fifth_taxable()
                + self.sixth_taxable(),
                2,
            )
        elif self.get_taxable_income() >= var.THREE_TWO_M.value:
            return round(
                self.second_taxable()
                + self.third_taxable()
                + self.fourth_taxable()
                + self.fifth_taxable()
                + self.sixth_taxable()
                + self.seventh_taxable(),
                2,
            )
        return None  # type: ignore

    def get_water_fee(self) -> Decimal:
        if self.gross < var.SEVENTY_K.value:
            return self.water_fee
        else:  # noqa: RET505
            return Decimal(200)

    def monthly_payee(self) -> Decimal:
        return round(self.payee_logic() / 12, 2)

    def get_net_pay(self) -> Decimal:
        if (self.get_gross_income()) - (self.payee_logic()) - self.get_water_fee() <= 0:
            return self.gross
        return round(
            (self.get_gross_income() / 12)
            - (self.payee_logic() / 12)
            - (self.get_health_empl() / 12)
            - (self.get_housing())
            - self.get_water_fee(),
            2,
        )

    def __str__(self) -> str:
        return f"your salary for the month of {month_date} is {self.gross} and your \
                    net pay is {self.get_net_pay():,.2f}\
                    and your PAYEE for the month is {self.payee_logic()/12:,.2f}"


if __name__ == "__main__":
    salary = int(input("enter your salary: "))
    emp = Grade(gross=salary, health_ins=False, contrib=True)  # type: ignore
    print(emp.__str__())
    print(f"Annual Income: ₦{emp.get_annual_gross():,.2f}")
    print(f"Water: ₦{emp.get_water_fee():,.2f}")
    print(f"housing: ₦{emp.get_housing():,.2f}")
    print(f"health: ₦{emp.get_health_empl()/12:,.2f}")
    print(f"EMplyee Pension Contribution: ₦{emp.get_pension_employees()/12:,.2f}")
    print(f"employers pension contribution: ₦{emp.get_pension_employer()/12:,.2f}")
    print(f"employee Gross income: ₦{emp.get_gross_income()/12:,.2f}")
    print(f"net pay for the year: ₦{emp.get_net_pay()*12:,.2f}")
