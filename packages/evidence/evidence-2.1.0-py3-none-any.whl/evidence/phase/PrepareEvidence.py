import os

class PrepareEvidence():
    def __init__(self):
        self.currentType = ""
        self.fileType = { "NEW_FILES": "New files", "DEL_FILES": "Deleted files", 
                          "RE_FILES": "Renamed files", "MOD_FILES": "Files with modified contents",
                          "PROP_FILES": "Files with changed properties"}
        self._idiff = []    # Initial list - Contains all the lines of the idiff file
        self._list = []     # processed list - Contains the lines after processing with the given logic
        self._unique = []   # unique list - Contains only unique lines
        self._sorted = []   # sorted list - Contains alphabetically sorted lines
    
    def _checkFileType(self, line):
        if(self.fileType["NEW_FILES"] in line):
                self.currentType = self.fileType["NEW_FILES"]
        elif(self.fileType["DEL_FILES"] in line):
                self.currentType = self.fileType["DEL_FILES"]
        elif(self.fileType["RE_FILES"] in line):
                self.currentType = self.fileType["RE_FILES"]
        elif(self.fileType["MOD_FILES"] in line):
                self.currentType = self.fileType["MOD_FILES"]
        elif(self.fileType["PROP_FILES"] in line):
                self.currentType = self.fileType["PROP_FILES"]

    def _reset(self):
        self._idiff.clear()
        self._list.clear()
        self._unique.clear()
        self._sorted.clear()

    def _sortAlphabetically(self):
        self._sorted = sorted(self._unique)

    def _makeUnique(self):
        self._unique = list(set(self._list))

    def _addLine(self, line):
        self._list.append(line)

    def _writeToFile(self, path):
        file = open(path, "w", encoding="utf-8")
        for line in self._sorted:
            file.write(line + "\n")
        print("    --> Write File: " + path)

    def _setIdiffData(self, idiff):
        self._idiff = idiff

    def _sanitize(self):
        for line in self._idiff:
            if(line == ""):
                self._idiff.remove("")
            elif(line == "\n"):
                self._idiff.remove("\n")

    def _process(self):
        for line in self._idiff:
            # Checks the current file type and set the current file type
            self._checkFileType(line)

            # Is it "New Files"...
            if(self.currentType == self.fileType["NEW_FILES"]):
                if(line != "" and line != "\n"):
                    newFile = line.split("\t")
                    if(len(newFile) == 3):
                        for ts in ["m", "a", "c", "cr"]:
                            self._addLine(newFile[1] + "\t" + ts)

            # Is it "Deleted Files"...
            elif(self.currentType == self.fileType["DEL_FILES"]):
                if(line != "" and line != "\n"):
                    delFile = line.split("\t")
                    if(len(delFile) == 3):
                            self._addLine(delFile[1] + "\t" + "d")

            # Is it "Renamed Files", "Files with modified contents" oder
            # "Files with changed properties"...
            elif(self.currentType == self.fileType["RE_FILES"] 
                or self.currentType == self.fileType["MOD_FILES"]
                or self.currentType == self.fileType["PROP_FILES"]):
                if(line != "" and line != "\n"):
                    fi = line.split("\t")
                    if("mtime" in line):
                        self._addLine(fi[0] + "\t" + "m")
                    elif("ctime" in line):
                        self._addLine(fi[0] + "\t" + "c")
                    elif("atime" in line):
                        self._addLine(fi[0] + "\t" + "a")
                    elif("crtime" in line):
                        self._addLine(fi[0] + "\t" + "cr")

    def process(self, pathGE, pathPE):
        for path, dirs, files in os.walk(pathGE):
            for file in files:
                self._reset()
                # File ending of new file
                newFileName = file.replace("idiff", "pe")
                # Full path
                fullPath = os.path.join(path, file)
                # Opens the specific .idiff file
                idiff = open(fullPath, "r", encoding="utf-8")
                # Reads all the lines from the idiff file
                lines = idiff.readlines()
                # Sets the readed lines
                self._setIdiffData(lines)
                # Removes space and newlines
                self._sanitize() 
                # Processes lines with the given logic
                self._process()
                # Remove duplicates
                self._makeUnique()
                # Sort lines alphabetically
                self._sortAlphabetically()
                # Write to new file
                p = os.path.join(pathPE, newFileName)
                self._writeToFile(p)  