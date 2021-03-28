#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 16:08:45 2018

@author: shuyanwang
"""
"""
block1:(7,1),block2:(9,7),block3:none,block4:(15,13),block5:none
"""
import numpy as np
import random


for a in range(5,6):
  block=np.load('map_75/block%d.npy'%a)
  block=block.tolist()  
  for b in range(5,6):  
        allowed_state=[]
        for x  in range(1,16):
            for y in range(1,16):        
                s=[x,y]
                #print(s)
# =============================================================================
#                 if a==1 and(s not in block)and (s not in [[10,6]]):            
#                    allowed_state.append(s)
#                 if a==2 and(s not in block)and (s not in [[9,8],[15,8],[6,15],[9,15]]):            
#                    allowed_state.append(s) 
#                 if a==3 and(s not in block)and (s not in [[2,1],[9,1]]):            
#                    allowed_state.append(s)
#                 if a==4 and(s not in block)and (s not in [[6,4],[15,11],[1,6]]):            
#                    allowed_state.append(s)
#                 if a==5 and(s not in block)and (s not in [[15,13]]):            
#                    allowed_state.append(s)
# =============================================================================
                if a==1 and(s not in block)and (s not in [[1,1]]):            
                     allowed_state.append(s)  
                else:
                    if a==5 and(s not in block)and (s not in [[5,5]]):            
                     allowed_state.append(s)
                    else:
                        if s not in block :
                           allowed_state.append(s)
        goal=random.choice(allowed_state)
        allowed_state.append(goal)
        map_=np.array(allowed_state)
        wdir='map_25/map%d_%d.npy'%(a,b)
        np.save(wdir,map_)

















