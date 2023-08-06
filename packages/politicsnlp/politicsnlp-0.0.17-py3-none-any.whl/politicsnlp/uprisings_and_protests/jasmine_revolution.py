class JasmineRevolution:
    """
 The Jasmine Revolution was a series of protests and uprisings that took place in Tunisia from December 2010 to January 2011. The main features of the revolution include:

 Popular protests: The Jasmine Revolution was sparked by a popular uprising against the government of President Zine El Abidine Ben Ali. The protests were initially sparked by the self-immolation of a street vendor, Mohamed Bouazizi, who set himself on fire in protest against police harassment.
 Social media: Social media played a key role in organizing and coordinating the protests, with activists using platforms like Facebook and Twitter to mobilize support and spread information.
 Repression: The government responded to the protests with a heavy-handed crackdown, including the use of riot police and the arrest and detention of protesters and journalists.
 International attention: The revolution received widespread international attention, with many countries and organizations calling for an end to the violence and repression.
 Political change: The Jasmine Revolution ultimately led to the overthrow of President Ben Ali and the establishment of a new government.
    """
    def __init__(self):
        self.protests = []
        self.social_media = True
        self.repression = True
        self.international_attention = True
        self.political_change = True
    
    def add_protest(self, protest):
        self.protests.append(protest)
    
    def set_social_media(self, value):
        self.social_media = value
    
    def set_repression(self, value):
        self.repression = value
    
    def set_international_attention(self, value):
        self.international_attention = value
    
    def set_political_change(self, value):
        self.political_change = value
