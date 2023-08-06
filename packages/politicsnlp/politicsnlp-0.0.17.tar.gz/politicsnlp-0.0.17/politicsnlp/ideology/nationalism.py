from politicsnlp.ideology.ideology import *
class Nationalism(Ideology):
    """
    ### Characteristics of nationalism:

    - Belief in the superiority of one's own nation: Nationalists believe that their nation is superior to others and often promote the idea of national pride.

    - Advocacy for the interests of one's own nation: Nationalists prioritize the interests of their own nation above those of other nations and may advocate for policies that protect their nation's culture, economy, and security.

    - Focus on national unity: Nationalists emphasize the importance of national unity and may view diversity or minority groups as a threat to that unity.

    - Cultural identity: Nationalists often emphasize the importance of their nation's culture and may advocate for policies that preserve or promote that culture.
    
    - Strong national defense: Nationalists often believe in the importance of a strong military and may advocate for policies that increase military spending or expand their nation's military capabilities.


    """
    def __init__(self,name, worldview, normative, political, influential):
        super().__init__(name, worldview, normative, political, influential)
        self.superiority = True
        self.interests = True
        self.unity = True
        self.cultural_identity = True
        self.strong_defense = True
