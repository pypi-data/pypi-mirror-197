class Rightist:
    def __init__(self, name, principles):
        self.name = name
        self.principles = principles

    def promote_principles(self):
        print(self.name + " is promoting " + str(self.principles) + " as the foundation of their movement.")

class RightistCapitulationism(Rightist):
    """
Right-wing capitulationism, also known as right-wing opportunism or right-wing surrenderism, is a term used to describe a tendency among right-wing political groups to prioritize compromise with their opponents over maintaining their core principles and values. This often involves making concessions that are seen as pragmatic in the moment, but may ultimately undermine the movement's objectives. Some common features of right-wing capitulationism include:

Compromising principles: A willingness to compromise on core principles and values in order to achieve short-term gains or maintain power.
Opportunistic alliances: A willingness to form alliances with groups or individuals that do not share the same long-term goals or principles, but may offer short-term gains.
Focus on electability: A focus on winning elections at any cost, even if it means abandoning or watering down core principles and values.
Appeasement: A tendency to appease opponents or make concessions in order to avoid conflict or maintain power.
Lack of ideological consistency: A tendency to shift positions or adopt new stances depending on the political climate or to appeal to certain constituencies.
    """
    def __init__(self, name, principles):
        super().__init__(name, principles)
        self.allies = []

    def form_alliance(self, ally):
        self.allies.append(ally)

    def prioritize_electability(self):
        print(self.name + " is prioritizing electability at any cost, even if it means abandoning or watering down core principles and values.")

    def compromise_principles(self):
        print(self.name + " is willing to compromise on " + str(self.principles) + " in order to achieve short-term gains or maintain power.")

    def appease_opponents(self):
        print(self.name + " is appeasing opponents or making concessions in order to avoid conflict or maintain power.")

    def lack_ideological_consistency(self):
        print(self.name + " lacks ideological consistency, often shifting positions or adopting new stances depending on the political climate or to appeal to certain constituencies.")
