class MEAction():
    def __init__(self, name) -> None:
        self.name = name
        self.occurence = 0
        self.merged = []

    def increment(self):
        self.occurence += 1

    def __repr__(self):
        return f"MEAction(Name: {self.name}, Occurence: {str(self.occurence)})"