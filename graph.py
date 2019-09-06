from graphviz import Digraph

u1 = Digraph('example', filename='example.gv', strict=True)
u1.attr(size='126,6')
u1.node_attr.update(color='lightblue2', style='filled')

u1.node('1', label='padre')
u1.node('2', label='hijo')
u1.edge('1', '2')
u1.node('3', label='hijo')
u1.edge('1', '3')

u1.render()