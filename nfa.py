import copy
"""
Data definition of NFA is given in the readme file
"""
class NFA:
    def __init__(self, states, alpha, delta, start, accept):
        self.states = states
        self.alpha = alpha
        self.delta = delta
        self.start = start
        self.accept = accept

    """
    run the desired input with this NFA
    """
    def run(self, input):
        currentState = [self.start]
        for char in input:
            temp = []
            for state in currentState:
                skipStates = self.epsilonReachableState(state, [state])
                temp += self.reachableState([state], char)
                temp += self.reachableState(skipStates, char)
            currentState = list(set(temp))

        final = [] + currentState
        for state in currentState:
            final += self.epsilonReachableState(state, [state])
        result = 'reject'
        for acceptState in self.accept:
            if acceptState in final:
                result = "accept"
                break
        return result

    """
    return all reachable states of the given states with given char, not
    counting epislon transition
    """
    def reachableState(self, states, char):
        result = []
        for state in states:
            if char in self.delta[state].keys():
                result += self.delta[state][char]
            else:
                continue
        return result

    """
    return all reachable states of the given state with only epsilon transition
    """
    def epsilonReachableState(self, state, final):
        result = []
        if '' in self.delta[state].keys():
            for s in self.delta[state][''][:]:
                if s in final:
                    continue
                final += [s]
                result += [s]
                result += self.epsilonReachableState(s, final)
        else:
            result += [state]
        return list(set(result))
