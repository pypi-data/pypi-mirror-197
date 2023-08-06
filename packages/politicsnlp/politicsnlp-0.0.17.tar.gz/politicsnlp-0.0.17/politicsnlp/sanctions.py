class Sanctions:
    """
    Sanctions, also known as economic or trade restrictions, are measures taken by countries or international organizations to restrict economic or political activity in another country or with a specific group or individual. The main features of sanctions include:

    Restriction of trade: Sanctions often involve restrictions on trade, such as prohibitions on the import or export of certain goods, services, or technologies.
    Financial restrictions: Sanctions can also include financial restrictions, such as freezing assets or banning financial transactions with designated individuals or entities.
    Diplomatic measures: Sanctions can include diplomatic measures, such as travel bans, the expulsion of diplomats, and the suspension of diplomatic relations.
    Political pressure: Sanctions are often used to exert political pressure on a country or group to change its policies or behavior.

    """
    def __init__(self, trade_restrictions, financial_restrictions, diplomatic_measures, political_pressure):
        self.trade_restrictions = trade_restrictions
        self.financial_restrictions = financial_restrictions
        self.diplomatic_measures = diplomatic_measures
        self.political_pressure = political_pressure
    
    def describe_trade_restrictions(self):
        return f"Sanctions often involve restrictions on trade, such as prohibitions on the import or export of certain goods, services, or technologies."
    
    def describe_financial_restrictions(self):
        return f"Sanctions can also include financial restrictions, such as freezing assets or banning financial transactions with designated individuals or entities."
    
    def describe_diplomatic_measures(self):
        return f"Sanctions can include diplomatic measures, such as travel bans, the expulsion of diplomats, and the suspension of diplomatic relations."
    
    def describe_political_pressure(self):
        return f"Sanctions are often used to exert political pressure on a country or group to change its policies or behavior."
