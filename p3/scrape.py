# project: p3
# submitter: jchalem
# partner: none
# hours: ????

#scrape.py will have the following
#    GraphSearcher (a class)
#    MatrixSearcher (a class)
#    FileSearcher (a class)
#    WebSearcher (a class)
#    reveal_secrets (a function)

import os, pandas as pd

class Parent:
    def twice(self):
        self.message()
        self.message()
        
    def message(self):
        print("parent says hi")
        
class Child(Parent):
    def message(self):
        print("child says hi")
        
c = Child()

c.twice()

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        self.order.clear()
        # 1. clear out visited set
        self.visited.clear()
        # 2. start recursive search by calling dfs_visit
        self.dfs_visit(node)

    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return
        # 2. mark node as visited by adding it to the set
        self.visited.add(node)
        # 3. add this node to the end of self.order
        self.order.append(node)
        # 4. get list of node's children with this: self.go(node)
        children = self.go(node)
        # 5. in a loop, call dfs_visit on each of the children
        for child in children:
            self.dfs_visit(child)
    
    def bfs_search(self, node):
        self.order.clear()
        self.visited.clear()
        #print(node)
        self.bfs_visit(node)
        for n in self.order: 
            #print(str(n) + " Loop")
            self.bfs_visit(n)
        
    def bfs_visit(self, node):     
        if node in self.visited:
            return
        #print(list(self.visited))
        children = self.go(node)
        #print(type(children))
        #print(children)
        self.visited.add(node)
        self.visited.update(set(children))
        #self.visited.add(node)
        self.order += [node] + children
        #print("List")
        #print(self.order)
            
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def go(self, node):
        children = []
        # TODO: use `self.df` to determine what children the node has and append them
        for node, has_edge in self.df.loc[node].items():
            if has_edge == 1:
                children.append(node)
        return children
    
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__() # call constructor method of parent class
    
    def go(self, node):
        with open(os.path.join("file_nodes", node)) as f:
            files = f.readlines()[1].replace("\n","").split(",")
        return files
    
    def message(self):
        self.mes = ""
        for i in self.order:
            f = open(os.path.join("file_nodes", i))
            self.mes += f.readlines()[0].replace("\n","")
            f.close()
        return self.mes