import copy
import xml.etree.ElementTree as ET

"""
Data representation of CFG, more detaill will be find in readme
"""
class CFG:
    def __init__(self, variables, alpha, rules, start):
        self.__variables = variables #list of variables
        self.__alpha = alpha #alphabet of this CFG
        self.__rules = rules #dictionary with key to be the left and value to be right
        self.__start = start #start variable

    """ getter function get variables of this CFG"""
    def variables(self):
        return copy.deepcopy(self.__variables)

    """ getter function get alpha of this CFG"""
    def alpha(self):
        return copy.deepcopy(self.__alpha)

    """ getter function get rules of this CFG"""
    def rules(self):
        return copy.deepcopy(self.__rules)

    """ getter function get start varible of this CFG"""
    def start(self):
        return copy.deepcopy(self.__start)

    """Change this CFG to xml format"""
    def CFGToXML(self):
        structure = ET.Element('structure')
        type = ET.SubElement(structure, 'type')
        type.text = 'grammar'
        for variable in self.variables():
            for rule in self.rules()[variable]:
                production = ET.SubElement(structure, 'production')
                left = ET.SubElement(production, 'left')
                left.text = variable
                right = ET.SubElement(production, 'right')
                if rule != '':
                    right.text = rule
        return structure

    """
    extract all variables (none-terminals) of the given string
    @param string: the rules to extract variables from
    @type string: String
    @return: all variables/non-terminals from the given string
    @rtype: [Listof String]
    """
    def extractVariables(self, string):
        result = []
        for char in string:
            if char in self.variables():
                result += [char]
        return result
