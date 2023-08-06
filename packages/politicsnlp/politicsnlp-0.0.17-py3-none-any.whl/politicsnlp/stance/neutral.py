class Neutral:
    """
To explain the characteristics of neutrality in English, neutrality refers to the objective and unbiased perspective, without taking sides or showing favoritism towards any particular person, group, or viewpoint. Neutral communication involves avoiding personal opinions, emotions, or judgments and instead presenting information in an impartial and factual manner. Key features of neutrality include:

Objectivity: A neutral person or communication should present facts and evidence in an objective manner, without any personal bias or emotional involvement.
Impartiality: Neutral communication should be free from any favoritism or prejudice towards any particular individual, group, or viewpoint.
Transparency: A neutral person or communication should be transparent about their sources and methods of information gathering and presenting.
Respectfulness: Neutral communication should be respectful towards all parties involved, avoiding any offensive or derogatory language.

    """
    def __init__(self, facts, sources):
        self.facts = facts
        self.sources = sources
        self.objectivity=True
        self.impartiality=True
        self.transparency=True
        self.respectfulness=True

    def present_information(self):
        for fact in self.facts:
            print(fact)
        print("Sources:")
        for source in self.sources:
            print(source)
