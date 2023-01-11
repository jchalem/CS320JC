# project: p2
# submitter: jchalem
# partner: none
# hours: 20

class Node():
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None
        self.left_height = 0
        self.right_height = 0
        
    def __len__(self):
        size = len(self.values)
        if self.left != None:
            size += self.left.__len__()
        if self.right != None:
            size += self.right.__len__()
        return size
    
    def lookup(self, key):
        if self.key == key:
            return self.values
        elif key < self.key and self.left != None:
            return self.left.lookup(key)
        elif key > self.key and self.right != None:
            return self.right.lookup(key)
        else:
            return []

class BST():
    def __init__(self):
        #self.right = right
        #self.left = left
        self.d = 0
        self.left_height = 0
        self.right_height = 0
        self.root = None
        

    def add(self, key, val):
        if self.root == None:
            self.root = Node(key)

        curr = self.root
        while True:
            if key < curr.key:
                # go left
                if curr.left == None:
                    curr.left = Node(key)
                curr = curr.left
            elif key > curr.key:
                if curr.right == None:
                    curr.right = Node(key)
                curr = curr.right
                # go right
            else:
                # found it!
                assert curr.key == key
                break

        curr.values.append(val)
        
    def __dump(self, node):
        if node == None:
            return
        self.__dump(node.left)            # 1
        print(node.key, ":", node.values)  # 2
        self.__dump(node.right)             # 3

    def dump(self):
        self.__dump(self.root)
        
    def __getitem__(self, index):
        return self.root.lookup(index)
    
    def depth(self, node):
        if node.right != None:
            self.right_height += 1
            self.depth(node.right)
        if node.left != None:
            self.depth(node.left)
            self.left_height += 1
        return max(self.right_height, self.left_height) + 1
    
    def number_nodes(self, node):
        if node.right != None:
            self.right_height += 1
            self.depth(node.right)
        if node.left != None:
            self.left_height += 1
            self.depth(node.left)
        return self.right_height + self.left_height + 1
    
            