class PoliticalRegime:
    """
A political regime or government is a system of authority and power that governs a state or society. The main features of a political regime include:

Legitimacy: A political regime must be seen as legitimate by the population and other actors, such as international organizations or other states.
Power and authority: A political regime must have the power and authority to make decisions and enforce laws and policies.
Control of territory: A political regime must control a specific territory, either through direct or indirect means.
Decision-making procedures: A political regime must have established procedures for making decisions, including laws and regulations, and the use of force or coercion.
PoliticalRegime和government都是用来描述国家政治制度和权力机构的术语，两者的区别和联系如下：

区别：

PoliticalRegime更强调国家政治制度的类型和性质，它包括了国家的政治体系、政党制度、选举制度、法律制度、宪政原则等。政治制度是政治文化、政治结构和政治行为的总和，是一个具有历史背景、意识形态、国际关系、法律体系等多个方面的复杂体系。
Government则更侧重于政府的机构和职能，它包括了政治领导层、政府机构、行政部门、司法部门、军队和警察等。政府是政治权力的具体代表和执行者，负责制定和执行国家政策、法律和规章制度，维护社会秩序和国家安全。
联系：

PoliticalRegime和government都是国家政治的重要组成部分。政治制度构成了政府的法律基础和政治基础，政府则是政治制度的具体执行者。
PoliticalRegime和government的性质和特征相互影响。不同的政治制度会影响政府的组织结构、职能和权力范围，不同的政府机构也会对政治制度产生影响。因此，了解政治制度和政府之间的关系，有助于更好地理解和分析国家政治。
    """
    def __init__(self, legitimacy, power_authority, control_of_territory, decision_making_procedures):
        self.legitimacy = legitimacy
        self.power_authority = power_authority
        self.control_of_territory = control_of_territory
        self.decision_making_procedures = decision_making_procedures
    
    def describe_legitimacy(self):
        return f"A political regime must be seen as legitimate by the population and other actors, such as international organizations or other states."
    
    def describe_power_authority(self):
        return f"A political regime must have the power and authority to make decisions and enforce laws and policies."
    
    def describe_control_of_territory(self):
        return f"A political regime must control a specific territory, either through direct or indirect means."
    
    def describe_decision_making_procedures(self):
        return f"A political regime must have established procedures for making decisions, including laws and regulations, and the use of force or coercion."
