from politicsnlp.core.freedom import *

class FreedomOfSpeech(Freedom):
    """
    Freedom of speech, also known as freedom of expression, is a fundamental human right that allows individuals to express their opinions and ideas without fear of censorship, retaliation, or persecution. The main features of freedom of speech include:

    Protection from censorship: Individuals are free to express their views and opinions without fear of government censorship, retaliation, or persecution.
    Protection from punishment: Individuals are free to express their views and opinions without fear of legal or other forms of punishment, as long as they do not violate the rights of others or incite violence.
    Protection of diversity: Freedom of speech protects the right of individuals to express their opinions, even if they are unpopular, offensive, or contrary to the mainstream.
    Promotion of democracy: Freedom of speech is essential for the functioning of a democratic society, allowing individuals to participate in public debate and to hold those in power accountable.

    """
    def __init__(self, censorship, punishment, diversity, democracy,speech, religion, want, fear, indivisibility, universality, equality):
        super().__init__(speech, religion, want, fear, indivisibility, universality, equality, diversity)
        self.censorship = censorship
        self.punishment = punishment
        self.democracy = democracy
    
    def describe_censorship(self):
        return f"Freedom of speech protects individuals from government censorship, retaliation, or persecution."
    
    def describe_punishment(self):
        return f"Freedom of speech protects individuals from legal or other forms of punishment, as long as they do not violate the rights of others or incite violence."
    
    def describe_diversity(self):
        return f"Freedom of speech protects the right of individuals to express their opinions, even if they are unpopular, offensive, or contrary to the mainstream."
    
    def describe_democracy(self):
        return f"Freedom of speech is essential for the functioning of a democratic society, allowing individuals to participate in public debate and to hold those in power accountable."
