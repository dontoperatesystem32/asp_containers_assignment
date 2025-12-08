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
        try:
            if (amt < 0):
                raise ValueError("Negative amount cannnot be added")
                
            #add to this container then redistribute
            else:
                self.amount += amt
        except ValueError as ve:
            print(ve)
            exit()
            
            
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
            
def main():                   
    print("Creating 5 containers: A, B, C, D, E")
    A = Container()
    B = Container()
    C = Container()
    D = Container()
    E = Container()

    print(f"Adding 10 to A")
    A.addWater(10)
    print(f"Adding 15 to B")

    B.addWater(-15)

    print("Error is thrown")
        
        
    print(f"Adding 20 to C")
    C.addWater(20)
    print(f"Adding 2 to D")
    D.addWater(2)
    print(f"Adding 12 to E")
    E.addWater(12)

    print('-------')


    print(f"Water in A: {A.amount}")
    print(f"Water in B: {B.amount}")
    print(f"Water in C: {C.amount}")
    print(f"Water in D: {D.amount}")
    print(f"Water in E: {E.amount}")

    print('-------')

    print("Connecting A to B and A to C")
    A.connectTo(B)
    A.connectTo(C)
    print('-------')

    print(f'Water in A: {A.amount}')
    print(f"Water in B: {B.amount}")
    print(f"Water in C: {C.amount}")

    print('-------')

    print("Connecting D to E")
    print('-------')

    D.connectTo(E)
    print(f"Water in D: {D.amount}")
    print(f"Water in E: {E.amount}")

    print('-------')
    print("Connecting ABC to DE")
    print('-------')


    A.connectTo(D)
    print(f'Water in A: {A.amount}')
    print(f'Water in D: {D.amount}')


if __name__ == '__main__':
    main()