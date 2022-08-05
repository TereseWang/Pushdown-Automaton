import sys
from pda import PDA
import xml.etree.ElementTree as ET

def PDAToXML(pda):
    structure = ET.Element('structure')
    type = ET.SubElement(structure, 'type')
    type.text = 'pda'
    automaton = ET.SubElement(structure, 'automaton')
    for state in pda.get_states():
        s = ET.SubElement(automaton, 'state', id=state, name=state)
        if pda.get_start() == state:
            ET.SubElement(s, 'initial')
        if state in pda.get_accept():
            ET.SubElement(s, 'final')
    transitions = pda.get_transitions()
    for state in transitions:
        for alpha in transitions[state]:
            trans = transitions[state][alpha]
            for i in trans:
                t = ET.SubElement(automaton, 'transition')
                fro = ET.SubElement(t, 'from')
                fro.text = state
                to = ET.SubElement(t, 'to')
                to.text = i[0]
                read = ET.SubElement(t, 'read')
                if alpha != '':
                    read.text = alpha
                pop = ET.SubElement(t, 'pop')
                if i[1] != '':
                    pop.text = i[1]
                push = ET.SubElement(t, 'push')
                if i[2] != '':
                    push.text = i[2]
    return structure

if __name__ == '__main__':
    states = ['q0', 'q1', 'q2']
    alpha = ['(', ')', '[', ']']
    stack_alpha = ['$', '(', '[']
    transitions = {'q0' : {'':[('q1', '', '$')]},
                   'q1' : {'(':[('q1', '', '(')],
                           '[':[('q1', '', '[')],
                           ')':[('q1', '(', '')],
                           ']':[('q1', '[', '')]},
                   'q2' : {}}
    start = 'q0'
    accept = ['q2']
    myPDA = PDA(states, alpha, stack_alpha, transitions, start, accept)
    result = PDAToXML(myPDA)
    ET.dump(result)
