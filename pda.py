import copy

class PDA:
    def __init__(self, states, alpha, stack_alpha, transitions, start, accept):
        self.__states = states
        self.__alpha = alpha
        self.__stack_alpha = stack_alpha
        self.__transitions = transitions
        self.__start = start
        self.__accept = accept

    def get_states(self):
        return copy.deepcopy(self.__states)

    def get_alpha(self):
        return copy.deepcopy(self.__alpha)

    def get_stack_alpha(self):
        return copy.deepcopy(self.__stack_alpha)

    def get_transitions(self):
        return copy.deepcopy(self.__transitions)

    def get_start(self):
        return self.__start

    def get_accept(self):
        return self.__accept
