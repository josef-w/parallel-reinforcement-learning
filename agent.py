#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 10:19:46 2018

@author: shuyuanwang
"""
import numpy as np
import random
import time
class agent():
    def __init__(self,agent_info,map_info):
        self.learning_rate=agent_info["learning_rate"]#beta
        self.discount=agent_info["discount"]
        self.qfunc=self.initialize_q()
        self.allowed_action=[0,1,2,3]
        self.epsilon=0.1
########set map##########################
        self.x=1
        self.y=1
        self.done=False
        self.count=0
        self.wdir=map_info
        self.map=np.load(self.wdir)        
        self.map=self.map.tolist()
        self.goal=self.map[len(self.map)-1]
    def initialize_q(self):
        load_qsa=np.zeros([16,16,4])
        self.qfunc=load_qsa
        return load_qsa
    def choose_action(self):
        a=self.epsilon_greedy(self.x,self.y)
        return a
    def greedy(self,x,y):
        qmax=self.qfunc[x][y][0]
        amax=[0]
        for i in range(len(self.qfunc[x][y])):
            q=self.qfunc[x][y][i]
            if qmax<q:
                qmax=q
                amax=[i]
            if qmax==q:
               amax.append(i)
        return random.choice(amax)
    def epsilon_greedy(self,x,y):
        choice=random.random()
        x=x
        y=y
        if self.epsilon<=choice:
           return self.greedy(x,y)
        else:
           return random.choice(self.allowed_action) 
    def output_qfunc(self):
        return self.qfunc
    def move(self):
        x=self.x
        y=self.y
        a=self.choose_action()
        r=0
#######first assume it is an empty place#######
        if a==0:
           next_s=[x+1,y]
        if a==1:
           next_s=[x,y-1] 
        if a==2:
           next_s=[x,y+1]
        if a==3:
           next_s=[x-1,y]
        if next_s in self.map:
            x=next_s[0]
            y=next_s[1]
        else:
            x=self.x
            y=self.y
            
########if reach the goal##########
        if x==self.goal[0] and y==self.goal[1]:
            r=100
            self.done = True 
        ac1=self.greedy(x,y)
        self.qfunc[self.x][self.y][a]+=self.learning_rate*(r+self.discount*self.qfunc[x][y][ac1]-self.qfunc[self.x][self.y][a])  
        self.x=x
        self.y=y
    def reset(self):
        while True:
            reset=random.choice(self.map)
            self.x=reset[0]
            self.y=reset[1]
            self.done=False
            if reset!=self.goal:
                break
        return reset


# =============================================================================
# time1=time.clock()
# def train(a,b,num_agent,delay_step):
#     map_info='map/map%d_%d.npy'%(a,b)
#     policy=np.zeros([16,16],dtype=int)
#     policy=policy.tolist()
#     bestpolicy=np.zeros([16,16,1],dtype=int)
#     bestpolicy=bestpolicy.tolist()
#     bestq=np.load('best_value/q_map%d_%d.npy')%(a,b)
#     Q_master=np.zeros([16,16,4])
#     Q_master=Q_master.tolist()
#     count=0
#     policy_conv=[]
#     policy_conv_better=[]
#     agent_info={"learning_rate":0.1,"discount":0.95}
#     finish=[1]
#     delay_step=6000
#     num_agent=8
#     for i in range(1,num_agent+1):  
#         name='agent'+str(i)
#         locals()[name]=agent(agent_info,map_info)
#         
#     
#     map_=np.load(map_info)            
#     for x in range(0,16):
#         for y in range(0,16):
#             if [x,y] in map_: 
#                bestpolicy[x][y]=[]
#                bestpolicy[x][y].append(np.argmax(bestq[x][y]))
#                for i in range(bestpolicy[x][y][0],4):
#                    if bestpolicy[x][y][0]!=i:
#                       if abs(bestq[x][y][bestpolicy[x][y][0]]-bestq[x][y][i])<0.5: 
#                          bestpolicy[x][y].append(i)     
#             else:
#                 bestpolicy[x][y]=-1
#                 policy[x][y]=-1
#     timetest1=[]
#     for t in range(1,100001):
#          finish=[1]    
#          for i in range(1,num_agent+1):
#              name='agent'+str(i)
#              locals()[name].reset() 
#              #print(name,locals()[name].x,locals()[name].y)
#              finish.append(0)
#     ###########per episode###########
#          #time0=time.clock()
#          for i in range(1,1001):
#              count+=1
#              for agent_i in range (1,num_agent+1):
#                  name='agent'+str(agent_i)
#                  if locals()[name].done:
#                      finish[agent_i]=1
#                  else:
#                      locals()[name].move()
#              if count%delay_step==0:
#                  for agent_i in range(1,num_agent+1):
#                      name='agent'+str(agent_i)
#                      slave=locals()[name].output_qfunc()
#                      for[x,y] in map_:
#                         for ac in range(4):
#                             if Q_master[x][y][ac]<=slave[x][y][ac]:
#                                Q_master[x][y][ac]=slave[x][y][ac]
#                      del  slave,ac,name
#         ######copy the master qsa to slave ###########
#                  for agent_i in range(1,num_agent+1):
#                      name='agent'+str(agent_i)
#                      locals()[name].qfunc=Q_master
#                  count=0        
#              if 0 not in finish :
#                  finish=0
#                  finish=[1]        
#                  break
#          #time0-=time.clock()
#          #timetest1.append(time0)
#          if (t%2000)==0:   
#         #######judge the policy#########
#              n_better=0
#              n=0
#              for agent_i in range(1,num_agent+1):   
#                  locals()['qfunc'+str(agent_i)]=locals()['agent'+str(agent_i)].output_qfunc() 
#              for [x,y] in map_:             
#                  policy[x][y]=[]                     
#                  amax=np.argmax(Q_master[x][y])
#                  if amax in bestpolicy[x][y]:
#                      n+=1
#                  for i in range(0,4):                         
#                         if abs(Q_master[x][y][amax]-Q_master[x][y][i])<0.5: 
#                            policy[x][y].append(i)                               
#                  if bestpolicy[x][y]==policy[x][y]:
#                     n_better+=1
#              policy_conv.append(n)
#              policy_conv_better.append(n_better)
#              if n_better==175:
#                  break
# train()
# time2=time.clock()
# time2-=time1
# print(time2)
# =============================================================================
# =============================================================================
# wdir='converge_speed/map%d_%d_conv.npy'%(a,b)
# single_conv=np.load(wdir)
# wdir='converge_speed/map%d_%d_conv_better.npy'%(a,b)
# single_conv_better=np.load(wdir)       
# =============================================================================
# =============================================================================
# for agent_i in range(1,4):
#     for t in range(100000):
#         locals()['agent'+str(agent_i)].reset()
#         for i in range(1000):
#             locals()['agent'+str(agent_i)].move()
#             if locals()['agent'+str(agent_i)].done:
#                 break
#for agent_i in range(1,4):   
#    locals()['qfunc'+str(agent_i)]=locals()['agent'+str(agent_i)].output_qfunc()        
#for x in range(0,16):
#     for y in range(0,16):
#         if [x,y] in map_:
#            policy[x][y]=np.argmax(qfunc1[x][y])    
#         else:
#             policy[x][y]=-1
# =============================================================================
