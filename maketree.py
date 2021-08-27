#!/usr/bin/python3
import sys
import re

class orderedTreeNode:
    def __init__(self, parent=None, data=None):
        self.data=data
        self.parent=parent
        self.children=[]
    
    def setChildren(self,count):
        for i in range(0, count):
            child = orderedTreeNode(parent=self)
            self.children.append(child)
        return self.children

    def addChild(self, value):
        child = orderedTreeNode(parent=self,data=value)
        self.children.append(child)

    def setData(self,value):
        self.data=value

    # A very, very primitive representation of a tree
    def __repr__(self):
        result = ""
        result += str(self.data) + " -> "
        for child in self.children:
            result += str(child.data) + ", "
        return result
    # def __repr__(self):
    #     return str(self.data)

def add_children(node_stack,n,count):
    current = node_stack.pop()
    for i in range(0,n):
        count+=1
        current.addChild(count)

    # we want the first child to be on top of the stack, so push them on the stack in reverse order
    for i in range(0,n):
        node_stack.append(current.children[n-i-1])
    return count

def latex_rec(node):
    result = ""
    for child in node.children:
        result += "child{node{}"
        # result += "\nchild{node{}"
        result += latex_rec(child)
        result += "}"
    return result
    # for child in root.children:

def latex(root):
    result = "\\begin{tikzpicture}[every node/.style={circle,draw=black}]"
    result += "\\"
    result += "node{}"
    result += latex_rec(root)
    result += ";"
    result += "\end{tikzpicture}"
    return result

def preorder(node):
    if node is None:
        return
    print(node)
    for child in node.children:
        preorder(child)

def mktree(degree_sequence):
    root = orderedTreeNode()
    count = 0
    node_stack = [root]
    for degree in degree_sequence:
        count = add_children(node_stack,degree,count)
    return root

if __name__ == '__main__':
    
    # input = sys.argv[1].split(",")
    otree_regex = re.compile(r"\\otree{(\s*\d+(?:, *\d+ *)*)}")
    inputfile = open(sys.argv[1],"r")
    outlines = []
    for line in inputfile:
        matches = otree_regex.finditer(line)

        # Note: This will theoretically process stuff that's in comments
        # but the % will still be there, and it outputs all on one line
        # so although it's some wasted work with the find and replaces, it doesn't affect the output
        for match in matches:
            # group 1 is the stuff inside the brackets
            degree_sequence_string = match.group(1)
            degree_sequence = [int(a) for a in degree_sequence_string.replace(" ","").split(",")]
            (start,end) = match.span()
            root = mktree(degree_sequence)

            tikz_tree=latex(root)

            # print(line)
            # print(degree_sequence)
            # print(tikz_tree)
            line = line[:start] + tikz_tree + line[end:]
        print(line,end="")
