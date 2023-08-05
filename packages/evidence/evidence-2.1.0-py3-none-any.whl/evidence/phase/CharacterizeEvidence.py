import os

from evidence.model.CEAction import CEAction

class CharacterizeEvidence():
    def __init__(self, occurence) -> None:
        self._actions = []
        self._occurence = occurence

    def _initSet(self, indicator, list):
        set_ = self._getSetForIndicator(indicator)
        for l in list:
            line = l.split("\t")
            if(indicator == "noise"):
                set_.add(line[0] + "\t" + line[1] + "\n")
            if(int(line[2]) >= self._occurence):                       # Only if evidence occures min 2 times
                set_.add(line[0] + "\t" + line[1] + "\n")
        
    def _getSetForIndicator(self, indicator):
        result = None
        for action in self._actions:
            if(indicator == action.name):
                result = action.set
        return result

    def _getCESetForIndicator(self, indicator):
        result = None
        for action in self._actions:
            if(indicator == action.name):
                result = action.ceSet
        return result
    
    def _writeToFile(self, indicator, path):
        w = []
        file = open(path, "w", encoding="utf-8")

        for line in self._getCESetForIndicator(indicator):
            w.append(line)
             
        for line in self._sortAlphabetically(w):
            file.write(line)

        print("        --> Write File: " + path)
            
    def _sortAlphabetically(self, w):
        return sorted(w)
    
    def _calculate(self, indicator):
        me = set()
        print("    --> Calculate Characteristic Evidence for: " + indicator)
        for action in self._actions:
            if(action.name != indicator):
                print("        --> Action for Evidence Sum: " + action.name)
                me = me | action.set

        for action in self._actions:
            if(action.name == indicator):
                action.ceSet = action.set - me

    def process(self, pathME, pathCE):

        # Go through all me files to get all actions
        for path, dirs, files in os.walk(pathME):
            for file in files:
                # Extract the action name from the file
                actionName = file.split(".")[0]
                self._actions.append(CEAction(actionName))
                p = os.path.join(pathME, actionName + ".me")
                me = open(p, "r", encoding="utf-8")
                lines = me.readlines()
                self._initSet(actionName, lines)

        # Write *.ce   
        for action in self._actions:
            if(action.name != "noise"):    
                self._calculate(action.name)
                p = os.path.join(pathCE, action.name + ".ce")
                self._writeToFile(action.name, p)