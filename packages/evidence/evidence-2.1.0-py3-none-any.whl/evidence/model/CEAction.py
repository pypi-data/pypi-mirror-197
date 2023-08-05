class CEAction():
    def __init__(self, name) -> None:
        self.name = name
        self.set = set()
        self.ceSet = set()

    def __repr__(self):
        return f"CEAction(Name: {self.name})"