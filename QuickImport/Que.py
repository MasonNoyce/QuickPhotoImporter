class Que():
    def __init__(self):
    self.items=[]
    
    def empty(self):
        return self.items == [], True
        
    def enqueue(self,item):
        self.items.insert(0,item)
        
    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
        
