# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 12:38:59 2017

@author: akhil
"""
import numpy
class TableauSimplex:
    
    def __init__(self,T):
        self.T=numpy.array(T, dtype=numpy.float64)
        
    def doSimplex(self):
        while(True):
            if self.isZOptimal():
                print("",end="\t")
                for i in range(1,self.T.shape[1]-1):
                    print("x%d"%(i),end="\t")
                print("bs",end="\t")
                print("")
                for i in range(0,self.T.shape[0]):
                    for j in range(0,self.T.shape[1]):
                        if(j==0):
                            if(i==self.T.shape[0]-1):
                                print("z",end="\t")
                            else:
                                print("x%d"%(self.T[i][j]),end="\t")   
                        else:    
                            print(self.T[i][j],end="\t")
                    print("")
                print("")
                return self.T
            ev=self.computeEnteringVar()
            if self.isZUnbounded(ev):
                print("System is Unbounded")
                return 0
            dv=self.minRatioTest(ev)
            self.pivot(ev,dv)
            
        
    def isZOptimal(self):
        for i in range(1,self.T.shape[1]):
            if self.T[-1][i] < 0:
                return False
        return True    
    
    def computeEnteringVar(self):
        var = 0
        val = 0
        for i in range(1,self.T.shape[1]):
            if self.T[-1][i] < val:
                val = self.T[-1][i]
                var = i
        return var
        
    def isZUnbounded(self,ev):
        for i in range(0,self.T.shape[0]-1):
            if self.T[i][ev] > 0:
                return False
            return True
    
    def minRatioTest(self,ev):
        val = 0
        var = 0
        for i in range(0,self.T.shape[0]-1):
            if self.T[i][ev] > 0:
                 k = self.T[i][-1]/self.T[i][ev]
                 if val==0 or k < val:
                     val = k
                     var = i
        return var
    
    def pivot(self,ev,dv):
        self.T=self.T
        self.T[dv][0]=ev
        pivot = self.T[dv][ev]
        for i in range(1,self.T.shape[1]):
            self.T[dv][i]= self.T[dv][i]/pivot
        for i in range(0,self.T.shape[0]):
            if i != dv:
                k = self.T[i][ev]
                for j in range(1,self.T.shape[1]):
                    self.T[i][j]=self.T[i][j]-(k*self.T[dv][j])
              
        

print("Problem2")
T = [[3, 1, 1, 1, 0, 0, 2000], [4, 1, 2, 0, 1, 0, 3000], [5, 90, 60, 0, 0, 1, 150000], [0, -170, -190, 0, 0, 0, 0]]
M = TableauSimplex(T)
M.doSimplex()

print("Problem2a") #increase in personal days by 100.
T = [[3, 1, 1, 1, 0, 0, 2000], [4, 1, 2, 0, 1, 0, 3100], [5, 90, 60, 0, 0, 1, 150000], [0, -170, -190, 0, 0, 0, 0]]
M = TableauSimplex(T)
M.doSimplex()

print("Problem2b") #increase in capital by $100.
T = [[3, 1, 1, 1, 0, 0, 2000], [4, 1, 2, 0, 1, 0, 3000], [5, 90, 60, 0, 0, 1, 150100], [0, -170, -190, 0, 0, 0, 0]]
M = TableauSimplex(T)
M.doSimplex()

"""
Problem 2:
    x1 – no. of acres of crop A
    x2 – no. of acres of crop B
    He should plant 1000 acres of computeEnteringVarrop A and 1000 acres of crop B to maximize the revenue. The maximum revenue would be $360,000.
        1.	If Rick has 100 more person-days available, his annual revenue will increase by 20*100 = $2000 since x4 at maximum Z is 20. Hence the final annual revenue is $362,000.
        2.	If Rick has $100 more available in Capital, his annual revenue will not change. Hence the final annual revenue is $360,000.
"""

print("Problem3")
T=[[3,4,1,1,0,300],[4,2,1,0,1,160],[0,-0.25,-0.1,0,0,0]]
M = TableauSimplex(T)
M.doSimplex()

"""
Problem 3:
    x1 – no. of large muffins
    x2 – no. of small muffins
    They should make 70 large muffins and 20 small muffins to maximize the profit. The maximum profit would be $19.5.
        1.	The dough can be increased to 320 ounces where the profit would be $20. The profit remains the same after this point.
        2.	The bran can be increased to 300 ounces where the profit would be $30. The profit remains the same after this point.
"""

print("Problem4")
T= [[4,10,10,0.3,1,0,0,60],[5,40,20,0.2,0,1,0,50],[6,60,30,0.6,0,0,1,90],[0,-250,-500,-9,0,0,0,0]]
M = TableauSimplex(T)
M.doSimplex()

"""
Problem 4:
    It is a minimization problem. Solving the dual and finding the slack variables at the maximum value is the solution to this problem.
    x4 – no. of 100 grams of apples
    x5 – no. of 100 grams of oranges
    x6 – no. of 100 grams of bananas
    The final values are x4 = 0, x5¬ = 5 and x6 = 13.333
    Hence the optimal combination is 0 grams of apples, 500 grams of oranges and 1333.3 grams of bananas.
"""
