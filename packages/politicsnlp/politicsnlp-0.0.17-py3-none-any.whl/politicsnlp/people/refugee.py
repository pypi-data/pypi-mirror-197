class Refugee:
    """
 In political science, a refugee is defined as an individual who has been forced to flee their country of origin due to a well-founded fear of persecution based on their race, religion, nationality, political opinion, or membership in a particular social group. Refugees often face significant legal, economic, and social challenges in their host countries and are entitled to certain legal protections under international law.
 ### Example:
 ```
 refugee1 = Refugee("Syria", "Well-founded fear of persecution", "Religion", "Entitled to legal protections under international law")
 refugee1.display_info()
 
 ```   
    """
    def __init__(self, country_of_origin, fear_of_persecution, persecution_basis, legal_protections):
        self.country_of_origin = country_of_origin
        self.fear_of_persecution = fear_of_persecution
        self.persecution_basis = persecution_basis
        self.legal_protections = legal_protections

    def display_info(self):
        print(f"Country of origin: {self.country_of_origin}")
        print(f"Fear of persecution: {self.fear_of_persecution}")
        print(f"Basis of persecution: {self.persecution_basis}")
        print(f"Legal protections: {self.legal_protections}")
