#### IMPORT SECTION ####################################### BEGINS

from collections import namedtuple
from collections.abc import Iterable
from types import FunctionType
from techentime.techentime import Techentime
from math import inf

#### IMPORT SECTION ####################################### ENDS

#### CLASSY SECTION ####################################### BEGINS

class Nill (namedtuple('VOID', ['key',])):
    def __new__(cls):
        obj = super(Nill, cls).__new__(cls, None)
        return obj
    
    def __init__ (self):
        self.parent = None
        self.left   = None
        self.right  = None
        self.color  = True
        self.data   = "The void is vast. The void blinks."

    def compare (self, other, op):
        raise ValueError("Nothing compares to the void.")
    def __lt__(self, other):
        return self.compare(other, lambda x, y: x < y) 

    def __le__(self, other):
        return self.compare(other, lambda x, y: x <= y) 
        
    def __eq__(self, other):
        return self.compare(other, lambda x, y: x == y) 

    def __ne__(self, other):
        return self.compare(other, lambda x, y: x != y) 

    def __gt__(self, other):
        return self.compare(other, lambda x, y: x > y) 

    def __ge__(self, other):
        return self.compare(other, lambda x, y: x >= y) 

    def __repr__(self):
        return ("NILL: CONTAINS INFINITE DARKNESS")

 
 
NILL = Nill()
NILL.parent = NILL
NILL.left   = NILL
NILL.right  = NILL





class Node (namedtuple('Node', ['key',])):
    def __new__(cls, key, **kwargs):
        obj = super(Node, cls).__new__(cls, key)
        return obj
    
    def __init__ (self, key, parent=None, left=None, right=None):
        self.parent = parent if parent else NILL
        self.left   = left if left else NILL
        self.right  = right if right else NILL
        self.color  = True
        self.data   = []

    def compare (self, other, op):
        if 'key' in dir(other):
            other = other.key
        return op(self.key, other) 
    def __lt__(self, other):
        return self.compare(other, lambda x, y: x < y) 

    def __le__(self, other):
        return self.compare(other, lambda x, y: x <= y) 
        
    def __eq__(self, other):
        return self.compare(other, lambda x, y: x == y) 

    def __ne__(self, other):
        return self.compare(other, lambda x, y: x != y) 

    def __gt__(self, other):
        return self.compare(other, lambda x, y: x > y) 

    def __ge__(self, other):
        return self.compare(other, lambda x, y: x >= y) 

    def __getitem__(self, key):
        if self.key == key:
            return self
        elif self.key > key and self.left is not NILL:
            return self.left[key]
        elif self.key < key and self.right is not NILL:
            return self.right[key]
        else:
            return None

    def __iter__(self):
        def iterer ():
            current = self
            while current:
                yield current
                current = successor(current)
        return iterer()
    def __reversed__(self):
        def iterer ():
            current = self
            while current:
                yield current
                current = predecessor(current)
        return iterer
        

class RB_Tree ():
    def __init__(self, root: Node or Nill):
        if isinstance(root, Node) or isinstance(root, Nill):
            self.root = root
            self.root.color = False
            self.keytype    = object
        else:
            raise TypeError(f"Tree root must be Node not {type(root)}")
    def __repr__(self):
        if self.root is NILL:
            return repr(self.root)
        return f"{self.root.key} color={self.root.color}: {str(self.root.data)}\nLEFT OF {self.root.key}: {str(display_tree(self.root.left))}\nRIGHT of {self.root.key}: {str(display_tree(self.root.right))}"

    def insert (self, node: Node) -> Node:
        '''returns root'''
        self.root = balanced_insert(self.root, node, rb_balance)
        return self.root
        

    def __iter__(self):
        def tree_iter ():
            least_left = least(self.root.left)
            current = least_left if least_left is not NILL else self.root
            while (current):
                if current.data == []:
                    current = successor(current)
                    continue
                if isinstance(current.data, Iterable):
                    yield from iter(current.data)
                else:
                    yield current.data
                current = successor(current)
        return tree_iter()

    def __getitem__ (self, key) -> []:
        if not isinstance(key, slice):
            node = self.root[key]
            return node.data if node else []
        else:
            node = self.get_first(key.start)
            if (not node) or node.key > key.stop:
                return []
        values = []
        start = key.start
        stop  = key.stop
        step  = abs(key.step) if key.step else 1
        traverse = iter if step > 0 else reversed

        for i, value in enumerate(traverse(node)):
            if i>=stop.n:
                break
            if i%step == 0:
                if isinstance(value.data, Iterable):
                    values.extend(value.data)
                else:
                    if value.data is not None:
                        values.append(value.data)
        return values

 
    def get_first (self, key):
        # check if in three
        node = self.root[key]
        if node:
            return node
        parent, spot = get_place(self.root, Node(key))
        if spot == "left":
            return parent
        elif spot == "right":
            return successor(parent)
        else:
            raise Exception ("no spot found for {key}")
        



    def keys (self):
        def tree_iter ():
            least_left = least(self.root.left)
            current = least_left if least_left is not NILL else self.root
            while (current):
                yield current.key
                current = successor(current)
        return tree_iter()

                   
                
        
    def __setitem__ (self, key, value):
        if not isinstance(key, self.keytype):
            raise TypeError(f"Keys must be of value {self.keytype} not {type(key)}")
        if not self[key]:
            node = Node(key)
            node.data = [value]
            self.insert(node)
        else:
            data = self[key]
            data.append(value)
        return None

    def __delitem__ (self, key):
        if not self[key]:
            return None
        else:
            node = self.root[key]
            success = successor(self.root[key])
            newnode = Node(success.key)
            newnode.parent = node.parent
            newnode.left   = node.left
            newnode.right  = node.right
            newnode.color  = node.color
            if node.parent is not NILL:
                if node.parent.left is node:
                    node.parent.left = newnode
                else:
                    node.parent.right = newnode
            else:
                self.root = newnode
            delete_one_child(success)
                
            
            
            
class display_tree(RB_Tree):
    def __init__(self, root):
        self.root = root
        

class Chronology (RB_Tree):
    def __init__ (self, root: Node):
        if not isinstance(root.key, Techentime):
            raise TypeError("Chronologies Require Techentime values not {type(root.key)} values for keys.")
        super().__init__(root)


 

#### CLASSY SECTION ####################################### ENDS
    
#### FUNCTION SECTION #################################### BEGINS

def get_sibling (node: Node) -> Node:
    parent = node.parent
    if parent is NILL:
        return NILL
    return parent.left if parent.right is node else parent.right

def get_uncle (node: Node) -> Node:
    return get_sibling(node.parent)

def get_root (node: Node) -> Node:
    return node if node.parent is NILL else get_root(node.parent)


def rotate_left (node: Node) -> None:
    newnode      = node.right
    assert(newnode is not NILL)
    parent       = node.parent

    node.right        = newnode.left
    node.right.parent = node

    newnode.left = node
    node.parent  = newnode

    if node.right is not NILL:
        node.right.parent = node

    newnode.parent = parent

    if parent is NILL:
        return None

    if parent.left is node:
        parent.left = newnode
    else:
        parent.right = newnode
    return None


def rotate_right (node: Node) -> None:
    newnode           = node.left
    assert(newnode is not NILL)
    parent            = node.parent

    node.left         = newnode.right
    node.left.parent  = node

    newnode.right     = node
    node.parent       = newnode

    if node.left is not NILL:
        node.left.parent = node

    newnode.parent = parent

    if parent is NILL:
        return None

    if parent.left is node:
        parent.left = newnode
    else:
        parent.right = newnode
    return None



def get_place (root: Node, node: Node) -> (Node, str):
    '''returns parent of node'''
    spot=['left', 'right'][int(node >= root)]
    if getattr(root, spot) is NILL:
        return root, spot
    return get_place(getattr(root, spot), node)

def balanced_insert (root: Node, node: Node, balance: FunctionType) -> Node:
    '''insert into root node then balance(root); then return root(root)'''
    parent, spot = get_place(root, node)
    if parent is not NILL:
        setattr(parent, spot, node)
    node.parent = parent
    balance(node)
    return get_root(root)
    

def rb_balance (node: Node) -> None:
    def case1 (node: Node) -> None:
        node.color = False
        return None

    def case2 (node: Node) -> None:
        return None

    def case3 (node: Node) -> None:
        node.parent.color        = False
        get_uncle(node).color    = False
        node.parent.parent.color = True
        rb_balance(node.parent.parent)
        return None

    def case4 (node: Node) -> None:

        # rotate node to parent pos; parent to outer child
        if node is node.parent.right and node.parent is node.parent.parent.left:
            rotate_left(node.parent)
            n = node.left
        elif node is node.parent.left and node.parent is node.parent.parent.right:
            rotate_right(node.parent)
            n = node.right

        else:
            n = node
        
        p = n.parent
        g = p.parent
        if n is n.parent.left:
            rotate_right(n.parent.parent)
        else:
            rotate_left(n.parent.parent)
        p.color = False
        g.color = True
        return None

    # 1
    if node is get_root(node):
        case1(node)
    # 2 
    elif not node.parent.color:
        case2(node)
    # 3 
    elif get_uncle(node) is not NILL and not get_uncle(node).color:
        case3(node)
    # 4 
    else:
        case4(node)

def relabel (node: Node, label) -> None:
    newnode        = Node(label)

    newnode.parent = parent
    if node is node.parent.left:
        node.parent.left  = newnode
    else:
        node.parent.right = newnode

    newnode.left      = node.left
    node.left.parent  = newnode
    newnode.right     = node.right
    node.right.parent = newnode
    return None

def cutout_node (node: Node, child: Node) -> None:
    child.parent = node.parent if child is not NILL else NILL
    if node is node.parent.left:
        node.parent.left = child
    else:
        node.parent.right = child
    return None

def delete_one_child (node: Node) -> None:

    def case1(node: Node) -> None:
        if node.parent is not NILL:
            case2(node)
        return None

    def case2(node: Node) -> None:
        s = get_sibling(node)
        if s.color:
            node.parent.color = True
            s.color = False
            if node is n.parent.left:
                rotate_left(node.parent)
            else:
                rotate_right(node.parent)
        case3(node)
        return None

    def case3(node: Node) -> None:
        s = get_sibling(node)
        if not node.parent.color and not s.color and not s.left.color and not s.right.color:
            s.color = True
            case1(node.parent)
        else:
            case4(node)
        return None

    def case4(node: Node) -> None:
        s = get_sibling(node)
        if node.parent.color and not s.color and not s.left.color and not s.right.color:
            s.color           = True
            node.parent.color = False
        else:
            case5(node)
        return None

    def case5 (node: Node) -> None:
        s = get_sibling(node)
        if not s.color:
            if n is n.parent.left and not s.right.color and s.left.color:
                s.color = True
                s.left.color = False
                rotate_right(s)
            elif n is n.parent.right and not s.left.color and s.right.color:
                s.color = True
                s.right.color = False
                rotate_left(s)
        case6(node)
        return None

    def case6(node):
        s = get_sibling(node)
        s.color = node.parent.color
        n.parent.color = False
        if n is n.parent.left:
            s.right.color = False
            rotate_left(node.parent)
        else:
            s.left.color = False
            rotate_right(node.parent)

    
    child = node.right if node.right else node.left
    cutout_node (node, child)
    if child is NILL:
        return None
    if not node.color:
        if child.color:
            child.color = False
        else:
            case1(child)
        
def greatest(node: Node) -> Node:
    if node is NILL:
        return NILL
    return node if node.right is NILL else greatest(node.right)

def least (node: Node) -> Node:
    if node is NILL:
        return NILL
    return node if node.left is NILL else least(node.left)

def next_right(node: Node) -> Node:
    if node.parent is NILL:
        return node
    return node if node is node.parent.right else next_right(node.parent)

def next_left(node: Node) -> Node:
    if node.parent is NILL:
        return node
    return node if node is node.parent.left else next_left(node.parent)



def predecessor (node: Node) -> Node or None:
    if node.parent is NILL:
        predecess = greatest(node.left)
    elif node is node.parent.left:
        greatest_left = greatest(node.left)
        potential_predecessor = greatest(node.left) if greatest_left is not NILL else predecessor(next_left(node.parent))
        predecess = None if potential_predecessor is node else potential_predecessor
    else:
        greatest_left = greatest(node.left)
        predecess = greatest_left if  greatest_left is not NILL else node.parent
    tbr = predecess if predecess is not NILL else None
    return tbr
            
def successor (node: Node) -> Node or None:
    if node.parent is NILL:
        success = least(node.right)
    elif node is node.parent.right:
        least_right = least(node.right)
        potential_successor = least(node.right) if least_right is not NILL else successor(next_right(node.parent))
        success = None if potential_successor is node else potential_successor
    else:
        least_right = least(node.right)
        success = least_right if  least_right is not NILL else node.parent
    return success if success is not NILL else None
        

def get_last (chron: Chronology, start=Techentime(-inf,0), stop=Techentime(inf,0), where=lambda x: True) -> []:
    node = chron.root[stop]
    if node is not NILL:
        parent, spot = get_place(chron.root, Node(stop))
        if spot == 'right':
            node = parent
        else:
            node = predecessor(parent)
        if not node:
            return []
    current = node
    while current:
        for value in current.data:
            if where(value):
                return value 
        pred = predecessor(current)
        current = pred if pred and pred.key > start else None
        if not current:
            return []
        
    

#### FUNCTION SECTION #################################### ENDS 

## TESTS

def test_a ():
    from random import random
    times = [int(random*10000000) for _ in range(100)]

