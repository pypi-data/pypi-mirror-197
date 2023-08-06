class TenseAir:
    """
"緊張空氣" 是一种氛围或情境，通常与紧张、不安、压抑的情绪有关。以下是描述緊張空氣的特征：

沉默和不自然的气氛
焦虑和紧张的情绪
大家的情绪都不太放松，甚至可能感到紧绷
可能有不愉快的气味或声音，增加了緊張的感觉    
    """
    def __init__(self, silence=True, anxiety=True, emotional_tension=True, unpleasant_stimuli=True):
        self.silence = silence
        self.anxiety = anxiety
        self.emotional_tension = emotional_tension
        self.unpleasant_stimuli = unpleasant_stimuli
        
    def describe(self):
        if self.silence and self.anxiety and self.emotional_tension and self.unpleasant_stimuli:
            print("There is a tense atmosphere with a feeling of anxiety, emotional tension, and unpleasant stimuli.")
        elif self.silence and self.anxiety and self.emotional_tension:
            print("There is a tense atmosphere with a feeling of anxiety and emotional tension.")
        elif self.silence and self.anxiety:
            print("There is a tense atmosphere with a feeling of anxiety.")
        else:
            print("The air is not tense.")
