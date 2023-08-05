class Line():
    def __init__(self, path, timestamp):
        self.path = path
        self.timestamp = timestamp
        self.occurence = 1

    def stringify(self):
        return self.path + "\t" + self.timestamp + "\t" + str(self.occurence)
     
    def __repr__(self):
        return f"Line(Path: {self.path}, Timestamp: {self.timestamp}, Occurence: {self.occurence})"