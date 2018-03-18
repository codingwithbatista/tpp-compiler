class stack(object):


    def __init__(self):
        self.data = []
    

    def isEmpty(self):
        return len(self.data) == 0 and True or False
    

    def getSize(self):
        return len(self.data)
    

    def push(self, element):
        self.data.append(element)
    

    def pop(self):
        if self.isEmpty() == False:
            self.data.pop(-1)