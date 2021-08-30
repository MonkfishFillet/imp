from enum import Enum

class Party:
    class AvgType(Enum):
        HP = 0
        AC = 1
        PASSIVE_PERCEPTION = 2
        PASSIVE_INVESITATION = 3
        PASSIVE_INSIGHT = 4

    def __init__(self, party: list):
        self._party = party

    def get_avg(self, avg_type: AvgType):
        if avg_type.value == 0:
            return self.__calculate_avg(avg_type)

    def __calculate_avg(self, avg_type: AvgType):
        avg = []
        if avg_type.value == 0:
            for char in self._party:
                avg.append(char.hp)
        if avg_type.value == 1:
            for char in self._party:
                avg.append(char.ac)
        if avg_type.value == 2:
            for char in self._party:
                avg.append(char.passive_perception)
        if avg_type.value == 3:
            for char in self._party:
                avg.append(char.passive_investigation)
        
        return sum(avg)/len(avg)
