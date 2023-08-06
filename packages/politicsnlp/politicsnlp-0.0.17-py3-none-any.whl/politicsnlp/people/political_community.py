class PoliticalCommunity:
    """
 In political science, a community of shared identity or commonality, also known as a political community, refers to a group of individuals who share a common sense of belonging and identity based on shared cultural, social, or historical factors. The main features of a political community include:

 Shared identity: Members of a political community share a common sense of identity and belonging, based on shared cultural, social, or historical factors.
 Political organization: A political community has a formal or informal political organization, such as a government, that represents and governs the community.
 Common interests: Members of a political community share common interests and goals, which may include economic, social, or political objectives.
 Solidarity: Members of a political community have a sense of solidarity and mutual obligation towards one another, based on their shared identity and common interests.
 Shared values: A political community may have shared values, such as democracy, freedom, or human rights, that are reflected in their political organization and decision-making.    
    """
    def __init__(self, name):
        self.name = name
        self.members = []
        self.political_organization = True
        self.common_interests = []
        self.solidarity = True
        self.shared_values = []
    
    def add_member(self, member):
        self.members.append(member)
    
    def set_political_organization(self, value):
        self.political_organization = value
    
    def add_common_interest(self, interest):
        self.common_interests.append(interest)
    
    def set_solidarity(self, value):
        self.solidarity = value
    
    def add_shared_value(self, value):
        self.shared_values.append(value)
