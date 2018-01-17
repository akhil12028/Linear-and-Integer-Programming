# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 11:29:03 2017

@author: akhil
"""
import numpy

class MatrixSimplex:

    def __init__(self,A,b,c,basis):
        self.A = numpy.array(A)
        self.b = numpy.array(b)
        self.c = numpy.array(c)
        self.basis = numpy.array(basis)
    
    def doSimplex(self): 
      while(True):
          value, z = self.ComputeZ()
          Xb = self.ComputeXb()
          if(self.isOptimal(z)):
              print("Z =", value)
              for i in range(0,self.A.shape[1]):
                  k = 0
                  notbasis = 0
                  for j in self.basis:
                      if(i == j):
                          notbasis = 1
                          print("x%d = %d"%(i+1,Xb[k][0]))
                      k = k+1
                  if(notbasis == 0):
                      print("x%d = %d"%(i+1,0))
              return
          
          ev = self.computeEnteringVar(z) 
          if(self.isBounded(ev) == "False"):
                print("The system is not bounded")
                return
          dv = self.minRatioTest(Xb,ev)
            
        
          for i in range(0,self.basis.shape[0]):
              if(self.basis[i] == dv):
                  self.basis[i] = ev
                            
    def ComputeZ(self):
        return (self.Cb().dot(self.B_i())).dot(self.b)[0],-1*(((self.Cb().dot(self.B_i())).dot(self.N()))-self.Cn())
        
    def ComputeXb(self):
        return (self.B_i().dot(self.b))
    
    def isOptimal(self,z):
        k = True
        for i in z:
            if(i > 0):
                k = False
        return k
    
    def computeEnteringVar(self,z):
        var = 0
        val = 0
        for i in range(0,z.shape[0]):
            if(z[i] > val):
                val = z[i]
                var = self.nonBasis()[i]
        return var 
        
    def minRatioTest(self,Xb,ev):
        Xk = self.A[:,ev]
        val = 9223372036854
        for i in range(0,Xb.shape[0]):
            if(Xk[i] > 0):
                if(Xb[i]/Xk[i] < val):
                    val = Xb[i]/Xk[i]
                    k = self.basis[i]
        return k
    
    def nonBasis(self):
        nonbasis = numpy.array([])
        for i in range(0,self.A.shape[1]):
            k=0
            for j in self.basis:
                if i==j:
                    k = 1
            if(k == 0):
                nonbasis = numpy.append(nonbasis,i)
        return nonbasis.astype(int)     
                
    def B(self):
        return self.A[:,self.basis]
    
    def N(self):
        return self.A[:,self.nonBasis()]
    
    def Cb(self):
        cb = numpy.array([])
        for i in self.basis:
            cb = numpy.append(cb,self.c[i])
        return cb  
    
    def Cn(self):
        cn = numpy.array([])
        for i in self.nonBasis():
            cn = numpy.append(cn,self.c[i])
        return cn
    
    def B_i(self):
        return numpy.linalg.inv(self.B())
    
    def isBounded(self,ev):
        Xk = self.A[:,ev]
        k = False
        for i in Xk:
            if(i > 0):
                k = True
        return k
                
    
    
 
        
print("Problem2")
A = [[-1,-1,1,0,0,0],[-3,1,0,1,0,0],[1,0,0,0,1,0],[0,1,0,0,0,1]]
b=[[-3],[1],[2],[2]]
c=[3,1,0,0,0,0]
basis=[2,3,4,5]
M = MatrixSimplex(A,b,c,basis)
M.doSimplex()

"""
Problem2:
    The maximum value of Z is 8 at x1=2 and x2=2.
"""
             
print("Problem3")            
A = [[2,3,1,0,0],[4,3,0,1,0],[0,1,0,0,1]]
b=[[72],[108],[16]]
c=[10,9,0,0,0]
basis= [2,3,4]
M = MatrixSimplex(A,b,c,basis)
M.doSimplex()

"""
Problem3:
    The Optimal Product mix would be 18 ‘A’ chairs and 12 ‘B’ chairs and the profit would be $288.
"""

print("Problem4")
A = [[4,5,1,0,0],[1,3,0,1,0],[8,12,0,0,1]]
b=[[320],[240],[240]]
c=[3,4,0,0,0]
basis= [2,3,4]
M = MatrixSimplex(A,b,c,basis)
M.doSimplex()

"""
Problem4:
    To maximize profit, they should manufacture 30 passenger planes and 0 cargo planes. The profit would be $90.
"""

print("Problem5")
A = [[400,600,1,0,0,0],[200,100,0,1,0,0],[100,0,0,0,1,0],[0,150,0,0,0,1]]
b=[[9600],[2400],[1500],[2100]]
c=[2,4,0,0,0,0]
basis= [2,3,4,5]
M = MatrixSimplex(A,b,c,basis)
M.doSimplex()

"""
Problem5:
    They should make 3 poppy seed cakes and 14 German chocolate cakes to maximize profit. The Profit would be $62.
        1. x3 = 0. This implies that there’s no flour left at the end of the day.
        2. x4 = 400. This implies that 400 grams of butter remain unused at the end of the day.
"""