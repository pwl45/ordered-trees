#!/usr/bin/python3
import sys
# READ THIS STRING FOR USAGE
usage_string='''\
*************************** dycktotex.py ***************************
********************* provides LaTeX for Dycks *********************
***** reads Dyck words from stdin; prints LaTeX code to stdout *****

usage: ./dycktotex.py [options]

options:
\t-o: print tex for ordered trees
\t-c: print tex for ordered trees with colors and labels.
\t    Default if no options are provided
\t-b: print tex for binary trees
\t-e: print tex for extended binary trees
\t-p: print tex for dyck paths

The output of this program can be saved as a tex file and compiled, or piped into pdflatex, which will automatically write a pdf to texput.pdf.

The classes orderedTreeNode and binTreeNode are atrociously written.
The program will break if given bad input.
This program is not good. But it is useful.'''

# Initialize the G-String
gstring="\\node[style={fill=lightyellow}]{G};"
# Initialize the P-String
pstring="\\node[style={fill=lightpurple}]{P};"
# Initialize the L-String
lstring="\\node[style={fill=pink}]{L};"
# Initialize the O-String
ostring="\\node[style={fill=lightblue}]{O};"

class binTreeNode:
    def __init__(self, parent=None, data=None):
        self.data=data
        self.parent=parent
        self.left=None
        self.right=None
    def addChild(self, value):
        child = binTreeNode(parent=self,data=value)
        if self.left is None:
            self.left=child
            return child
        elif self.right is None:
            self.right=child
            return child
        else:
            print("Error: Third child")
            input()
            return -1

    def __repr__(self):
        result = ''
        result+=str(self.data)
        result += '->('

        if self.left is not None:
            result+=str(self.left.data)
            result+=' '

        if self.right is not None:
            result+=str(self.right.data)

        result  += ')'

        return result

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

    def addChild(self, value=None):
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
    if node.data == None:
        result = "[.{} "
    else:
        result = "[." + str(node.data) + " "
    for child in node.children:
        result += qtree(child)
    result += "] "
    return result

def leaf(extended):
    if extended:
        return "[.\\node[style={rectangle,minimum height=.6cm,minimum width=1cm}]{0}; ]"
    else:
        return "\\edge[draw=none]; \\node[blank]{};" # just don't draw the leaves
# little bit messy, but works
def binary_qtree(binary_node,extended=False):
    # print(extended)
    if binary_node.data == -1:
        return leaf(extended)
    # result = "[." + str(binary_node.data) + " "
    if extended:
        result = "[.{1} "
    else:
        result = "[.{} "
    if binary_node.left is not None:
        result += binary_qtree(binary_node.left,extended)
    else:
        result += leaf(extended)


    if binary_node.right is not None:
        result += binary_qtree(binary_node.right,extended)
    else:
        result += leaf(extended)
    result += "] "

    return result

def latex_binary_qtree(node,extended=False):
    result='''
\\begin{tikzpicture}[every tree node/.style={draw,circle},sibling distance=6, level distance=20]
\\tikzset{every tree node/.style={minimum width=1.5em,draw,circle},
         blank/.style={draw=none},
         edge from parent/.style=
         {draw,edge from parent path={(\\tikzparentnode) -- (\\tikzchildnode)}},
         level distance=1.5cm}
    \\Tree '''
    result+=binary_qtree(node,extended)
    result+='\n\\end{tikzpicture}'
    return result

def latex_qtree(node):
    result='''
\\begin{tikzpicture}[every tree node/.style={draw,circle},sibling distance=10pt, level distance=40pt]
\\tikzset{minimum width=1.5em,edge from parent/.style={draw, edge from parent path=
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

def preorder_degree_sequence(node):
    result=""
    if node is None:
        return result
    # print(node)
    result+=str(len(node.children))
    for child in node.children:
        result+=preorder_degree_sequence(child)
    return result

def bin_preorder(node):
    if node is None:
        return
    print(node)
    bin_preorder(node.left)
    bin_preorder(node.right)
def mktree_dyck(dyck_word):
    root = orderedTreeNode(parent=None)
    curr = root
    count=1
    for c in dyck_word:
        if int(c) == 1:
            curr = curr.addChild()
            count+=1
            # print(count)
        else:
            curr = curr.parent

        # print(c)

    # preorder(root)
    # print(root)
    return root

def mkbintree_dyck(dyck_word):
    if int(dyck_word[0]) != 1:
        print("something has gone wrong")
        return None
    root = binTreeNode(parent=None,data=0)
    curr = root
    count=1
    for c in dyck_word[1:]:
        if int(c) == 1:
            child = curr.addChild(count)
            curr = child
            count+=1
        else:
            curr.addChild(-1)
            while(curr.right is not None):
                curr = curr.parent

    return root

#hate this
def label_gplo(g,p,l,o):
    if g is not None:
        g.data = gstring

    if p is not None:
        p.data = pstring

    if l is not None:
        l.data = lstring

    if o is not None:
        o.data = ostring

# hate this
def label_otree_nodes(root):
    curr = root
    o = None
    while(len(curr.children) > 0):
        if len(curr.children) > 1:
            o = curr.children[1]
        curr = curr.children[0]

    l = None
    p = None
    g = None
    if o == None:
        o=curr
        if o != root:
            p = o.parent
            if p != root:
                g = p.parent
    else:
        p=o.parent
        l=p.children[0]
        if p != root:
            g = p.parent
    label_gplo(g,p,l,o)

def dyck_word_to_luka_word(dyck_word):
    root = mktree_dyck(dyck_word)
    # result = latex_qtree(root)
    result=""
    result += latex_qtree(root) + "\n\n"
    result += "$" + preorder_degree_sequence(root) + "$"
    return result

def dyck_word_to_extended_binary_qtree(dyck_word):
    root = mkbintree_dyck(dyck_word)
    result = latex_binary_qtree(root,extended=True)
    return result

def dyck_word_to_binary_qtree(dyck_word):
    root = mkbintree_dyck(dyck_word)
    result = latex_binary_qtree(root)
    return result

def dyck_word_to_path_and_tree(dyck_word):
    root = mktree_dyck(dyck_word)
    result = latex_qtree(root)
    result += dyck_word_to_tikz_path(dyck_word)

    return result

def dyck_word_to_tikz_qtree(dyck_word):
    root = mktree_dyck(dyck_word)
    result = latex_qtree(root)
    return result

def dyck_word_to_colored_tikz_qtree(dyck_word):
    root = mktree_dyck(dyck_word)
    label_otree_nodes(root)
    result = latex_qtree(root)
    return result

def dyck_word_to_tikz_path(dyck_word):
    result = '\\LukaTableDriver[1][1]{' + str(len(dyck_word)) + '}'
    maxheight = 0
    currheight = 0
    sequence="{"
    for c in dyck_word:
        if int(c) == 1:
            currheight+=1
            maxheight = max(currheight,maxheight)
            sequence+='2,'
        else:
            currheight-=1
            sequence+='0,'
    sequence+="}"

    result += "{" + str(maxheight) + "}" + sequence

    return result

def parse_file(file,tex_function):
    body=""
    for line in file:
        if line[0] == "#"  or line[0] == "%":
            continue
        if line[0] != "[" and line[0] != "1":
            body += "\n\n"
            body += line
            body += "\n\n\\bigskip\n\n"
            continue
        line=line.replace("[","").replace("]","")
        if ',' in line:
            dyck_word = [int(a) for a in line.split(",")]
        else:
            dyck_word = line[:-1]
        body +=str(dyck_word) + "\n\n"

        tex_output=tex_function(dyck_word)
        body +=  tex_output
        body += "\n\n\\bigskip\n\n"

    return body


if __name__ == '__main__':

    header = \
            '''\\documentclass{article}
\\usepackage{tikz}
\\usepackage{indentfirst} % the fact that this needs to be its own """"package"""" is beyond stupid. 
\\definecolor{lightpurple}{RGB}{203, 195, 227}
\\definecolor{lightblue}{RGB}{173, 216, 230}
\\definecolor{lightyellow}{RGB}{255, 255, 158}
'''

    body = '''\\begin{document}
'''
    footer = "\\end{document}"

    if len(sys.argv) < 2:
        mode = '-c'
    else:
        mode = sys.argv[1]

    header += "\\usepackage{tikz-qtree}\n"
    header += '''\\usetikzlibrary{math}\n\\usepackage{twoopt}

\\newcommand{\\LukaTable}[2][2]{\\LukaTableDriver[1][1]{8}{#1}{#2}}
\\newcommandtwoopt{\\LukaTableDriver}[5][1][1]{
  \\begin{tikzpicture}[x=#1cm, y=#2cm, step=1]
      \\tikzmath{
        \\xValue = 0;
        \\yValue = 0;
        {
          \\draw[black,thin] (0,0) grid (#3,#4);
          \\filldraw[fill=none, draw=none] (#3, #4) ellipse (0.05cm and 0.05cm);  % for consistent bounding box
        };
        for \\yDelta in {#5}{
          %\\labelUp = int(\\yDelta+1);
          %\\labelDn = int(\\yDelta);
          {
            \\filldraw[fill=black, draw=black] (\\xValue, \\yValue) ellipse (0.05cm and 0.05cm);
            %\\node[] at (\\xValue + 0.5, -1) {\\labelDn};
            %\\node[] at (\\xValue + 0.5, #3) {\\labelUp};
          };
          \\xNext = \\xValue + 1;
          \\yNext = \\yValue + \\yDelta - 1; % Here is the -1
          {
            \\draw[black,very thick] (\\xValue, \\yValue) -- (\\xNext, \\yNext);
          };
          \\xValue = \\xNext;
          \\yValue = \\yNext;
        };
      }
      {
        \\filldraw[fill=black, draw=black] (\\xValue, \\yValue) circle (0.05cm);
      };
  \\end{tikzpicture}
}
'''

    if mode == '-h':
        print(usage_string)
        exit(1)
    if mode == '-o':
        body+= '\\section*{Dyck Words $\iff$ Ordered Trees}\n\n'
        body+=parse_file(sys.stdin,dyck_word_to_tikz_qtree)
    if mode == '-c':
        body+= '\\section*{Dyck Words $\iff$ Ordered Trees}\n\n'
        body+=parse_file(sys.stdin,dyck_word_to_colored_tikz_qtree)
    elif mode == '-p':
        body+= '\\section*{Dyck Words $\iff$ Dyck Paths}\n'
        body+=parse_file(sys.stdin,dyck_word_to_tikz_path)
    elif mode == '-b':
        body+= '\\section*{Dyck Words $\iff$ Binary Trees}\n'
        body+=parse_file(sys.stdin,dyck_word_to_binary_qtree)
    elif mode == '-e':
        body+= '\\section*{Dyck Words $\iff$ Binary Trees}\n'
        body+=parse_file(sys.stdin,dyck_word_to_extended_binary_qtree)
    elif mode == '-a':
        body+= '\\section*{Dyck Words$\iff$Ordered Trees$\iff$Dyck Paths}\n'
        body+=parse_file(sys.stdin,dyck_word_to_path_and_tree)
    elif mode == '-l':
        body+= '\\section*{Dyck Words$\iff$Lukasiewicz Words}\n'
        body+=parse_file(sys.stdin,dyck_word_to_luka_word)

    print(header)
    print(body)
    print(footer)

