class Populism:
    """
Populism is a political ideology that emphasizes the interests and perspectives of ordinary people, often characterized as the "silent majority," against those of the elite or ruling class. Here are some common characteristics of populism:

Anti-elitism: Populists often reject the political establishment and criticize the elite for being out of touch with the concerns of ordinary people.
Nationalism: Populists may promote a strong sense of national identity and prioritize the interests of their country over international cooperation.
Simplistic solutions: Populists may offer simple and straightforward solutions to complex social, economic, and political problems, often blaming specific groups (e.g., immigrants, the media, globalists) for these issues.
Appeals to emotion: Populists may use emotional appeals to rally support, rather than relying on rational argumentation.
Authoritarianism: Populists may reject the separation of powers, the rule of law, and other democratic institutions, instead favoring a strong and decisive leader who can enact their agenda.    
    """
    def __init__(self, anti_elitism=True, nationalism=True, simplistic_solutions=True, appeals_to_emotion=True, authoritarianism=True):
        self.anti_elitism = anti_elitism
        self.nationalism = nationalism
        self.simplistic_solutions = simplistic_solutions
        self.appeals_to_emotion = appeals_to_emotion
        self.authoritarianism = authoritarianism

    def describe(self):
        description = "This ideology exhibits the following characteristics:\n"
        if self.anti_elitism:
            description += "- Anti-elitism\n"
        if self.nationalism:
            description += "- Nationalism\n"
        if self.simplistic_solutions:
            description += "- Simplistic solutions\n"
        if self.appeals_to_emotion:
            description += "- Appeals to emotion\n"
        if self.authoritarianism:
            description += "- Authoritarianism\n"
        return description
