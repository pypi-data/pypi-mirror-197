from politicsnlp.ideology.ideology import *

class Confucianism(Ideology):
    def __init__(self, name, worldview, normative, political, influential,ruler, people):
        super().__init__(name, worldview, normative, political, influential)
        self.ruler = ruler
        self.people = people

    def ren(self):
        if self.ruler and self.people:
            print("仁者爱人，爱民，治国平天下。")
        else:
            print("己所不欲，勿施于人。")

    def yi(self):
        if self.ruler and self.people:
            print("以礼治国，以礼行事。")
        else:
            print("不做违背天理的事情。")

    def li(self):
        if self.ruler and self.people:
            print("君子务本，本立而道生。")
        else:
            print("积善之家，必有余庆。")