class CivilServant:
    """
    公务员是指受雇于政府机构的工作人员，他们通常具有以下特征：

    忠诚于国家：公务员应该忠诚于国家和政府，服从法律和法规，为公众利益服务。
    公正和廉洁：公务员应该保持公正和廉洁，不接受贿赂或其他不当利益，不违反职业道德。
    专业能力：公务员应该具备相应的专业知识和技能，以便有效地履行职责和服务公众。
    社会责任：公务员应该意识到自己的工作对社会和公众有重要的影响，应该履行相应的社会责任。

    """
    def __init__(self, loyalty, impartiality, professionalism, social_responsibility):
        self.loyalty = loyalty
        self.impartiality = impartiality
        self.professionalism = professionalism
        self.social_responsibility = social_responsibility
    
    def describe_loyalty(self):
        return f"Civil servants should be loyal to the state and government, and serve the public interest."
    
    def describe_impartiality(self):
        return f"Civil servants should maintain impartiality and integrity, and avoid accepting bribes or other improper benefits."
    
    def describe_professionalism(self):
        return f"Civil servants should possess the necessary professional knowledge and skills to effectively perform their duties and serve the public."
    
    def describe_social_responsibility(self):
        return f"Civil servants should recognize the importance of their work to society and the public, and fulfill corresponding social responsibilities."
