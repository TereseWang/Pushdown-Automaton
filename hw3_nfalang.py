import sys
import xml.etree.ElementTree as ET
import itertools
from nfa import NFA

"""
Build the nfa class based on the given xml data
@param xmlData: given the xml data to build a nfa
@type xmlData: xml
"""
def buildNFA(xmlData):
    stateList = getStates(xmlData)
    states = stateList[0]
    start = stateList[1]
    accept = stateList[2]
    alphaDelta = getTransitions(xmlData, states)
    alpha = alphaDelta[0]
    delta = alphaDelta[1]
    states = list(states.values())
    return NFA(states, alpha, delta, start, accept)

"""
Return all states, start state, and accept states of the given xmlData
@param xmlData: xml data to extract from
@type xmlData: xml
"""
def getStates(xmlData):
    states = {}
    start = ""
    accept = []
    for state in xmlData.iter("state"):
        states[state.attrib["id"]] = state.attrib["name"]
        if state.find("initial") != None:
            start = state.attrib["name"]
        if state.find("final") != None:
            accept.append(state.attrib["name"])
    return(states, start, accept)

"""
Return all transitions of the given xmlData in the format of
{startstate: {alpha : [nextstate1, nextstate2..., ...}}
@param xmlData: xml data to extract information
@type xmlData: xml
@param states: list of all states in the given xmlData
@type states: {id : name}
"""
def getTransitions(xmlData, states):
    alpha = []
    delta = {}
    for state in states:
        stateName = states[state]
        delta[stateName] = {}
    for transition in xmlData.iter("transition"):
        fromState = transition.find("from").text
        toState = transition.find("to").text
        read = transition.find("read").text
        if read == None:
            read = ''
        alpha.append(read)
        alpha = list(set(alpha))
        fromState = states[fromState]
        try:
            delta[fromState][read]
        except:
            delta[fromState][read] = []
        delta[fromState][read].append(states[toState])
    return(alpha, delta)
