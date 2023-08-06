class Populist:
    """
    #### A Populist class representing an individual or group promoting populism.

    Populism is an ideology that emphasizes the importance of the "common people" and their interests, often in opposition to a perceived elite or establishment. It can take various forms and exist on different sides of the political spectrum.

    Attributes:
    -----------
    anti_elitism : bool
        Whether the Populist opposes the perceived elite or establishment.
    pro_common_people : bool
        Whether the Populist supports the interests of the common people.
    political_spectrum : str
        The position of the Populist on the political spectrum (e.g., 'left', 'right', 'center').
    """

    def __init__(self, anti_elitism: bool = True, pro_common_people: bool = True, political_spectrum: str = 'center'):
        """
        Initializes a Populist instance with the given attributes.

        Parameters:
        -----------
        anti_elitism : bool, optional
            Whether the Populist opposes the perceived elite or establishment (default is True).
        pro_common_people : bool, optional
            Whether the Populist supports the interests of the common people (default is True).
        political_spectrum : str, optional
            The position of the Populist on the political spectrum (default is 'center').
        """
        self.anti_elitism = anti_elitism
        self.pro_common_people = pro_common_people
        self.political_spectrum = political_spectrum

    def __str__(self):
        return f"Populist on the {self.political_spectrum} side of the political spectrum"

    def advocate_for_common_people(self):
        """
        Advocates for the interests of the common people.

        This is a placeholder method representing actions that a Populist might take to promote the interests of the common people, such as advocating for policies that benefit the majority, fighting against perceived elitism, or challenging the status quo.
        """
        pass
