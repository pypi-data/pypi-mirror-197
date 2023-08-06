class Crowd:
    """
    乌合之众（Crowd）和 The Masses 通常被用来描述一群人的行为和心态，但它们在概念上有所不同。

    乌合之众（Crowd）是指一群人在特定时间和地点聚集在一起，通常因为某种事件或活动，如政治集会、体育比赛、音乐会等。在这种情况下，个人的独立思考和行为往往被抛弃，人们更容易受到集体情绪和行为的影响，也更容易被煽动和操纵。乌合之众通常表现出情绪化、冲动、暴力和不稳定的特征。

    The Masses（群众）是一个更加广泛的概念，它可以指任何由许多人组成的社会群体。在政治上，群众通常被视为具有一定的政治力量和影响力，可以通过集体行动来推动政治变革和社会进步。相比于乌合之众，群众更具有自我意识和独立思考的能力，更能够对自己的行为和行动负责。

    People（人民）通常指的是一个国家或地区的公民，他们拥有政治权利和责任，并且能够通过投票和其他民主机制来参与政治决策。相比于群众和乌合之众，人民更具有集体意识和组织性，更能够自主地参与政治和社会事务，并对自己的未来有更多的掌控力。


    """
    def __init__(self, location, event):
        self.location = location
        self.event = event
        self.characteristics = []
    
    def add_characteristic(self, characteristic):
        self.characteristics.append(characteristic)
    
    def remove_characteristic(self, characteristic):
        self.characteristics.remove(characteristic)
    
    def describe(self):
        characteristics = ", ".join(self.characteristics)
        return f"The crowd is gathered in {self.location} for {self.event}, and typically exhibits characteristics of {characteristics}."
