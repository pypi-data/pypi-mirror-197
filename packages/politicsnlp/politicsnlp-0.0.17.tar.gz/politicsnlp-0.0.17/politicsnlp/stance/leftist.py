class Leftist:
    def __init__(self, name, principles):
        self.name = name
        self.principles = principles

    def organize(self):
        print(self.name + " is working to build a sustainable movement based on " + str(self.principles))

class LeftistOpportunism(Leftist):
    def __init__(self, name, principles):
        super().__init__(name, principles)
        self.allies = []

    def form_alliance(self, ally):
        self.allies.append(ally)

    def prioritize_tactics(self):
        print(self.name + " is focusing on short-term tactics to gain popularity and power, rather than building a sustainable movement based on " + str(self.principles))

    def compromise_principles(self):
        print(self.name + " is willing to compromise on " + str(self.principles) + " in order to achieve short-term gains and popularity")

    def prioritize_factionalism(self):
        print(self.name + " is prioritizing factional or ideological concerns over broader movement goals and the needs of the working class")

    def prioritize_elitism(self):
        print(self.name + " is prioritizing the interests of an intellectual or activist elite over the needs and concerns of the broader working class")
