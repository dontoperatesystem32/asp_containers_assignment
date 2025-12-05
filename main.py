class Container:
    def __init__(self):
        self.amount = 0.0
        self.neighbors = set()

    def getAmount(self):
        return self.amount

    def connectTo(self, c):
        if c is self or c in self.neighbors:
            return
        self.neighbors.add(c)
        c.neighbors.add(self)
        self._redistribute()

    def disconnectFrom(self, c):
        if c not in self.neighbors:
            return
        self.neighbors.remove(c)
        c.neighbors.remove(self)
        #after disconnect both components must redistribute
        self._redistribute()
        c._redistribute()

    def addWater(self, amt):
        #add to this container then redistribute
        self.amount += amt
        self._redistribute()

    def _redistribute(self):
        #perform bfs to find all connected containers
        visited = set()
        stack = [self]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(node.neighbors)

        #compute equal share
        total = sum(x.amount for x in visited)
        share = total / len(visited)

        #assign equal water
        for x in visited:
            x.amount = share
