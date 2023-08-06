class Territory:
    """
Territory is a geographical area that is under the jurisdiction and control of a particular state or government. The main features of territory include:

Defined borders: A territory is defined by clear and recognized borders that separate it from neighboring areas.
Sovereignty: The state or government that controls a territory has full authority over it and can exercise its powers within that area.
Resources: A territory may contain valuable resources such as natural resources, strategic military locations, or cultural heritage sites.
Population: A territory may have a distinct population with its own culture, language, and traditions.
    """
    def __init__(self, borders, sovereignty, resources, population):
        self.borders = borders
        self.sovereignty = sovereignty
        self.resources = resources
        self.population = population
    
    def describe_borders(self):
        return f"A territory is defined by clear and recognized borders that separate it from neighboring areas."
    
    def describe_sovereignty(self):
        return f"The state or government that controls a territory has full authority over it and can exercise its powers within that area."
    
    def describe_resources(self):
        return f"A territory may contain valuable resources such as natural resources, strategic military locations, or cultural heritage sites."
    
    def describe_population(self):
        return f"A territory may have a distinct population with its own culture, language, and traditions."
