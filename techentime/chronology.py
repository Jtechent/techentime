#### IMPORT SECTION ####################################### BEGINS

from collections import namedtuple
from collections.abc import Iterable, Collection
from types import FunctionType
from techentime.techentime import Techentime, timestamp_to_techentime
from math import inf

#### IMPORT SECTION ####################################### ENDS

#### CLASSY SECTION ####################################### BEGINS

class Nill (namedtuple('VOID', ['key',])):
    '''Nill is like a tree but is None equiv'''
    def __new__(cls):
        '''creates the nill object which is empty'''
        obj = super(Nill, cls).__new__(cls, None)
        return obj
    
    def __init__ (self):
        '''initialize nill tree; all data members are none'''
        self.parent = None
        self.left   = None
        self.right  = None
        self.color  = True
        self.data   = "The void is vast. The void blinks."

    def compare (self, other, op):
        '''comparison operations fail because Nill is None equiv
           maybe I should just compare the other to none instead
        '''
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
        '''repr is like repr for rb-tree, no children displayed'''
        return ("NILL: CONTAINS INFINITE DARKNESS")

 
# create and initialize nill; nill is self referential
# I should try changing the none assignments in init to self
# if that fails I can always produce nill by closure
NILL = Nill()
NILL.parent = NILL
NILL.left   = NILL
NILL.right  = NILL



class Node (namedtuple('Node', ['key',])):
    '''node used in rb-tree'''
    def __new__(cls, key, **kwargs):
        '''creates nambed tuple decending node object with key'''
        obj = super(Node, cls).__new__(cls, key)
        return obj
    
    def __init__ (self, key, parent=None, left=None, right=None):
        '''initialize the node with proper relations'''
        self.parent = parent if parent else NILL
        self.left   = left if left else NILL
        self.right  = right if right else NILL
        self.color  = True
        self.data   = [] # data is always null on init rn

    def compare (self, other, op):
        '''compare self to other
           if other has key, compare self to other.key
           otherwise compare self to other
        '''
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
        '''search for key in tree rooted at self
           might be wise to impliment __getitem__ in nill
           nill.__getitem__ could always return none
        '''
        if self.key == key:
            return self
        elif self.key > key and self.left is not NILL:
            return self.left[key]
        elif self.key < key and self.right is not NILL:
            return self.right[key]
        else:
            return None

    def __iter__(self):
        '''returns in order iterator'''
        def iterer ():
            current = self
            while current:
                yield current
                current = successor(current)
        return iterer()

    def __reversed__(self):
        '''returns in reverse order iterator''' 
        def iterer ():
            current = self
            while current:
                yield current
                current = predecessor(current)
        return iterer
        

class RB_Tree ():
    '''implimentation of red black tree'''
    def __init__(self, root: Node or Nill):
        '''tree requires a root node; of type Node or Nill'''
        if isinstance(root, Node) or isinstance(root, Nill):
            self.root = root
            self.root.color = False
            self.keytype    = object
        else:
            raise TypeError(f"Tree root must be Node not {type(root)}")

    def __repr__(self):
        '''combines repr of root with the repr of rb trees  generated at left and right'''
        if self.root is NILL:
            return repr(self.root)
        return f"{self.root.key} color={self.root.color}: {str(self.root.data)}\nLEFT OF {self.root.key}: {str(display_tree(self.root.left))}\nRIGHT of {self.root.key}: {str(display_tree(self.root.right))}"

    def insert (self, node: Node) -> Node:
        '''insert using ordered binary tree insert
           balance with red black tree balancing
           set the root to the new root after balance
           return the new root
        '''
        self.root = balanced_insert(self.root, node, rb_balance)
        return self.root
        

    def __iter__(self):
        '''returns in order iterable
           iterable returned traverses the entire tree
           maybe I should alter this so that it calls the nodes iter
        '''
        def tree_iter ():
            least_left = least(self.root.left) # smallest value; why not call least on root?
            current = least_left if least_left is not NILL else self.root # have to do this because I did not call least on root
            while (current): # node data should be containers, so i have to interate over those
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
            # if key is not a slice, we are looking for a direct match
            node = self.root[key]
            return node.data if node else []
        else:
            node = self.get_first(key.start) # assume get first gets the least-greater then key.start
            if (not node) or node.key > key.stop:
                return [] # if there are not any nodes in the period defined by slice then we have the answer
        values = []
        start = key.start
        stop  = key.stop # what if slice is made via [n:]? or [:n]? I assume slices like tree[1:23]
        step  = abs(key.step) if key.step else 1
        traverse = iter if step > 0 else reversed

        for i, value in enumerate(traverse(node)): # traversal is done in the node level
            if i>=stop.n: # here we assume that stop is a techentime object; also, i is not a number expected to have meaningful compare to techentime.n
                break
            if i%step == 0:
                if isinstance(value.data, Iterable):
                    values.extend(value.data) # list data added to the list of values top level
                else:
                    if value.data is not None:
                        values.append(value.data) # add data if not iterable? should change to add data if not container correct?
        return values

 
    def get_first (self, key):
        '''returns least node >= key'''
        # check if in tree
        node = self.root[key]
        if node:
            return node
        parent, spot = get_place(self.root, Node(key))
        if spot == "left":
            return parent
        elif spot == "right":
            return successor(parent)
        else:
            raise Exception ("no spot found for {key}") # are there conditions where I expect to end up here?
    
    def key_to_label(self, key):
        '''default key check function which must be over ridden in the chronology'''
        if isinstance(key, self.keytype):
            return key
        return None

    def keys (self):
        '''returns an interator that fetches all keys'''
        def tree_iter ():
            least_left = least(self.root.left)
            current = least_left if least_left is not NILL else self.root
            while (current):
                yield current.key
                current = successor(current)
        return tree_iter()

        
    def __setitem__ (self, key, value):
        '''if keytype is proper
           set ends with rb tree with node where node.key == key, where data in node.data
        '''
        # change this to a keycheck function
        label = self.key_to_label(key)
        if not label:
            raise TypeError(f"Keys must be of value {self.keytype} not {type(key)}")
        if not self[label]:
            node = Node(label)
            node.data = [value]
            self.insert(node)
        else:
            data = self[label]
            data.append(value)
        return None

    def __delitem__ (self, key):
        ''''''
        if not self[key]:
            return None
        else:
            node = self.root[key] 
            success = successor(self.root[key]) # why not successor(node)?
            newnode = Node(success.key) 
            # don't I have to change the parent attributes of node.left and node.right?
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
        # this creates a tree for use in repr, idk
        self.root = root
        

class Chronology (RB_Tree):
    def __init__ (self, unit: int):
        '''creates a tree where labels must be Techentime
           want to change this so that we check for 2-tuple
        '''
        if not isinstance(unit, int) :
            raise TypeError("Chrononology unit must be of type int")
        # add epoch root
        epoch = timestamp_to_techentime('1970-01-01')
        root = Node(epoch << unit) if unit >= 0 else Node(epoch >> unit)
        super().__init__(root)

    def key_to_label (self, key):
        '''tests if the key is a 2-collection'''
        if isinstance(key, Collection) and len(key) == 2:
            return Techentime(key[0],key[1])
        return None

 

#### CLASSY SECTION ####################################### ENDS
    
#### FUNCTION SECTION #################################### BEGINS

def label_process (label: (object, object)) -> Node:
    pass

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

