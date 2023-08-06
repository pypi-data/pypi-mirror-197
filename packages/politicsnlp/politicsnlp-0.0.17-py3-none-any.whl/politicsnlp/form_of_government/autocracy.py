from politicsnlp.form_of_government.form_of_government import *

class Autocracy(FormOfGovernment):
    """
    Dictatorship和autocracy都是一种集中权力的政治制度，但它们有一些不同之处。Dictatorship强调一个人或一小群人掌握政治权力，而autocracy则强调权力的不受限制和无限制的性质。

    Autocracy是一种政治制度，其中权力集中在一人或一小群人手中，这些人对政治体系有完全的控制权，并且没有制衡或监督他们的机制。相比之下，Dictatorship通常更加强调权力的掌握和运用。
    
    这个类和前面的Dictatorship类很相似，但是我们把它命名为Autocracy，并且删除了elections和civil_liberties这两个特征，因为Autocracy并不强调这些方面。相反，我们增加了一个no_checks_on_power特征，用于表示权力是否受到任何制约或监督。
    """
    def __init__(self, ruler, group_size, no_checks_on_power, use_of_force,name, power_structure, legitimacy, accountability, decision_making):
        super().__init__(name, power_structure, legitimacy, accountability, decision_making)
        self.ruler = ruler
        self.group_size = group_size
        self.no_checks_on_power = no_checks_on_power
        self.use_of_force = use_of_force

    def is_autocracy(self):
        return True

    def has_one_person_rule(self):
        return self.group_size == 1

    def has_no_checks_on_power(self):
        return self.no_checks_on_power

    def uses_force(self):
        return self.use_of_force
