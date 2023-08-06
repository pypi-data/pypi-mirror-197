class CivilWar:
    """
 In political science, a civil war is a violent conflict within a country between organized groups that are fighting for control of the government or for independence. Civil wars often arise from political, economic, or social grievances and are characterized by high levels of violence, population displacement, and economic disruption.
 ### Example:
 ```
 civil_war1 = CivilWar("Syria", ["Syrian government", "Rebel groups"], "Political grievances", "High", "Millions of people displaced", "Significant economic disruption")
 civil_war1.display_info()

 ```
    """
    def __init__(self, country, organized_groups, conflict_cause, violence_level, population_displacement, economic_disruption):
        self.country = country
        self.organized_groups = organized_groups
        self.conflict_cause = conflict_cause
        self.violence_level = violence_level
        self.population_displacement = population_displacement
        self.economic_disruption = economic_disruption

    def display_info(self):
        print(f"Country: {self.country}")
        print(f"Organized groups: {self.organized_groups}")
        print(f"Cause of conflict: {self.conflict_cause}")
        print(f"Violence level: {self.violence_level}")
        print(f"Population displacement: {self.population_displacement}")
        print(f"Economic disruption: {self.economic_disruption}")
