from cfg import CFG
import sys
import xml.etree.ElementTree as ET
from pda import PDA
from hw7_representation import PDAToXML

"""
transfer the given xml file to CFG class
@param line: name of the xml file
@type line: String
@return: the transformed CFG
@rtype: CFG class
"""
def XMLToCFG(line):
    xml = ET.parse(line)
    xmlData = xml.getroot()
    rules = {}
    for production in xmlData.iter('production'):
        left = production.find('left').text
        right = production.find('right').text
        if left not in rules.keys():
            rules[left] = []
        if right == None:
            right = ''
        rules[left].append(right)
    variables = list(rules.keys())
    start = variables[0]
    alpha = extractAlpha(xmlData, variables)
    return CFG(variables, alpha, rules, start)

def CFGToPDA(cfg):
    states = ['q0', 'q1', 'q2']
    alpha = ['']
    stack_alpha = ['$']
    transitions = {'q0' : {'' : [('q1', '', cfg.start()+'$')]},
                   'q1' : {'' : [('q2', '$', '')]},
                   'q2' : {}}
    start = "q0"
    accept = ['q2']
    for variable in cfg.rules():
        stack_alpha += [variable]
        for rule in cfg.rules()[variable]:
            transitions['q1'][''] += [('q1', variable, rule)]
            stack_alpha += [rule]
            for char in rule:
                if char.islower():
                    alpha += [char]
                    transitions['q1'][char] = [('q1', char, '')]
    return PDA(states, alpha, stack_alpha, transitions, start, accept)

"""
extract alphabet of the given xml data
@param xmlData: the xml data that represent a CFG
@type xmlData: XML tree
@param variables: variables of the CFG to be built
@type variables: [Listof String]
@return: all alphabets of the CFG
@rtype: [Listof Char]
"""
def extractAlpha(xmlData, variables):
    alpha = []
    for production in xmlData.iter('production'):
        right = production.find('right').text
        if right == None:
            alpha += ['']
        else:
            for char in right:
                if char not in variables:
                    alpha += [char]
    alpha = list(set(alpha))
    return alpha

if __name__ == '__main__':
    line = sys.stdin.readlines()[0]
    myCFG = XMLToCFG(line)
    myPDA = CFGToPDA(myCFG)
    automaton = PDAToXML(myPDA)
    ET.dump(automaton)
