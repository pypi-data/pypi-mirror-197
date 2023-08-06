class Centralization:
    """
Centralized power or centralization is a system of government in which power and decision-making authority is concentrated in the hands of a central authority or government. The main features of centralization include:

Concentration of power: In a centralized system, power is concentrated in the hands of a single central authority, such as a national government or a ruling party.
Uniformity: Centralization often leads to a uniform approach to policy-making and governance, with decisions made at the center being applied uniformly across the country.
Control: The central authority has greater control over the various regions and populations within the country, with decisions made at the center being binding on all.
Limited local autonomy: In a centralized system, local authorities or regional governments may have limited autonomy to make decisions or implement policies that deviate from the central authority's directives.

    """
    def __init__(self, concentration_of_power, uniformity, control, limited_local_autonomy):
        self.concentration_of_power = concentration_of_power
        self.uniformity = uniformity
        self.control = control
        self.limited_local_autonomy = limited_local_autonomy
    
    def describe_concentration_of_power(self):
        return f"In a centralized system, power is concentrated in the hands of a single central authority, such as a national government or a ruling party."
    
    def describe_uniformity(self):
        return f"Centralization often leads to a uniform approach to policy-making and governance, with decisions made at the center being applied uniformly across the country."
    
    def describe_control(self):
        return f"The central authority has greater control over the various regions and populations within the country, with decisions made at the center being binding on all."
    
    def describe_limited_local_autonomy(self):
        return f"In a centralized system, local authorities or regional governments may have limited autonomy to make decisions or implement policies that deviate from the central authority's directives."
