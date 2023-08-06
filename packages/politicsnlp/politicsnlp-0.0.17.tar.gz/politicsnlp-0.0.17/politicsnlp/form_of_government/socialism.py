from politicsnlp.form_of_government.form_of_government import *

class Socialism(FormOfGovernment):
    """
    Socialism is a political and economic system that emphasizes collective ownership and control of the means of production and distribution of goods and services. The following are some common characteristics of socialism:

    - Collective ownership: Socialism emphasizes collective ownership of the means of production, including factories, land, and other resources, rather than private ownership.
    
    - Central planning: Socialism often involves central planning of the economy, with the government or a central planning agency making decisions about production and distribution.
    
    - Social welfare: Socialism emphasizes social welfare programs to ensure that everyone has access to basic necessities, such as housing, healthcare, and education.
    
    - Economic equality: Socialism seeks to reduce economic inequality by redistributing wealth and income from the wealthy to the less affluent members of society.
    """
    def __init__(self, name, power_structure, legitimacy, accountability, decision_making, collective_ownership, central_planning, social_welfare, economic_equality):
        super().__init__(name, power_structure, legitimacy, accountability, decision_making)
        self.collective_ownership = collective_ownership
        self.central_planning = central_planning
        self.social_welfare = social_welfare
        self.economic_equality = economic_equality

    def is_socialism(self):
        return True

    def has_collective_ownership(self):
        return self.collective_ownership

    def has_central_planning(self):
        return self.central_planning

    def emphasizes_social_welfare(self):
        return self.social_welfare

    def seeks_economic_equality(self):
        return self.economic_equality
