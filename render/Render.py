# -*- coding: utf-8 -*-
from anytree.dotexport import DotExporter
from anytree import RenderTree
from anytree import DoubleStyle
from subprocess import call

class tree_render(object):
    def exporToDotFile(self, syntax_tree, output_filename):
        DotExporter(syntax_tree, graph="graph", nodenamefunc=self.__nodenamefunc,
        nodeattrfunc=lambda node: "shape=box", edgeattrfunc=self.__edgeattrfunc,
        edgetypefunc=self.__edgetypefunc).to_dotfile(output_filename + ".dot")
    

    def compileDotFile(self, out_name):
        dot_name = out_name + ".dot"
        img_name = out_name + ".png"
        call(["dot", dot_name, "-T", "png", "-o", img_name])

    def renderTXT(self, syntax_tree):
        print(RenderTree(syntax_tree, style=DoubleStyle))
    

    def exportToTxtFile(self, syntax_tree, output_filename):
            filename = output_filename + ".txt"
            with open(filename, "w") as f:
                print(RenderTree(syntax_tree, style=DoubleStyle), filename, file=f)
    

    def __nodenamefunc(self, node):
        try:
            return '%s\n%s:%s\n%s\n%s' % (node.number, node.name, node.depth, node.tokentype, node.lexeme)
        except AttributeError:
            return '%s\n%s:%s' % (node.number, node.name, node.depth)
    
    
    def __edgeattrfunc(self, node, child):
        return 'label="%s:%s"' % (node.name, child.name)
    
    
    def __edgetypefunc(self, node, child):
        return '--'