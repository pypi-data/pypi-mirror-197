class UKIP:
    """
The UK Independence Party (UKIP) is a right-wing populist and Eurosceptic political party in the United Kingdom. It was founded in 1993 and gained momentum in the early 2000s as a protest against European integration, immigration, and what it sees as a loss of British sovereignty. Here are some of the key features of the UK Independence Party:

Euroscepticism: UKIP is strongly opposed to the UK's membership of the European Union, and has campaigned for the UK to leave the EU in several referendums and elections.
Anti-immigration: UKIP is also known for its hardline stance on immigration. It advocates for tighter border controls and restrictions on the rights of immigrants, particularly those from non-European countries.
Nationalism: UKIP promotes a sense of British nationalism and is critical of what it perceives as a dilution of British culture and identity through immigration and European integration.
Populism: UKIP has been known to use populist rhetoric to appeal to disaffected voters. It often presents itself as the voice of the "ordinary people" and portrays the political establishment as out of touch with the concerns of ordinary citizens.
    
    """
    def __init__(self, name, eurosceptic, anti_immigration, nationalist, populist):
        self.name = name
        self.eurosceptic = eurosceptic
        self.anti_immigration = anti_immigration
        self.nationalist = nationalist
        self.populist = populist

    def get_name(self):
        return self.name

    def is_eurosceptic(self):
        return self.eurosceptic

    def is_anti_immigration(self):
        return self.anti_immigration

    def is_nationalist(self):
        return self.nationalist

    def is_populist(self):
        return self.populist
