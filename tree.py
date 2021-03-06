#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 09:26:17 2019

@author: @MauricioAcosta
"""

import numpy as np
import pandas as pd
from pandas import DataFrame, read_csv
from graphviz import Digraph


df = pd.read_excel('./default_of_credit_card_clients.xls')
df = df.dropna(axis=0, how='any')
df = df.drop(0)
del df['Unnamed: 0']
df.truncate(before=2, after=10)

class Node: pass

axisArray = []
medianArray = []

def kdtree(pointList, depth=0):
    if not pointList:
        return

    auxpointList = np.array(pointList)
    salidaY = auxpointList[:, 23]
    # print('salidaY: ',salidaY)
    if all(elem == salidaY[0] for elem in salidaY):
        #print('encontre una hoja: ')
        node = Node()
        node.pointList = pointList
        return node
        # Select axis based on depth so that axis cycles through all valid values
    k = len(pointList[0]) - 1  # assumes all points have the same dimension
    # print('k: ',k)
    axis = depth % k
    # print('axis: ',axis)
    axisArray.append(axis)
    # Sort point list and choose median as pivot element
    pointList.sort(key=lambda x: x[axis])
    median = len(pointList) // 2  # choose median
    medianArray.append(median)
    # print(median)
    # Create node and construct subtrees
    tempDepth = depth
    node = Node()
    # node.condition = 'L' + str(tempDepth) + ' X' + str(axis) + '<=' + str(median)
    medianValueInAxis = pointList[median][axis]
    node.condition = 'L' + str(tempDepth) + ' X' + str(axis) + '<=' + str(medianValueInAxis)
    node.location = pointList[median]
    # node.leftChild = kdtree(pointList[0:median], depth + 1, 'Left L' + str(tempDepth) + ' X' + str(axis) + '<' + str(median))
    # node.rightChild = kdtree(pointList[median + 1:], depth + 1, 'Right L' + str(tempDepth) + ' X' + str(axis) + '>' + str(median))
    # newCondition = 
    node.leftChild = kdtree(pointList[0:median], depth + 1)
    node.rightChild = kdtree(pointList[median + 1:], depth + 1)
    return node

aux = df.values.tolist()

tree = kdtree(aux)

u1 = Digraph('arbol', filename='arbol.gv', strict=True)
# u1.attr(size='20000') # 17654 inch, 1765400 px, 100dpi
u1.attr(size='20000', dpi='100')
# u1.attr(size='200', dpi='100')
u1.node_attr.update(color='lightblue2', style='filled')

def getShortName(fullName):
    array = fullName.split(' ')
    return array[-1]
    if len(array) > 1:
        return  '(' + array[-2]+ ') ' + array[-1]
    else:
        return array[-1]

nodosFinales = []
ids = []
def printTree(tree, depth=0, id='root'):
    maxDepth = 3
    # condition = depth <= maxDepth # only the firsth depths
    condition = True # all levels/depth
    ids.append(id)
    # print('depth', depth)
    if tree is not None:
        if hasattr(tree, 'pointList'):
            # print('tree', dir(tree))
            colY = np.array(tree.pointList)[:,23]
            nodosFinales.append(id)
            print(('-' * depth) + '>', 'depth', depth, 'colY', colY)
            # u1.edge(dependencia, proceso)
            if condition:
                # print('label', 'Y=' + str(colY[0]))
                idNodoFinal = id + 'Final'
                u1.node(idNodoFinal, label='Y=' + str(colY[0]))
                u1.edge(id, idNodoFinal, label='final')
        else:
            # print('depth', depth, 'tree', tree.location, tree.leftChild, tree.rightChild)
            idLeft = id + 'L'
            idRight = id + 'R'
            if condition:
                if id == 'root':
                    u1.node(id, label=getShortName(tree.condition))
                if hasattr(tree.leftChild, 'condition'):
                    u1.node(idLeft, label=getShortName(tree.leftChild.condition))
                    u1.edge(id, idLeft, label='left(yes)')
                if hasattr(tree.rightChild, 'condition'):
                    u1.node(idRight, label=getShortName(tree.rightChild.condition))
                    u1.edge(id, idRight, label='right(no)')
            printTree(tree.leftChild, depth + 1, idLeft)
            printTree(tree.rightChild, depth + 1, idRight)
    else:
        # print('no hay mas nodos en nivel: ' + str(depth))
        return

printTree(tree)

print('cantidad elementos:', len(ids))
print('nodos finales:', len(nodosFinales))

u1.format = 'tiff'
u1.render()