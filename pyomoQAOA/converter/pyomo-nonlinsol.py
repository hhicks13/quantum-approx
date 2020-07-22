#!/usr/bin/env python3

#
# Graphs to Objective
# Author: Phil
#
#Generate analytical functions for p=1 QAOA for different graphsjj
#The functions will be fed into Couenne to find optimal angles.

#The analytical functions are taken from
#theorem 4, p. 114 of https://arxiv.org/pdf/1805.03265.pdf
#Note that this corrects a typo in the published version, sin^2(\beta) -> sin^2(2\beta),
#see Eq. (14) of https://journals.aps.org/pra/pdf/10.1103/PhysRevA.97.022304

#The output function has
#m.s = beta, m.t = gamma

# Objective to Pyomo
# Author: Harrison
#
#passes QAOA to pyomo, then to couenne

from pyomo.environ import *
import numpy as np
import re
import os
import sys
import time
import numpy


def Read_in_graph_dreadnaught(file,n_vertices):
    edges = []
    f = open(file, "r")
    f.readline() #skip first line
    for n in range (n_vertices):
        line=f.readline()
        m=0
        keepgoing=True
        while keepgoing:
            #read all connected vertices, separated by a space in the file
            #print('m,line[6+m]',m,line[6+m])
            if line[6+m] != ';':
                if m % 2 == 0:
                    #check if the edge is already in edges
                    if (int(line[6+m]),n) not in edges:
                        #if edge is new, add to edges
                        edges.append((n,int(line[6+m])))
                m+=1
            else:
                #stop when the ';' is reached at the end of the line
                keepgoing=False
    f.close()
    return edges

def main():
    try:
        graph_file = open(sys.argv[1],'r')
        n_vertices = int(sys.argv[2])
    except IndexError:
        print('<!> argument should be a FILE')
        print('<x> exiting')
        sys.exit()
    else:
        if sys.argv[1].endswith('.qaoa'):
            import qaoa_graph
            os.system("clear")
            print("processing {}\n".format(graph_file.name))
            m = ConcreteModel()
            ### ###
            m.s = Var(within=NonNegativeReals,
                          bounds=(0,2*numpy.pi),
                          doc='Nonnegative')
            m.t = Var(within=NonNegativeReals,
                          bounds=(0,2*numpy.pi),
                          doc='Nonnegative')
            ### ###
            m.obj = Objective(expr = 0.0, sense = maximize)
            ### ###
            edges = Read_in_graph_dreadnaught(graph_file.name,n_vertices)
            print('edges:',edges)
            subgraph_list = qaoa_graph.CountSubgraphs(edges)
            ### ###

            """ Taken from phil's original version of the code, assumed correct """
            for graph in subgraph_list:
                m.obj.expr += graph.counts*(0.5 + 0.25*(sin(4*m.s)*sin(m.t)*(cos(m.t)**graph.d+cos(m.t)**graph.e)-sin(2*m.s)**2*cos(m.t)**(graph.d+graph.e-2*graph.f)*(1-cos(2*m.t)**graph.f)))
            ### ###
            solver=SolverFactory("couenne")
            results=solver.solve(m,tee=True)
            m.display()
            sys.exit()
if __name__ == "__main__":
    #
    print("<> ARGUMENT COUNT".format(sys.argv))
    #
    for i, arg in enumerate(sys.argv):
        print("<{}>  {}\n".format(i,arg))
    #
    main()


#
# prior code for Make_Functions.py
#
#for n_vertices in range(3,7): #number of vertices
#
#    Directory='Graph'+str(n_vertices)+'/'
#
#    #for each file in the directory, write a new file XXXXXX with the analytical cost function
#    for file in os.listdir(Directory):
#        if file.endswith('.txt'):
#            print('file:',file)
#            edges = Make_QAOA_Functions_sr.Read_in_graph_dreadnaught(Directory+file,n_vertices)
#            print('edges:',edges)
#            subgraph_list=Make_QAOA_Functions_sr.CountSubgraphs(edges)
#            C = Make_QAOA_Functions_sr.Analytic_print_cost_function(subgraph_list)
#
#            f=open(Directory+file[:-4]+'_func.txt','w')
#            f.write(C)
#            f.close()





