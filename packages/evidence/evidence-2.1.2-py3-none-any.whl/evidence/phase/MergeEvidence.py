import os

from string import Template

from evidence.model.Line import Line
from evidence.model.MEAction import MEAction

class MergeEvidence():
    def __init__(self) -> None:
        self._actions = []
        self.nameTemplate = Template("$action.$number.pe")

    def _add(self, indicator, line):
        self._getListForIndicator(indicator).append(line)
        
    def _getListForIndicator(self, indicator):
        result = None
        for action in self._actions:
            if(indicator == action.name):
                result = action.merged
        return result
    
    def _init(self, indicator, lines):
        for line in lines:
            parts = line.split("\t")
            self._add(indicator, Line(path=parts[0], timestamp=parts[1].replace("\n", "")))
    
    def _compare(self, indicator, lines):
            temp = []
            # for each line in the file to be compared
            for line in lines:
                # Split into parts
                parts = line.split("\t")
                # Flag indicating if a line is already present
                isMatched = False
                # For each entry in a
                for line in self._getListForIndicator(indicator):
                    # Check if the line is already present
                    if(line.path == parts[0] and line.timestamp == parts[1].replace("\n", "")):
                        # if yes, increment occurense
                        line.occurence = line.occurence + 1
                        # set flag that hit occured
                        isMatched = True
                        break
                # If there was no hit, line need to be added 
                if(isMatched == False):
                    temp.append(Line(path=parts[0], timestamp=parts[1].replace("\n", "")))
            # Add the additional lines
            for n in temp:
                self._add(indicator, n)
            # Clears the additional lines list
            temp.clear()  

    def _writeToFile(self, indicator, path):
        w = []
        file = open(path, "w", encoding="utf-8")
        for line in self._getListForIndicator(indicator):
            w.append(line.stringify() + "\n")
  
        for line in self._sortAlphabetically(w):
            file.write(line)

        print("    --> Write File: " + path)
        
    def _sortAlphabetically(self, w):
        return sorted(w)

    def process(self, pathPE, pathME): 
        # Go through all pe files to get all actions
        for path, dirs, files in os.walk(pathPE):
            for file in files:
                # Extract the action name from the file
                actionName = file.split(".")[0]
                # If there is no action yet
                if(len(self._actions) == 0):
                    a = MEAction(actionName)
                    a.increment()
                    self._actions.append(a)
                else:
                    # If there are actions...
                    actionListed = False
                    for action in self._actions:
                        # Check if action is already created
                        if(action.name == actionName):
                            action.increment()
                            actionListed = True
                            break
                    # If action is not created yet...
                    if(not actionListed):
                        a = MEAction(actionName)
                        a.increment()
                        self._actions.append(a)

        # Read *.1.pe
        for action in self._actions:
            if(action.name != "noise"):
                name = self.nameTemplate.substitute(action=action.name, number="1")
                p = os.path.join(pathPE, name)
                pe = open(p, "r", encoding="utf-8")
                lines = pe.readlines()
                self._init(action.name, lines)

        for action in self._actions:
            if(action.occurence == 1):
                # Check if action only have one occurence.
                # If so, comparison is not needed
                p_ = os.path.join(pathME, action.name + ".me")
                self._writeToFile(action.name, p_)
            else:
                # Read *.*.pe, compare to *.1.pe and write *.me
                if(action.name != "noise"):
                    for i in range(2, (action.occurence+1)):
                        name = self.nameTemplate.substitute(action=action.name, number=i)
                        p = os.path.join(pathPE, name)
                        pe = open(p, "r", encoding="utf-8")
                        lines = pe.readlines()
                        self._compare(action.name, lines)
                    p_ = os.path.join(pathME, action.name + ".me")
                    self._writeToFile(action.name,  p_)
                
        # Read noise.pe and write noise.me
        p = os.path.join(pathPE, "noise.1.pe")
        pe = open(p, "r", encoding="utf-8")
        lines = pe.readlines()
        self._init("noise", lines)
        p = os.path.join(pathME, "noise.me")
        self._writeToFile("noise", p)