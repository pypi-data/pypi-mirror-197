class PeoplesCongressSystem:
    """
    The People's Congress system, also known as the system of people's congresses, is a political system used in the People's Republic of China and other countries. The main features of the People's Congress system include:

    - Multi-level representative bodies: The system consists of multi-level representative bodies, including the National People's Congress, provincial-level people's congresses, and local-level people's congresses.
    
    - Direct and indirect elections: Members of the people's congresses are elected through direct and indirect elections, with voters electing representatives at the local level who then go on to elect representatives at higher levels.

    - Legislative and oversight functions: The people's congresses have both legislative and oversight functions, including the power to make laws, approve budgets, and supervise the work of government officials.
    
    - Party-led system: The People's Congress system is part of a larger party-led system, with the Chinese Communist Party playing a dominant role in the selection and appointment of officials at all levels.
    """
    def __init__(self, multi_level_bodies, direct_indirect_elections, legislative_oversight, party_led_system):
        self.multi_level_bodies = multi_level_bodies
        self.direct_indirect_elections = direct_indirect_elections
        self.legislative_oversight = legislative_oversight
        self.party_led_system = party_led_system
    
    def describe_multi_level_bodies(self):
        return f"The system consists of multi-level representative bodies, including the National People's Congress, provincial-level people's congresses, and local-level people's congresses."
    
    def describe_direct_indirect_elections(self):
        return f"Members of the people's congresses are elected through direct and indirect elections, with voters electing representatives at the local level who then go on to elect representatives at higher levels."
    
    def describe_legislative_oversight(self):
        return f"The people's congresses have both legislative and oversight functions, including the power to make laws, approve budgets, and supervise the work of government officials."
    
    def describe_party_led_system(self):
        return f"The People's Congress system is part of a larger party-led system, with the Chinese Communist Party playing a dominant role in the selection and appointment of officials at all levels."
