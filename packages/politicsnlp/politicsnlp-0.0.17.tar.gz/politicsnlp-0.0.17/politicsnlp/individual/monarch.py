class Monarch:
    def __init__(self, name, country):
        """
        - Authority: Monarchs have the ultimate authority in their respective countries. They hold the power to make final decisions on all matters of state, and their decisions are generally not subject to review or appeal.
        - Sovereignty: Monarchs are the highest authority in their countries, and their sovereignty extends over all aspects of governance, including the legislative, executive, and judicial branches.
        - Symbolic role: Monarchs also have a symbolic role in their countries, representing the national identity and tradition. They often serve as the head of state and participate in ceremonial and symbolic events.
        - Inheritance: Monarchy is a hereditary system of government, which means that the position of monarch is inherited by a member of the royal family, typically a son or daughter.
        - Continuity: Monarchs provide a sense of continuity and stability to their countries. They are often seen as the embodiment of the nation's history and traditions, and their long-term reigns provide a sense of stability and consistency.
        """
        self.name = name
        self.country = country
        self.authority = True
        self.sovereignty = True
        self.symbolic_role = True
        self.inheritance = True
        self.continuity = True

    def make_decision(self, decision):
        # Monarch makes a decision on a matter of state
        pass

    def attend_event(self, event):
        # Monarch attends a ceremonial or symbolic event
        pass
