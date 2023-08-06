class Strongman:
    """
    A political strongman, also known as a political leader with a strong and authoritarian style of governance, is characterized by the following features:

    - Dominant and authoritarian leadership: A political strongman exercises a strong, domineering and authoritarian leadership style. They may not tolerate opposition and are often intolerant of dissenting views.
    
    - Control over the government: Political strongmen often have complete control over the government and its policies. They may use the state's institutions to maintain their hold on power.
    
    - Cult of personality: Political strongmen often promote a cult of personality and may use propaganda to create a favorable image of themselves in the media and public.
    
    - Lack of transparency and accountability: Political strongmen may lack transparency in their decision-making processes, and often refuse to be held accountable for their actions. They may also limit the role of independent institutions, such as the judiciary or the media, in order to maintain their hold on power.
    """
    def __init__(self, name, leadership_style, control_over_government, cult_of_personality, lack_of_transparency):
        self.name = name
        self.leadership_style = leadership_style
        self.control_over_government = control_over_government
        self.cult_of_personality = cult_of_personality
        self.lack_of_transparency = lack_of_transparency

    def is_political_strongman(self):
        return True

    def has_dominant_leadership(self):
        return self.leadership_style == 'dominant' or self.leadership_style == 'authoritarian'

    def controls_the_government(self):
        return self.control_over_government

    def promotes_cult_of_personality(self):
        return self.cult_of_personality

    def lacks_transparency_and_accountability(self):
        return self.lack_of_transparency
