class TiananmenSquareIncident:
    """
 The Tiananmen Square incident, also known as the June Fourth incident, was a student-led pro-democracy movement that took place in Beijing, China in 1989. The main features of the Tiananmen Square incident include:

 Student-led movement: The Tiananmen Square incident was largely led by university students who were protesting against the lack of democracy and political freedom in China.
 Non-violent protests: The protests were largely non-violent, with demonstrators engaging in hunger strikes, sit-ins, and peaceful marches.
 Government crackdown: The Chinese government responded to the protests with a brutal crackdown, including the use of the military to clear protesters from Tiananmen Square and the arrest and imprisonment of protesters and their supporters.
 Censorship: The Chinese government imposed strict censorship on news and media coverage of the protests, both domestically and internationally.
 International condemnation: The Tiananmen Square incident received widespread international attention and condemnation, with many countries and organizations calling for an end to the violence and repression.    
    """
    def __init__(self):
        self.protests = []
        self.student_led_movement = True
        self.non_violent_protests = True
        self.government_crackdown = True
        self.censorship = True
        self.international_condemnation = True
    
    def add_protest(self, protest):
        self.protests.append(protest)
    
    def set_student_led_movement(self, value):
        self.student_led_movement = value
    
    def set_non_violent_protests(self, value):
        self.non_violent_protests = value
    
    def set_government_crackdown(self, value):
        self.government_crackdown = value
    
    def set_censorship(self, value):
        self.censorship = value
    
    def set_international_condemnation(self, value):
        self.international_condemnation = value
