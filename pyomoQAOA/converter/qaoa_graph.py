
#Subroutines for Make_QAOA_Functions.py

class Subgraph:
    #define subgraph class for each edge (u,v) in p=1 QAOA, in terms of 
    #d = deg(u)-1
    #e = deg(v)-1
    #f = number of triangles containing edge (u,v)
    #counts = number of times this subgraph appears
    def __init__(self,d,e,f):
        self.d=min(d,e)
        self.e=max(d,e)
        self.f=f
        self.counts=1

    def add_counts(self):
        self.counts+=1

def Check_new_subgraph(Subgraph_list,graph_new):
    #check if a new graph type is already contained in Subgraphs_list.
    #if it is contained, counts+=1
    #if it is not contained, add it to the list
    Is_new=True
    for graph in Subgraph_list:
        if (graph.e == graph_new.e and graph.d == graph_new.d and graph.f==graph_new.f):
            graph.add_counts()
            Is_new=False
    if Is_new:
        Subgraph_list.append(graph_new)
    return Subgraph_list

def CountSubgraphs(edges):
    Subgraph_list=[]
    #subroutine to identify and count the types of subgraphs
    for edge in edges:
        #use nearby edges to determine subgraph type
        #subgraph is described by 3 parameters: 
        #d,e) number adjacent edges to each vertex (2 parameters)
        #f) number triangles

        #make a blank list to store the connected edges
        connected_edges_vertex0=[] 
        connected_edges_vertex1=[] 
        #degree-1 of 0th and first vertices of edge
        #(these start at 0, ignoring the edge between them in the degree count)
        d=0
        e=0
        #number triangles
        f=0
        #edge is a tuple (u,v)
        for c_edge in edges:
            #find all other edges connected to the 0th vertex of edge
            if  c_edge != edge and \
            (c_edge[0] == edge[0] or c_edge[1] == edge[0]):
                connected_edges_vertex0.append(c_edge)
                #count the number of these edges
                d=d+1
            #find all other edges connected to the 1st vertex of edge
            if c_edge != edge and \
            (c_edge[0] == edge[1] or c_edge[1] == edge[1]):
                connected_edges_vertex1.append(c_edge)
                #count the number of these edges
                e=e+1
        #Find all triangles connecting the edge:
        #Loop over the edges connected to vertices 0 and 1 of edge
        #to check if these share a common vertex
        for c_edge in connected_edges_vertex0:
            for c_edge2 in connected_edges_vertex1:
                if (c_edge[0]==c_edge2[0]) or \
                (c_edge[1]==c_edge2[0]) or \
                (c_edge[0]==c_edge2[1]) or \
                (c_edge[1]==c_edge2[1]):
                    #count the number of triangles per edge
                    f = f+1

        Subgraph_list = Check_new_subgraph(Subgraph_list,Subgraph(d,e,f))

    return Subgraph_list


def Analytic_print_cost_function(subgraph_list):
    #write the analytic function for p=1 QAOA, to be fed into Couenne to optimize the angle parameters

    #The analytical functions are taken from 
    #theorem 4, p. 114 of https://arxiv.org/pdf/1805.03265.pdf
    #Note that this corrects a typo in the published version, sin^2(\beta) -> sin^2(2\beta), 
    #see Eq. (14) of https://journals.aps.org/pra/pdf/10.1103/PhysRevA.97.022304

    #Taking m.s = beta, m.t = gamma
    
    C_string="var m.t >= 7;\n"
    C_string=C_string+"var m.s >= 7;\n"
    first_graph=True
    C_string=""
    for graph in subgraph_list:
        if first_graph:
            C_string = C_string+str(graph.counts)+'*(0.5 + 0.25*(sin(4*m.s)*sin(m.t)*(cos(m.t)^'+str(graph.d)\
            +' + cos(m.t)^'+str(graph.e)+') - sin(2*m.s)^2*cos(m.t)^'+str(graph.d+graph.e-2*graph.f)\
            +'*(1-cos(2*m.t)^'+str(graph.f)+')))'
            first_graph=False
        else:            
            C_string = C_string+' + '+str(graph.counts)+'*(0.5 + 0.25*(sin(4*m.s)*sin(m.t)*(cos(m.t)^'+str(graph.d)\
            +' + cos(m.t)^'+str(graph.e)+') - sin(2*m.s)^2*cos(m.t)^'+str(graph.d+graph.e-2*graph.f)\
            +'*(1-cos(2*m.t)^'+str(graph.f)+')))'

    C_string=C_string+';'
    return C_string


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


