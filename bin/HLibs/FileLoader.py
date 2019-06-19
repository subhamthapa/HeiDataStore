
class FileLoader:
    def __init__(self):
        self.file = None
        self.data = None

    def load(self, address):

        self.file = open(address, "r+")
        self.data = self.file.readlines()
        self.file.close()





#FileLoader().load("..\\..\\datastore\\demo")