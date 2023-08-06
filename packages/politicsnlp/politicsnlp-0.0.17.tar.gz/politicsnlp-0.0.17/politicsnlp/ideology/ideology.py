class Ideology:
    """
    Ideology is a set of ideas and beliefs about how society should be organized and how power should be distributed. The following are some common characteristics of ideology:

    - Comprehensive worldview: Ideology provides a comprehensive and systematic worldview that explains the nature of society, politics, and human relationships. It offers a set of ideas and beliefs that guide the actions of individuals and groups.
    
    - Normative: Ideology is normative in nature, meaning it provides a vision of what should be, rather than what is. It offers a set of moral and ethical principles that guide political action.
    
    - Political: Ideology is political in nature, meaning it provides a framework for understanding and engaging in political action. It offers a set of ideas and beliefs about the proper role and function of government and other political institutions.
    
    - Influential: Ideology is influential, meaning it can shape political behavior and policy outcomes. It can mobilize individuals and groups to take political action and can influence the decisions of policymakers.

    """
    def __init__(self, name, worldview, normative, political, influential):
        self.name = name
        self.worldview = worldview
        self.normative = normative
        self.political = political
        self.influential = influential

    def is_ideology(self):
        return True

    def provides_comprehensive_worldview(self):
        return self.worldview

    def is_normative(self):
        return self.normative

    def is_political(self):
        return self.political

    def is_influential(self):
        return self.influential
