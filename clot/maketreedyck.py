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
        return child

    def setData(self,value):
        self.data=value

    # A very, very primitive representation of a tree
    def __repr__(self):
        result = ""
        result += str(self.data) + " -> "
        for child in self.children:
            result += str(child.data) + ", "
        result += "  parent is " + str(self.parent)
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

def qtree(node):
    # if len(
    children=len(node.children)
    result = "[." + str(children) + " "
    for child in node.children:
        result += qtree(child)
    result += "] "
    return result

def latex_qtree(node):
    result='''
\\begin{tikzpicture}[every tree node/.style={draw,circle},sibling distance=10pt, level distance=40pt]
\\tikzset{edge from parent/.style={draw, edge from parent path=
    {(\\tikzparentnode) -- (\\tikzchildnode)}}}
    \\Tree '''
    result+=qtree(node)
    result+='\n\\end{tikzpicture}'
    return result
    
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

def mktree_dyck(dword):
    root = orderedTreeNode(parent=None,data=0)
    curr = root
    count=1
    for c in dword:
        if int(c) == 1:
            curr = curr.addChild(count)
            count+=1
            # print(count)
        else:
            curr = curr.parent

        # print(c)

    # preorder(root)
    # print(root)
    return root

def mktree(degree_sequence):
    root = orderedTreeNode()
    count = 0
    node_stack = [root]
    for degree in degree_sequence:
        count = add_children(node_stack,degree,count)
    return root

def parse_file(file):
    outlines = []
    body=""
    for line in file:
        if line[0] == "#"  or line[0] == "%":
            continue
        if line[0] != "[" and line[0] != "1":
            body += "\n\n"
            body += line
            body += "\n\n\\bigskip\n\n"
            # print("werid") 
            continue
        line=line.replace("[","").replace("]","")
        degree_sequence = [int(a) for a in line.split(",")]
        body +=str(degree_sequence) + "\n\n"
        root = mktree_dyck(degree_sequence)
        tikz_tree=latex_qtree(root)
        # tikz_tree=latex(root)
        body +=   tikz_tree
        body += "\n\n"
        # body += "\n\n------------------------------------------\n\n\\bigskip\n\n"
        # body += "\n\n\\bigskip\n\n\\bigskip"
        # line = line[:start] + tikz_tree + line[end:]
        # matches = otree_regex.finditer(line)

        # Note: This will theoretically process stuff that's in comments
        # but the % will still be there, and it outputs all on one line
        # so although it's some wasted work with the find and replaces, it doesn't affect the output
        # for match in matches:
            # group 1 is the stuff inside the brackets
            # (start,end) = match.span()


    print(body)
        # print(tikz_tree,end="")


def balanced(ms):
    sum = 0
    for i in range(0, len(ms) - 1):
        sum += ms[i]
        if sum < i+1:
            # print(ms, sum,i)
            return False
    return ms[len(ms)-1] == 0

def valid_tree(degree_sequence):
    if not sum(degree_sequence) == len(degree_sequence)-1:
        print("Invalid tree: sum not equal to length-1")
        print("SUM:",sum(degree_sequence), "LEN:",len(degree_sequence))
        return False
    elif not balanced(degree_sequence):
        print("Invalid tree: not balanced")
        return False
    else:
        return True



if __name__ == '__main__':

    # input = sys.argv[1].split(",")
    # otree_regex = re.compile(r"\\otree{(\s*\d+(?:, *\d+ *)*)}")
    # if len(sys.argv) < 2:
    #     print("Error: not enough args")
    header = \
            '''\\documentclass{article}
\\usepackage{tikz}
\\usepackage{tikz-qtree}
\\begin{document}
\\section{Trees}'''
    footer = "\end{document}"
    mode = sys.argv[1]
    if mode == '-f':
        inputfile = open(sys.argv[2],"r")
        print(header)
        parse_file(inputfile)
        print(footer)
    else:
        body = ""
        for arg in sys.argv[1:]:
            degree_sequence = [int(a) for a in arg.split(",")]
            # if not valid_tree(degree_sequence):
            #     exit(1)
            root = mktree_dyck(degree_sequence)
            # tikz_tree=latex(root)
            tikz_tree=latex_qtree(root)
            body += str(degree_sequence) + "\n\n"
            body += tikz_tree + "\n\n"
        print(header)
        print(body)
        print(footer)
