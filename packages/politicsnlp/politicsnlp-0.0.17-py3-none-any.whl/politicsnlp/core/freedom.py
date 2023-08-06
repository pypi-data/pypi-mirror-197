from politicsnlp.core.natural_rights import *

class Freedom(NaturalRights):
    def __init__(self,speech, religion, want, fear, indivisibility, universality, equality, diversity):
        super().__init__(indivisibility, universality, equality, diversity)

        self.speech = speech
        self.religion = religion
        self.want = want
        self.fear = fear

