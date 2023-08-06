class Tyrant:
    """
    A tyrant, also known as a despot or autocrat, is a ruler who exercises absolute power and authority without any legal or constitutional constraints. The following are some common characteristics of a tyrant:

    - Authoritarian rule: A tyrant exercises authoritarian rule, where their power is absolute and unchecked. They may use force and coercion to maintain their power.
    
    - Lack of accountability: A tyrant is often not accountable to anyone and may act with impunity. They may not follow the rule of law and may use their power to oppress the people.
    
    - Suppression of opposition: A tyrant may suppress opposition, such as political dissidents, and may use violence or imprisonment to silence dissent.
    
    - Personal gain: A tyrant may use their power for personal gain, such as enriching themselves and their family, at the expense of the people.

    """
    def __init__(self, name, authoritarian_rule, lack_of_accountability, suppression_of_opposition, personal_gain):
        self.name = name
        self.authoritarian_rule = authoritarian_rule
        self.lack_of_accountability = lack_of_accountability
        self.suppression_of_opposition = suppression_of_opposition
        self.personal_gain = personal_gain

    def is_tyrant(self):
        return True

    def exercises_authoritarian_rule(self):
        return self.authoritarian_rule

    def lacks_accountability(self):
        return self.lack_of_accountability

    def suppresses_opposition(self):
        return self.suppression_of_opposition

    def seeks_personal_gain(self):
        return self.personal_gain
