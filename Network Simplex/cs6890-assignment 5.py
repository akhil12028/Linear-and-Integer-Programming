# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 03:15:59 2017

@author: akhil
"""

G = {
    "node": [{"point":1, "balance":12},{"point":2, "balance":7},{"point":3, "balance":3},{"point":4, "balance":-8},
             {"point":5, "balance":-14}],
    "arc": [{"sp":1,"ep":2,"cost":2},{"sp":1,"ep":3,"cost":3},{"sp":1,"ep":4,"cost":4},{"sp":2,"ep":3,"cost":4},
            {"sp":2,"ep":5,"cost":3},{"sp":3,"ep":4,"cost":1},{"sp":3,"ep":5,"cost":5},{"sp":4,"ep":5,"cost":6},
            {"sp":5,"ep":-1,"cost":0}]
    }

T = {
    "node": [{"point":1},{"point":2},{"point":3},{"point":4},{"point":5}],
    "arc": [{"sp":1,"ep":3},{"sp":1,"ep":4},{"sp":2,"ep":3},{"sp":3,"ep":5},{"sp":5,"ep":-1}]
    }
import copy

class NetSimplex:
    
    def __init__(self,G,T):
        self.G = G
        self.T = T
        
    def degree(self,node,tree):
        val = 0
        for arc in tree:
            if arc["sp"] == node:
                val = val+1 
        for arc in tree:
            if arc["ep"] == node:
                val = val+1
        return val
        
    def endNode(self,tree):
        for node in self.G['node']:
            point = node['point'] 
            if self.degree(point,tree) == 1:
                return point
            
    def nodeArcs(self,node,tree):
        val = []
        for arc in tree:
            if arc["sp"] == node or arc["ep"] == node:
                val.append(arc)
        return val
    
    def equalArcs(self,arc1,arc2):
        if arc1["sp"] == arc2["sp"] and arc1["ep"] == arc2["ep"]:
            return True
        return False
        
    def balance(self,point):
        for node in G['node']:
            if node['point'] == point:
                val = node['balance']
        return val
    
    def updateBalance(self,point,flow):
        for node in G['node']:
            if node['point'] == point:
                node['balance']=node['balance']+flow
        
    def computeFlow(self):
        k = copy.deepcopy(self.T['arc'])
        for i in range(0,len(k)):
            end = self.endNode(k)
            node_arcs = self.nodeArcs(end,k)
            end_arc = node_arcs[0]
            if end_arc["sp"] != -1 and end_arc["ep"] != -1:
                for arc in self.T['arc']:
                    if self.equalArcs(arc,end_arc):
                        if arc["sp"] == end:
                            arc["flow"] = self.balance(end)
                            self.updateBalance(arc["ep"],arc["flow"])
                        if arc["ep"] == end:
                            arc["flow"] = -1*self.balance(end)
                            self.updateBalance(arc["sp"],-1*arc["flow"])
            for i,arc in enumerate(k):
                if self.equalArcs(arc,end_arc):
                    k.pop(i)
                    
    def rootNode(self,tree):
        for arc in tree:
            if arc["sp"] == -1:
                return arc["ep"]
            if arc["ep"] == -1:
                return arc["sp"]
            
    def nPotential(self,node1,k1):
        val = []
        f = 0
        otherends = self.otherEnds(node1,k1)
        nodearcs1 = self.nodeArcs(node1,k1)
        """
        for arc6 in nodearcs1:
            for i in range(0,len(k1)):
                if arc6 == k1[i]:
                    
        """  
        
        p=[]
        for j in range(len(nodearcs1)):
            for i,arc5 in enumerate(k1):
                for arc6 in nodearcs1:
                    if self.equalArcs(arc5,arc6):
                        
                        k1.pop(i)
                        break    
        
        for arc in nodearcs1:
            
            for arc2 in G['arc']:
                if self.equalArcs(arc,arc2):
                    arc_cost = arc2['cost']
            if arc['sp'] == node1:
                for node in T['node']:
                    if node['point'] == arc['sp']:
                        potential = node['potential'] 
                for node in T['node']:
                    if node['point'] == arc['ep']:
                        node['potential'] = potential - arc_cost

                        val.append(arc['ep'])
            if arc['ep'] == node1:
                
                for node in T['node']:
                    if node['point'] == arc['ep']:
                        potential = node['potential']
                for node in T['node']:
                    if node['point'] == arc['sp']:
                        node['potential'] = potential + arc_cost
                        
                        val.append(arc['sp'])
        
        return {'value': val}
            
                
        
    def computeNodePotential1(self):
        x=[]
        k=copy.deepcopy(self.T['arc'])
        root_node = self.rootNode(k)
        for node in T['node']:
            if node['point'] == root_node:
                node['potential'] = 0
        x.append(root_node)
        pin1=0
        for i,arc in enumerate(k):
            if arc['ep'] == -1:
                k.pop(i)
        while(len(k)>0):    
            for node1 in x:
                y = self.nPotential(node1,k)
                h = y['value']
            x = h
            
            
            
            
            

         
    def nonBasicArcs(self):
        nonbasic = []
        for arc1 in G['arc']:
            basic = False
            for arc2 in T['arc']:
                if self.equalArcs(arc1,arc2):
                    basic = True
            if basic == False:
                nonbasic.append(arc1)
        return nonbasic
                
            
    def computeReducedCost(self):
        nonbasic = self.nonBasicArcs()
        for arc in nonbasic:
            for node in T['node']:
                if node['point'] == arc["sp"]:
                    arc['reduced_cost'] = node['potential']
            for node in T['node']:
                if node['point'] == arc["ep"]:
                    arc['reduced_cost'] = arc['reduced_cost'] - node['potential']
            arc['reduced_cost'] = arc['reduced_cost'] - arc['cost']
        return nonbasic
    
    def isOptimal(self,tree):
        for arc in tree:
            if arc['reduced_cost'] > 0:
                return False
        return True
    
    def computeEnteringArc(self,tree):
        val = 0
        ea = []
        for arc in tree:
            if arc['reduced_cost'] > val:
                val = arc['reduced_cost']
                ea = arc
        return {'sp':ea['sp'],'ep':ea['ep'],'flow':0} 
    
    def otherEnds(self,node,tree):
        otherend = []
        for arc in tree:
            if arc['sp'] == node:
                otherend.append(arc['ep'])
            if arc['ep'] == node:
                otherend.append(arc['sp'])
        return otherend
    
    def endCt(self,start,k,end):
        val = [start]
        end = end
        tree = copy.deepcopy(k)
        p = self.otherEnds(start,tree)
        nodearcs = self.nodeArcs(start,tree)
        for arc1 in nodearcs:
            for i,arc2 in enumerate(tree):
                if self.equalArcs(arc1,arc2):
                    tree.pop(i)
        if len(p) == 0:
            val.pop()
            return {'Result':False,'value':val} 
        for h in p:
            if h == end:
                val.append(h)
                return {'Result':True,'value':val}
        for h in p:
            z = self.endCt(h,tree,end)
            if z['Result']:
                for i in z['value']:
                    val.append(i)
                return {'Result':True,'value':val}
        
       
    def flowInduction(self,ea):
            oppflow = []
            sameflow = []
            var = 9999999999
            cycle = self.endCt(ea['sp'],self.T['arc'],ea['ep'])['value']
            for arc in self.T['arc']:
                if arc['sp'] == cycle[0] and arc['ep'] == cycle[1]:
                    oppflow.append(arc)
                if arc['sp'] == cycle[1] and arc['ep'] == cycle[0]:
                    sameflow.append(arc)
            for i in range(1,len(cycle)-1):
                for arc in self.T['arc']:
                    if arc['sp'] == cycle[i] and arc['ep'] == cycle[i+1]:
                        oppflow.append(arc)
                    if arc['sp'] == cycle[i+1] and arc['ep'] == cycle[i]:
                        sameflow.append(arc)
            for arc in oppflow:
                if arc['flow'] < var:
                    var = arc['flow']
                    da = arc
                    
            delta = da['flow']
            for arc in self.T['arc']:
                if arc in oppflow:
                    arc['flow'] = arc['flow'] - delta
                if arc in sameflow:
                    arc['flow'] = arc['flow'] + delta
                       
            ea['flow'] = delta
            self.T['arc'].append(ea)
            for i,arc in enumerate(self.T['arc']):
                if arc['sp'] == da['sp'] and arc['ep'] == da['ep']:
                    self.T['arc'].pop(i)
            return
    
                        
               
    def doSimplex(self):
        self.computeFlow()
        while True:
            self.computeNodePotential1()
            reduced_Cost = self.computeReducedCost()
            if self.isOptimal(reduced_Cost):
                return
            ea = self.computeEnteringArc(reduced_Cost)
            self.flowInduction(ea)
            self.T = self.T
 
                
                    
    
"""                    
One Iteration is Working.
NodePotential function is giving error in 2nd iteration.
Solution for Problem 2 is 
X12* = 7
X14* = 5
X25* = 14 
X34* = 3
Z* = 79

I did the work on paper.
"""
                
            


M = NetSimplex(G,T)
M.computeFlow()
M.computeNodePotential1()
"""
"""
reduced_Cost = M.computeReducedCost()
ea = M.computeEnteringArc(reduced_Cost)
M.flowInduction(ea)
print("The solution after 1st iteration is",M.T['arc'])
print("\nOne Iteration is Working.\nNodePotential function is giving error in 2nd iteration.\nSolution for Problem 2 is \nX12* = 7\nX14* = 5\nX25* = 14 \nX34* = 3\nZ* = 79")
G1 = M.G
T1 = M.T

M1 = NetSimplex(G1,T1)

#M1.computeNodePotential()
#M.computeNodePotential()


"""  
           
    def computeNodePotential(self):
        z = len(self.T['node'])
        k = copy.deepcopy(self.T['arc'])
        x = []
        root_node = self.rootNode(k)
        for node in T['node']:
            if node['point'] == root_node:
                node['potential'] = 0
                z = z-1
        x.append(root_node)
        print("root is",root_node)                        
        while z>0:
            for node1 in x:
                print(node1)
                h=[]
                node_arcs = self.nodeArcs(node1,k)
                for arc in node_arcs:
                    for i,arc3 in enumerate(k):
                        if self.equalArcs(arc,arc3):
                            k.pop(i)
                            
                    for arc2 in G['arc']:
                        if self.equalArcs(arc,arc2):
                            arc_cost = arc2['cost']
                            
                    if arc["sp"] != -1 or arc["ep"] != -1:
                        if arc["ep"] == node1:
                            for node in T['node']:
                                if node['point'] == arc["ep"]:
                                    potential = node['potential']
                            for node in T['node']:
                                if node['point'] == arc["sp"]:
                                    node['potential'] = potential + arc_cost
                                    z = z-1
                                    h.append(arc["sp"])
                                    
                        if arc["sp"] == node1:
                            for node in T['node']:
                                if node['point'] == arc["sp"]:
                                    potential = node['potential']
                            for node in T['node']:
                                if node['point'] == arc["ep"]:
                                    node['potential'] = potential - arc_cost
                                    z = z-1
                                    h.append(arc["ep"])
                                    
                x=h
                print(x)
"""