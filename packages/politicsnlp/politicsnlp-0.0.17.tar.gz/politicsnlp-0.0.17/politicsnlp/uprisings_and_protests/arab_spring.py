class ArabSpring:
    """
    The Arab Spring was a series of uprisings and protests that took place in several Arab countries in North Africa and the Middle East from 2010 to 2012. The main features of the Arab Spring include:

    Popular protests: The Arab Spring was sparked by a wave of popular protests against authoritarian regimes, corruption, and economic hardship. The protests were often organized and led by youth movements and civil society groups.
    Social media: Social media played a key role in organizing and coordinating the protests, with activists using platforms like Facebook, Twitter, and YouTube to mobilize support and spread information.
    Repression: The governments of many Arab countries responded to the protests with a heavy-handed crackdown, including the use of riot police, military force, and censorship.
    International attention: The Arab Spring received widespread international attention, with many countries and organizations calling for an end to the violence and repression.
    Political change: The Arab Spring led to the overthrow of several long-standing authoritarian regimes, including those of Tunisia, Egypt, and Libya, and to significant political and social change in other countries in the region.
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
