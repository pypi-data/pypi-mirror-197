class ConservativeParty:
    """
The Conservative Party in the United Kingdom is a center-right political party that emphasizes economic liberalism, social conservatism, and nationalism. Here are some common characteristics of the Conservative Party:

Economic liberalism: The Conservative Party generally supports free-market capitalism, deregulation, and low taxes, and opposes state intervention in the economy.
Social conservatism: The Conservative Party tends to promote traditional values and social norms, such as the nuclear family, individual responsibility, and law and order.
Nationalism: The Conservative Party emphasizes national sovereignty and cultural identity, often taking a more skeptical view of European integration and immigration.
Pragmatism: The Conservative Party is often associated with a pragmatic and cautious approach to policy-making, favoring incremental reforms over radical change.
Leadership: The Conservative Party places a strong emphasis on leadership and often looks to a charismatic leader to rally support and shape the party's direction.
    
    """
    def __init__(self, economic_liberalism=True, social_conservatism=True, nationalism=True, pragmatism=True, leadership=True):
        self.economic_liberalism = economic_liberalism
        self.social_conservatism = social_conservatism
        self.nationalism = nationalism
        self.pragmatism = pragmatism
        self.leadership = leadership

    def describe(self):
        description = "This political party exhibits the following characteristics:\n"
        if self.economic_liberalism:
            description += "- Economic liberalism\n"
        if self.social_conservatism:
            description += "- Social conservatism\n"
        if self.nationalism:
            description += "- Nationalism\n"
        if self.pragmatism:
            description += "- Pragmatism\n"
        if self.leadership:
            description += "- Leadership\n"
        return description
