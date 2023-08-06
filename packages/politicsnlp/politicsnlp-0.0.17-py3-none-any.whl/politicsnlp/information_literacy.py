class InformationLiteracy:
    """
Information literacy refers to the ability to identify, locate, evaluate, and effectively use information. Here are some key features of information literacy:

The ability to determine the nature and extent of the information needed.
The ability to access information effectively and efficiently.
The ability to evaluate information and its sources critically.
The ability to use information effectively to accomplish a specific purpose.
The ability to understand the economic, legal, and social issues surrounding the use of information, and to access and use information ethically and legally.    
    """
    def __init__(self):
        self.information_needed = ""
        self.information_sources = []
        self.information_evaluation = False
        self.information_use = ""
        self.information_ethics = ""

    def determine_information_needed(self, info):
        self.information_needed = info

    def access_information(self, sources):
        self.information_sources = sources

    def evaluate_information(self, evaluation):
        self.information_evaluation = evaluation

    def use_information(self, use):
        self.information_use = use

    def understand_information_ethics(self, ethics):
        self.information_ethics = ethics
