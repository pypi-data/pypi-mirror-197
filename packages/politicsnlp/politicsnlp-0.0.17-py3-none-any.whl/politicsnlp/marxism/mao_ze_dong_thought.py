from politicsnlp.marxism.marxism import *
class MaoZedongThought(Marxism):
    """
    ## Characteristics of Mao Zedong Thought:

    Mass line: Mao emphasized the importance of understanding and serving the needs of the masses. The Mass line is a method of leadership that requires leaders to listen to the opinions and demands of the people they lead, and to integrate these opinions and demands into their decision-making process.
    Continuous revolution: Mao believed that revolution should be a continuous process. He argued that society is in a constant state of change, and that it is the duty of the Communist Party to lead the people in a never-ending struggle against the forces of capitalism and imperialism.
    Class struggle: Mao believed that class struggle was the driving force behind historical development. He saw the world as divided into two primary classes: the proletariat and the bourgeoisie. According to Mao, the struggle between these two classes was the engine of history.
    Self-reliance: Mao believed that China could only achieve true independence by relying on its own resources and capabilities. He advocated for the development of China's industry and agriculture, and emphasized the importance of self-sufficiency in all areas of life.
    People's war: Mao believed that the people were the main force in the struggle against imperialism and colonialism. He developed the concept of "people's war," which emphasizes the use of guerrilla tactics and the mobilization of the masses in a protracted struggle against the enemy.

    """
    def __init__(self,economic_system, social_classes,class_struggle,surplus_value,dialectical_materialism,historical_materialism):
        super().__init__(economic_system, social_classes,class_struggle,surplus_value,dialectical_materialism,historical_materialism)
        self.mass_line = True
        self.continuous_revolution = True
        self.self_reliance = True
        self.peoples_war = True
    
    def explain(self):
        print("Mao Zedong Thought is characterized by the following features:")
        print("- Mass line: understanding and serving the needs of the masses")
        print("- Continuous revolution: revolution as a never-ending process")
        print("- Class struggle: the engine of historical development")
        print("- Self-reliance: relying on China's own resources and capabilities")
        print("- People's war: the use of guerrilla tactics and mobilization of the masses")
