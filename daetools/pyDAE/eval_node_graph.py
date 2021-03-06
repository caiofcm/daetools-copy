"""********************************************************************************
                            eval_node_graph.py
                 DAE Tools: pyDAE module, www.daetools.com
                 Copyright (C) Dragan Nikolic
***********************************************************************************
DAE Tools is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License version 3 as published by the Free Software
Foundation. DAE Tools is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with the
DAE Tools software; if not, see <http://www.gnu.org/licenses/>.
********************************************************************************"""
from pyCore import *
from pyDealII import *
try:
    import pygraphviz as pgv
except Exception as e:
    print(str(e))
    
class daeNodeGraph(object):
    def __init__(self, rootLabel, node):
        # node is a Runtime Node object
        self.counter = 0

        self.graph = pgv.AGraph()
        self.graph.add_node('__root__', label = rootLabel)

        self._processNode('__root__', node)
    
    def SaveGraph(self, filename, layout = 'dot'):
        # Layouts: dot|neato|circo|twopi|fdp|nop
        # The best layout is made by 'dot'
        self.graph.layout(layout)
        self.graph.draw(layout + '-' + filename)

    def _newLeaf(self, parent, labelChild, shape='ellipse', color='black', fontcolor='black', edgeLabel='', edgeColor='gray50'):
        child = str(self.counter)
        self.counter += 1
        
        self.graph.add_node(child, label = str(labelChild), shape = shape, color = color, fontcolor = fontcolor)
        self.graph.add_edge(parent, child, label = edgeLabel, color = edgeColor)
        
        return child

    def _processNode(self, parent, node, edgeLabel=''):
        if isinstance(node, adConstantNode):
            label = '%.15e' % node.Quantity.value
            child = self._newLeaf(parent, label, color='darkorchid', fontcolor='darkorchid', edgeLabel=edgeLabel)
        
        elif isinstance(node, adTimeNode):
            label = 'time'
            child = self._newLeaf(parent, label, color='black', edgeLabel=edgeLabel)

        elif isinstance(node, adUnaryNode):
            if node.Function == eSign:
                label = '-'

            elif node.Function == eSqrt:
                label = 'sqrt'

            elif node.Function == eExp:
                label = 'exp'

            elif node.Function == eLog:
                label = 'log10'

            elif node.Function == eLn:
                label = 'log'

            elif node.Function == eAbs:
                label = 'abs'

            elif node.Function == eSin:
                label = 'sin'

            elif node.Function == eCos:
                label = 'cos'

            elif node.Function == eTan:
                label = 'tan'

            elif node.Function == eArcSin:
                label = 'asin'

            elif node.Function == eArcCos:
                label = 'acos'

            elif node.Function == eArcTan:
                label = 'atan'

            elif node.Function == eCeil:
                label = 'ceil'

            elif node.Function == eFloor:
                label = 'floor'

            elif node.Function == eSinh:
                label = 'sinh'

            elif node.Function == eCosh:
                label = 'cosh'

            elif node.Function == eTanh:
                label = 'tanh'

            elif node.Function == eArcSinh:
                label = 'asinh'

            elif node.Function == eArcCosh:
                label = 'acosh'

            elif node.Function == eArcTanh:
                label = 'atanh'

            elif node.Function == eErf:
                label = 'erf'
                
            else:
                raise RuntimeError('Not supported unary function: %s' % node.Function)
            
            child = self._newLeaf(parent, label, shape='ellipse', color='black', edgeLabel=edgeLabel)
            self._processNode(child, node.Node)

        elif isinstance(node, adBinaryNode):
            if node.Function == ePlus:
                label = '+'

            elif node.Function == eMinus:
                label = '-'

            elif node.Function == eMulti:
                label = '*'

            elif node.Function == eDivide:
                label = '/'

            elif node.Function == ePower:
                label = '**'

            elif node.Function == eMin:
                label = 'min'

            elif node.Function == eMax:
                label = 'max'

            elif node.Function == eArcTan2:
                label = 'atan2'

            else:
                raise RuntimeError('Not supported binary function: %s' % node.Function)
            
            child = self._newLeaf(parent, label, shape='circle', color='black', edgeLabel=edgeLabel)
            self._processNode(child, node.LNode, edgeLabel='')
            self._processNode(child, node.RNode, edgeLabel='')

        elif isinstance(node, adDomainIndexNode):
            label = '%s[%d]' % (node.Domain.Name, node.Index)
            child = self._newLeaf(parent, label, color='black', edgeLabel=edgeLabel)

        elif isinstance(node, adRuntimeParameterNode):
            label = '%s%s' % (node.Parameter.Name, node.DomainIndexes)
            child = self._newLeaf(parent, label, color='green', fontcolor='green', edgeLabel=edgeLabel)

        elif isinstance(node, adRuntimeVariableNode):
            label = '%s%s' % (node.Variable.Name, node.DomainIndexes)
            child = self._newLeaf(parent, label, color='blue', fontcolor='blue', edgeLabel=edgeLabel)

        elif isinstance(node, adRuntimeTimeDerivativeNode):
            label = 'dt(%s%s)' % (node.Variable.Name, node.DomainIndexes)
            child = self._newLeaf(parent, label, color='red', fontcolor='red', edgeLabel=edgeLabel)

        elif isinstance(node, adFloatCoefficientVariableSumNode):
            items = node.sum.values()
            #if len(items) > 0:
            #    index,item_0 = items[0]
            #    label = 'sum(c_j*%s(j))' % item_0.variable.Name
            #else:
            #    label = 'sum(c_j*var(j))'
            label = 'SUM'
            child = self._newLeaf(parent, label, color='green', fontcolor='green', edgeLabel=edgeLabel)
            
            label = '%.15e' % node.base
            child = self._newLeaf(child, label, color='darkorchid', fontcolor='darkorchid', edgeLabel=edgeLabel)
                
            for overallIndex,item in items:
                label = '%.15e * %s(%d)' % (item.coefficient, item.variable.Name, overallIndex-item.variable.OverallIndex)
                child = self._newLeaf(child, label, color='darkorchid', fontcolor='darkorchid', edgeLabel=edgeLabel)
                
        else:
            raise RuntimeError('Not supported node: %s' % type(node))

class daeComputeStackGraph(object):
    def __init__(self, rootLabel, computeStackItems):
        # node is a Runtime Node object
        self.counter = 0

        self.graph = pgv.AGraph()
        self._processItems(computeStackItems)
    
    def SaveGraph(self, filename, layout = 'dot'):
        # Layouts: dot|neato|circo|twopi|fdp|nop
        # The best layout is made by 'dot'
        self.graph.layout(layout)
        self.graph.draw(layout + '-' + filename)

    def _addNode(self, labelChild, shape='ellipse', color='black', fontcolor='black', edgeLabel='', edgeColor='gray50'):
        child = str(self.counter)
        self.counter += 1
        
        self.graph.add_node(child, label = str(labelChild), shape = shape, color = color, fontcolor = fontcolor)
        
        return child

    def _processItems(self, computeStackItems):
        lvalue = []
        rvalue = []
        value  = []
        for item in computeStackItems:
            print(item)
            if item.opCode == eOP_Constant:
                label = '%.6e' % item.value
                child = self._addNode(label, color='darkorchid', fontcolor='darkorchid')
            
            elif item.opCode == eOP_Time:
                label = 'time'
                child = self._addNode(label, color='black')

            elif item.opCode == eOP_InverseTimeStep:
                label = '1/dt'
                child = self._addNode(label, color='black')

            elif item.opCode == eOP_Unary:
                label = str(item.function)            
                child = self._addNode(label, shape='ellipse', color='black')
                arg_node = value.pop()
                self.graph.add_edge(child, arg_node, color = 'gray50')

            elif item.opCode == eOP_Binary:
                label = ''
                if item.function == ePlus:
                    label = '+'
                elif item.function == eMinus:
                    label = '-'
                elif item.function == eMulti:
                    label = '*'
                elif item.function == eDivide:
                    label = '/'
                elif item.function == ePower:
                    label = '**'
                elif item.function == eMin:
                    label = 'min'
                elif item.function == eMax:
                    label = 'max'
                elif item.function == eArcTan2:
                    label = 'atan2'
                child = self._addNode(label, shape='circle', color='black')
                l_node = lvalue.pop()
                r_node = rvalue.pop()
                self.graph.add_edge(child, l_node, color = 'gray50')
                self.graph.add_edge(child, r_node, color = 'gray50')

            elif item.opCode == eOP_DegreeOfFreedom:
                if hasattr(item, 'variableName') and item.variableName != '':
                    label = '%s(overallIndex=%d, dofIndex=%d)' % (item.variableName, item.overallIndex, item.blockIndex)
                else:
                    label = 'var(overallIndex=%d, dofIndex=%d)' % (item.overallIndex, item.blockIndex)
                child = self._addNode(label, color='blue', fontcolor='blue')

            elif item.opCode == eOP_Variable:
                if hasattr(item, 'variableName') and item.variableName != '':
                    label = '%s(overallIndex=%d, blockIndex=%d)' % (item.variableName, item.overallIndex, item.blockIndex)
                else:
                    label = 'var(overallIndex=%d, blockIndex=%d)' % (item.overallIndex, item.blockIndex)
                child = self._addNode(label, color='blue', fontcolor='blue')

            elif item.opCode == eOP_TimeDerivative:
                if hasattr(item, 'variableName') and item.variableName != '':
                    label = 'dt(%s){overallIndex=%d, blockIndex=%d}' % (item.variableName, item.overallIndex, item.blockIndex)
                else:
                    label = 'dt{overallIndex=%d, blockIndex=%d}' % (item.overallIndex, item.blockIndex)
                child = self._addNode(label, color='red', fontcolor='red')
                    
            else:
                raise RuntimeError('Not supported node: %s' % type(node))

            if item.resultLocation == eOP_Result_to_value:
                value.append(child)
            elif item.resultLocation == eOP_Result_to_lvalue:
                lvalue.append(child)
            elif item.resultLocation == eOP_Result_to_rvalue:
                rvalue.append(child)
    
