import numpy as np
import pandas as pd
import networkx as nx
import random

def n_neighbors(graph,node):
    return len([i for i in graph.neighbors(node)])

def check_both_sides(graph,edge):
    return all(n_neighbors(graph,i) > 1 for i in edge)

def risking_my_life_for_these_cubes(rods, verbose = False):
    
    #First count how many repeat edges
    
    repeats = len(rods) - len(set(rods))

    #Initialize Graph and add the edges. At this point repeat edges are cut.
    
    G = nx.Graph()
    G.add_edges_from(rods)
    
    #Iterate through each edge
    
    cut_counter = 0
    edgelist = list(G.edges)
    
    #Randomly shuffle the list of edges so that the rods are considered in a different sequence each time
    random.shuffle(edgelist)
    
    for edge in edgelist:
        
        #First: Are nodes on both ends of edge connected to another node?
        
        if check_both_sides(G,edge):
            
            #Second: After cut, is the graph still connected?
            
            Aftercut = G.copy()
            Aftercut.remove_edge(edge[0],edge[1])
            
            if nx.is_connected(Aftercut):
                
                if verbose:
                    print('Edge {} has been cut!'.format(edge))
                
                #Cut the rod!
                G.remove_edge(edge[0],edge[1])
                cut_counter += 1
                
                if verbose:
                    print('Cut counter: {}'.format(cut_counter))
                
                
                
            else: 
            
                if verbose:
                    print('Cutting this rod ({}) makes the cubes disconnected'.format(edge))
        
        else:
            
            if verbose:
                print ('Cutting this rod ({}) leaves an isolated cube'.format(edge))
            
            continue
            
    return cut_counter + repeats


#Define a function that runs the algorithm a number of iterations for random permutations of the rod sequence

def compute(rods, iterations = 5000, verbose = False):
    solutions = []
    for i in range(iterations):
        solution = risking_my_life_for_these_cubes(rods = rods,verbose = verbose)
        solutions.append(solution)
    return max(solutions)

#For script

import argparse

parser = argparse.ArgumentParser(description = 'Calculate how many rods can be removed')

parser.add_argument('rods', help = 'List of rods (tuples) connecting the cubes')

args = parser.parse_args()


if __name__ == '__main__':
    
    print(compute(args.rods))