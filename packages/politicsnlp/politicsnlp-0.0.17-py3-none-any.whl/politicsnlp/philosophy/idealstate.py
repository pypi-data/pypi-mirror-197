from politicsnlp.ideology.ideology import *

class IdealState(Ideology):
    def __init__(self):
        self.leaders = [] # 智者
        self.guardians = [] # 守卫者
        self.producers = [] # 生产者

    def add_leader(self, person):
        if person.wisdom >= 5 and person.courage >= 5 and person.justice >= 5 and person.temperance >= 5:
            self.leaders.append(person)
        else:
            print("This person does not meet the requirements to be a leader in the ideal state.")

    def add_guardian(self, person):
        if person.courage >= 5:
            self.guardians.append(person)
        else:
            print("This person does not meet the requirements to be a guardian in the ideal state.")

    def add_producer(self, person):
        self.producers.append(person)

    def get_leader_names(self):
        return [leader.name for leader in self.leaders]

    def get_guardian_names(self):
        return [guardian.name for guardian in self.guardians]

    def get_producer_names(self):
        return [producer.name for producer in self.producers]

    def get_public_interest(self):
        return "The public interest is the most important consideration in the ideal state."








