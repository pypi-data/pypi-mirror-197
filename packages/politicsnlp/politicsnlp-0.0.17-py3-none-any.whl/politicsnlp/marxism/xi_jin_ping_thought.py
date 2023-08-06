from politicsnlp.marxism.marxism import *

class XiJinpingThought(Marxism):
    """
    Characteristics of Xi Jinping Thought:

    Socialist modernization: Xi Jinping has emphasized the need to modernize China's economy, society, and governance through a socialist framework. This includes prioritizing innovation, entrepreneurship, and high-quality development.
    The "Chinese Dream": Xi Jinping has promoted the idea of the "Chinese Dream," which includes the goal of national rejuvenation and the achievement of the "Two Centenary Goals" - namely, to build a moderately prosperous society by 2021 and to transform China into a modern socialist country by 2049.
    The Belt and Road Initiative: Xi Jinping has promoted the Belt and Road Initiative, a massive infrastructure project aimed at promoting economic development and connectivity across Asia, Africa, and Europe.
    Strengthening of the Communist Party of China (CPC): Xi Jinping has emphasized the importance of strengthening the CPC and has launched a high-profile anti-corruption campaign to root out corruption within the party.
    "New Era" of Chinese socialism: Xi Jinping has declared that China has entered a "new era" of Chinese socialism, which is characterized by a shift towards higher-quality economic development, greater emphasis on environmental protection, and the promotion of global governance.
    """
    def __init__(self,economic_system, social_classes,class_struggle,surplus_value,dialectical_materialism,historical_materialism):
        super().__init__(economic_system, social_classes,class_struggle,surplus_value,dialectical_materialism,historical_materialism)
        self.socialist_modernization = True
        self.chinese_dream = True
        self.belt_and_road_initiative = True
        self.cpc_strengthening = True
        self.new_era_of_chinese_socialism = True
    
