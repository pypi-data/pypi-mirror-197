class FormOfGovernment:
    """
    Form of government refers to the way in which power is organized and exercised within a political system. The following are some common characteristics of form of government:

    ower structure: Form of government determines the structure of power within a political system, including the roles and responsibilities of different institutions and individuals.
    Legitimacy: Form of government is based on a certain level of legitimacy, which refers to the degree to which the people accept and support the government's authority.
    Accountability: Form of government determines the degree to which those in power are held accountable for their actions, and the mechanisms through which such accountability is enforced.
    Decision-making processes: Form of government determines the processes through which political decisions are made, including the level of participation and representation of citizens in the decision-making process.
    """
    def __init__(self, name, power_structure, legitimacy, accountability, decision_making):
        self.name = name
        self.power_structure = power_structure
        self.legitimacy = legitimacy
        self.accountability = accountability
        self.decision_making = decision_making

    def is_form_of_government(self):
        return True

    def has_power_structure(self):
        return self.power_structure

    def is_legitimate(self):
        return self.legitimacy

    def has_accountability(self):
        return self.accountability

    def has_decision_making_process(self):
        return self.decision_making
