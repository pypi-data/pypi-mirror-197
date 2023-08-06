class BlankRevolution:
    """
 The Blank Revolution, also known as the White Revolution, was a series of protests and uprisings that took place in Lebanon in 2005. The main features of the Blank Revolution include:

 Peaceful protests: The Blank Revolution was marked by a series of peaceful protests and demonstrations, with protesters carrying blank sheets of paper to symbolize their demands for a clean slate and a new government.
 Non-violent resistance: The protesters used non-violent methods of resistance, including sit-ins, marches, and civil disobedience, to demand political and social change.
 Youth-led movement: The Blank Revolution was largely led by youth activists and civil society groups, who mobilized support through social media and other forms of communication.
 Political change: The Blank Revolution led to the withdrawal of Syrian troops from Lebanon and to significant political and social change in the country.
    
    """
    def __init__(self):
        self.protests = []
        self.non_violent_resistance = True
        self.youth_led_movement = True
        self.political_change = True
    
    def add_protest(self, protest):
        self.protests.append(protest)
    
    def set_non_violent_resistance(self, value):
        self.non_violent_resistance = value
    
    def set_youth_led_movement(self, value):
        self.youth_led_movement = value
    
    def set_political_change(self, value):
        self.political_change = value
