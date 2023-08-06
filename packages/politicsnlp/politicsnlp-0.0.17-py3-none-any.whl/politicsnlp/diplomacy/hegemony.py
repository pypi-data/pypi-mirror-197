class Hegemony:
    """
    Hegemony is a term that refers to a dominant influence or leadership of one state, group, or culture over others. It can be characterized by several features, including:

    Control or domination: Hegemony involves the ability to control or dominate others, either through military, economic, or cultural means.
    Consent and cooperation: The hegemonic power is able to maintain its dominance through the voluntary consent and cooperation of others, rather than relying solely on coercion.
    Ideological justification: Hegemony is often accompanied by an ideological justification that presents the hegemonic power as a natural or necessary leader.
    Cultural hegemony: Hegemony can extend beyond political and economic spheres to encompass cultural influence, such as language, art, and media.
    """
    def __init__(self, hegemonic_power, controlled_states,consent,cultural_hegemony):
        self.hegemonic_power = hegemonic_power
        self.controlled_states = controlled_states
        self.consent=consent
        self.cultural_hegemony=cultural_hegemony
    
    def is_hegemonic(self, state):
        return state in self.controlled_states
    
    def ideological_justification(self):
        return f"{self.hegemonic_power} is the natural leader of the {self.controlled_states} because of its superior."
    
    def cultural_influence(self, medium):
        return f"{self.hegemonic_power} has a strong {medium} presence in the {self.controlled_states}, shaping the culture and values of its people."
