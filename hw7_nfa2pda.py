from hw3_nfalang import buildNFA
from hw7_representation import PDAToXML
from nfa import NFA
from pda import PDA
import sys
import xml.etree.ElementTree as ET
import copy

def NFAToPDA(nfa:NFA):
    start = copy.deepcopy(nfa.start)
    accept = copy.deepcopy(nfa.accept)
    states = copy.deepcopy(nfa.states)
    alpha = copy.deepcopy(nfa.alpha)
    stack = []
    transitions = get_PDA_transitions(copy.deepcopy(nfa.delta))
    return PDA(states,alpha, stack, transitions, start, accept)

def get_PDA_transitions(nfa_transitions:dict):
    pda_transitions = copy.deepcopy(nfa_transitions)
    for key, val in nfa_transitions.items():
        for inp, states in val.items():
            pda_transitions[key][inp] = get_transitions_helper(states)
    return pda_transitions

def get_transitions_helper(states:list):
    res_list = []
    for s in states:
        res_list.append((s, '', ''))
    return res_list



if __name__ == "__main__":
    line = sys.stdin.readlines()[0]
    xml = ET.parse(line)
    xmlData = xml.getroot()
    myNFA = buildNFA(xmlData)
    myPDA = NFAToPDA(myNFA)
    result = PDAToXML(myPDA)
    ET.dump(result)
    