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
            
                   
            
A = Container()
B = Container()
C = Container()
D = Container()
E = Container()
A.addWater(10)
B.addWater(15)
C.addWater(20)
D.addWater(2)
E.addWater(12)
print(A.amount)
print(B.amount)
print(C.amount)
print(D.amount)
print(E.amount)
print('-------')


A.connectTo(B)
A.connectTo(C)
print(f'ABC amount per each: {A.amount}')
print(f'ABC amount per each: {B.amount}')
print(f'ABC amount per each: {C.amount}')

print('-------')

D.connectTo(E)
print(f'DE amount per each: {D.amount}')
print(f'DE amount per each: {E.amount}')


A.connectTo(D)
print(f'Obshi: {A.amount}')
print(f'Obshi: {D.amount}')