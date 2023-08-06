from politicsnlp.government import *

class SocialContract:
    def __init__(self, individuals):
        self.individuals = individuals
        self.government = None
        
    def create_government(self):
        # check if all individuals have agreed to the social contract
        if all([individual.agreed_to_social_contract for individual in self.individuals]):
            self.government = Government()
            return self.government
        else:
            raise Exception("All individuals must agree to the social contract to create a government.")
    