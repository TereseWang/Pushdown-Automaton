import sys
import xml.etree.ElementTree as ET
from pda import PDA
import copy

def XMLToPDA(file):
    xml = ET.parse(file)
    xmlData = xml.getroot()
    automaton = xmlData.find('automaton')
    states = []
    alpha = []
    stack_alpha = []
    transitions = {}
    start = ""
    accept = []
    tempState = {}
    for state in automaton.iter('state'):
        states += state.attrib['name']
        if state.find('initial') != None:
            start = state.attrib['name']
        if state.find('final') != None:
            accept.append(state.attrib['name'])
        transitions[state.attrib['name']] = {}
        tempState[state.attrib['id']] = state.attrib['name']
    for transition in automaton.iter('transition'):
        fromstate = transition.find('from').text
        fromstate = tempState[fromstate]
        tostate = transition.find('to').text
        tostate = tempState[tostate]
        read = transition.find('read').text
        if read == None:
            read = ''
        if read not in alpha:
            alpha += [read]
        pop = transition.find('pop').text
        if pop == None:
            pop = ''
        push = transition.find('push').text
        if push == None:
            push = ''
        if read not in transitions[fromstate].keys():
            transitions[fromstate][read] = []
        stack = (tostate, pop, push)
        transitions[fromstate][read] += [stack]
        stack_alpha += [pop]
        stack_alpha += [push]
    stack_alpha = list(set(stack_alpha))
    return PDA(states, alpha, stack_alpha, transitions, start, accept)

"""
run the desired input with this NFA
"""
def run(pda, input, max):
    transitions = pda.get_transitions()
    steps = {}
    index = 0
    char = input[index]
    currentRoutes = [(pda.get_start(), [])]
    stepNum = 0
    steps = {}
    final = True
    while index <= len(input) - 1 and final:
        steps = allSteps(currentRoutes, transitions, char, stepNum, steps)
        stepNums = list(steps.keys())
        stepNum = stepNums[len(stepNums) - 1]
        currentRoutes = steps[stepNum]
        if currentRoutes[0][1] == []:
            if index < len(input) - 1:
                final = False
        if max != 0 and stepNum > max:
            final = False

        index +=1
        stepNum += 1
        if index <= len(input) - 1:
            char = input[index]

    return final

def allSteps(currentRoutes, transitions, char, step, acc):
    for route in currentRoutes:
        tempChar = nextStep(transitions, route[0], route[1], char, [])
        tempEmpty = nextStep(transitions, route[0], route[1], '', [])
        newCurrent = tempEmpty + tempChar

        if tempChar != []:
            if step not in acc.keys():
                acc[step] = []
            acc[step] += newCurrent
            break
        else:
            allSteps(newCurrent, transitions, char, step+1, acc)
    return acc

def nextStep(transitions, state, stack, char, acc):
    result = []
    if char in transitions[state].keys():
        for route in transitions[state][char]:
            nextState = route[0]
            nextStack = pushPop(stack, route[1], route[2])
            if nextStack == False:
                continue
            if (nextState, nextStack) in acc:
                continue
            result += [(nextState, nextStack)]
            acc += [(nextState, nextStack)]
    return result


def pushPop(stack, pop, push):
    stack = copy.deepcopy(stack)
    if pop == '' and push != '':
        stack += push
    elif pop != '' and push == '':
        if stack == []:
            return False
        if stack[len(stack) - 1] == pop:
            del stack[len(stack) - 1]
        else:
            return False
    elif pop != '' and push != '':
        if stack == []:
            return False
        if stack[len(stack) - 1] == pop:
            del stack[len(stack) - 1]
            stack += push
        else:
            return False
    return stack

if __name__ == '__main__':
    line = sys.stdin.readlines()[0]
    line = line.split(' ')
    myPDA = XMLToPDA(line[0])
    if len(line) == 3:
        max = int(line[2])
    else:
        max = 0
    result = run(myPDA, line[1], max)
    if result:
        print('accept')
    else:
        print('reject')
