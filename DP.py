#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 10:26:56 2018

@author: shuyanwang
"""
"""0:x+1 1:y-1 2:y+1 3:x-1"""

import numpy as np
#from env_new import env
#env=env()


# =============================================================================
# for a in range(1,6):
#     for b in range(1,6):
#         dp(a,b)
# =============================================================================

#Qsa=Qsa.tolist()
#V=V.tolist()    
n=0
def one_step_lookahead(s, V,Qsa,goal,load_map):
#    global Qsa
#    global goal
#    global load_map
    for a in range(0,4):
        if a==0:
           next_s=[s[0]+1,s[1]]
        if a==1:
           next_s=[s[0],s[1]-1] 
        if a==2:
            next_s=[s[0],s[1]+1]
        if a==3:
           next_s=[s[0]-1,s[1]]
        if next_s in load_map:
            pass
        else:
            next_s=s 
        #print(next_s,s)
        if next_s== goal:
           Qsa[s[0]][s[1]][a]= 100+(0.95*V[next_s[0]][next_s[1]])
           #print(Qsa[s[0]][s[1]][a])
        else:
           Qsa[s[0]][s[1]][a]= 0+(0.95*V[next_s[0]][next_s[1]])
def dp(a,b):   
    n=0          
    theta=0.000001
    wdir='map_25/block%d.npy'%a
    block=np.load(wdir)
    wdir='map_25/map%d_%d.npy'%(a,b)
    load_map=np.load(wdir)
    load_map=load_map.tolist()
    goal=load_map[len(load_map)-1]
    Qsa=np.zeros([16,16,4])
    V=np.zeros([16,16])
    while True:
    # Stopping condition\n",
          delta = 0
    # Update each state...\n",
          for s in load_map:
    #no use to calculate value of goal
              if s == goal:
                 pass
              else:
    # Do a one-step lookahead to find the best action\n",
                  one_step_lookahead(s, V,Qsa,goal,load_map)
                  best_action_value = np.max(Qsa[s[0]][s[1]])
                  #print(best_action_value)
    # Calculate delta across all states seen so far\n",
                  delta = max(delta, abs(best_action_value - V[s[0]][s[1]]))
    # Update the value function\n",
                  V[s[0]][s[1]] = best_action_value
                  #print(state)
    #print trail
          n+=1
          if (n%100)==0:
             print('the trail now is %d'%n)
                      
    # Check if we can stop \n",
          if delta < theta:
             print(n)
             break
    #action=np.argmax(Qsa[s[6]][s[2]])    
    
    v_wdir='best_value_25/v_map%d_%d.npy'%(a,b)
    qsa_wdir='best_value_25/q_map%d_%d.npy'%(a,b)
    #V=np.array(V)
    #sa=np.array(Qsa)
    np.save(v_wdir,V)
    np.save(qsa_wdir,Qsa)

# =============================================================================
# for a in range(1,6):
#     for b in range(1,6):
#         dp(a,b)  
# =============================================================================
dp(5,5)
V=np.load('best_value_25/v_map%d_%d.npy'%(5,5))












