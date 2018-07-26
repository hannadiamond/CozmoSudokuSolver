
class Square(object):
     def __init__(self):
        self.row = 0
        self.col = 0
        self.chars='.'
        self.domain=["1","2","3","4","5","6","7","8","9"]
        self.neighbors = []
     def addNeighbor(self, square):
         self.neighbors.append(square)
     def getNeighbors(self):
        return self.neighbors
     def compareNeighbors(self):
        changed = False
        for i, neighbor in enumerate(self.neighbors):
                for i, num in enumerate(self.domain):
                    if neighbor.chars in self.domain:
                        self.domain.remove(neighbor.chars)
                        changed=True
                        if len(self.domain)==1:
                            self.chars = self.domain[0]
        return changed
     def setDomain(self):
        self.domain=[self.chars]
     def printNeighbors(self):
        string=""
        for i, nb in enumerate(self.neighbors):
            string+=nb.chars
        return string
     def getChar(self):
        return self.chars
