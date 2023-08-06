from politicsnlp.limited_power import *

class Government:
    def __init__(self):
        self.power = None
        
    def limit_power(self, power):
        # the government's power should be limited to the protection of individual rights
        self.power = LimitedPower(power)
        
    def protect_individual_rights(self, individual):
        # the government is responsible for protecting individual rights
        individual.protection.protect()
        
    def violate_individual_rights(self, individual):
        # individuals have the right to overthrow a government that fails to uphold its end of the social contract
        raise Exception("Individual rights have been violated. Right to revolution.")
    