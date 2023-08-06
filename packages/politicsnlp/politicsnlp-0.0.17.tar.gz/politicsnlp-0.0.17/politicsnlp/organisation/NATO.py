class NATO:
    """
 As mentioned earlier, NATO (North Atlantic Treaty Organization) is a political and military organization between 30 North American and European countries. The main features of NATO include:

 Collective defense: The primary purpose of NATO is to provide collective defense and security for its member countries through military cooperation and joint defense planning.
 Military organization: NATO is a military organization with a permanent headquarters, military commands, and joint military exercises and training.
 Political alliance: NATO is also a political alliance, with member countries working together on issues of shared concern, such as counterterrorism, cyber security, and energy security.
 Democratic values: NATO member countries share common democratic values and principles, such as individual liberty, democracy, and the rule of law.
 Partnership: NATO has established partnerships with other countries and international organizations to promote peace, stability, and cooperation around the world.   
    """
    def __init__(self):
        self.member_countries = []
        self.collective_defense = True
        self.military_organization = True
        self.political_alliance = True
        self.shared_values = []
        self.partnerships = []
    
    def add_member_country(self, country):
        self.member_countries.append(country)
    
    def set_collective_defense(self, value):
        self.collective_defense = value
    
    def set_military_organization(self, value):
        self.military_organization = value
    
    def set_political_alliance(self, value):
        self.political_alliance = value
    
    def add_shared_value(self, value):
        self.shared_values.append(value)
    
    def add_partnership(self, partner):
        self.partnerships.append(partner)
