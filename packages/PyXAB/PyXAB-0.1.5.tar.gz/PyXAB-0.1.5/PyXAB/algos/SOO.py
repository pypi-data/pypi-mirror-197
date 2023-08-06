# -*- coding: utf-8 -*-
"""Implementation of SOO (Munos, 2011)
"""
# Author: Haoze Li <li4456@purdue.edu>
# License: MIT


import math 
import numpy as np
from PyXAB.algos.Algo import Algorithm
from PyXAB.partition.Node import P_node
import pdb

class SOO_node(P_node):
    def __init__(self, depth, index, parent, domain):
        super(SOO_node, self).__init__(depth, index, parent, domain)
        
        self.visited = False
        self.reward = -np.inf
        
    def update_reward(self, reward):
        self.reward = reward
        
    def get_reward(self):
        return self.reward
    
    def visit(self):
        
        self.visited = True
        

class SOO(Algorithm):
    def __init__(self, n=100, h_max=100, domain=None, partition=None): # TODO: h_max should not be too small otherwise it will be a dead loop.
        super(SOO, self).__init__()
        if domain is None: 
            raise ValueError("Parameter space is not given.")
        if partition is None:
            raise ValueError("Partition of the parameter space is not given.")
        self.partition = partition(domain=domain, node=SOO_node)
        
        self.iteration = 0
        self.n = n
        self.h_max = h_max
        
        self.curr_node = None
        
    def pull(self, time):
        
        self.iteration = time 
        node_list = self.partition.get_node_list()
        flag = False # indicate if we should terminate the iteration
        
        while True: 
            h = 0
            v_max = -np.inf
            while h <= min(self.partition.get_depth(), self.h_max):
                max_value = -np.inf
                max_node = None
                for node in node_list[h]: # for all node in the layer
                    if node.get_children() is None: # if the node is not evaluated, evaluate it 
                        if not node.visited: 
                            node.visit()
                            self.curr_node = node
                            return node.get_cpoint()
                        if node.get_reward() >= max_value: # find the leaf node with maximal reward
                            max_value = node.get_reward() 
                            max_node = node
                if max_value >= v_max:
                    if max_node is not None: # Found a leaf node
                        self.partition.make_children(max_node, newlayer=True)
                        v_max = max_value
                h += 1
            if max_node is None: 
                if flag: # We terminate the outer loop if we cannot find a leaf node that satisfies those conditions
                    return self.partition.get_root().get_cpoint()
                flag = True # We set flag = True iff the loop cannot find the node starting from root.
                
    def receive_reward(self, time, reward):
        
        self.curr_node.update_reward(reward)
        
    def get_last_point(self):
        
        max_value = -np.inf
        max_node = None
        node_list = self.partition.get_node_list()
        for h in range(len(node_list)):
            for node in node_list[h]:
                if node.get_reward() >= max_value:
                    max_value = node.get_reward()
                    max_node = node
        return max_node.get_cpoint()

