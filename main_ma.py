#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 16:15:59 2018

@author: shuyuanwang
"""
from agent import agent
import numpy as np
import time
import matplotlib.pyplot as plt
import os
time1=time.clock()
##############################
def compare_data(master,slave,map_):
    for[x,y] in map_:
       for a in range(4):
           if master[x][y][a]<=slave[x][y][a]:
               master[x][y][a]=slave[x][y][a]
def train(a,b,num_agent,delay_step):
##########set the programe information####
    Q_master=np.zeros([16,16,4])
    Q_master=Q_master.tolist()
    time1=time.clock()
    wdir='best_value_50/q_map%d_%d.npy'%(a,b)
    map_info='map_50/map%d_%d.npy'%(a,b)
    map_=np.load(map_info)
    map_=map_.tolist()
    epsilon=0.1
    agent_info={"learning_rate":0.1,"discount":0.95}
    bestq= np.load(wdir)
    bestpolicy=np.zeros([16,16,1],dtype=int)
    bestpolicy=bestpolicy.tolist()
    policy=np.zeros([16,16,1],dtype=int)
    policy=policy.tolist()
    finish=[1]
    #time2=time.clock()
    #print(2,time2-time1)
    #########initialize multi-agent################
    for i in range(1,num_agent+1):  
        name='agent'+str(i)  
        locals()[name]=agent(agent_info,map_info)
        finish.append(0)
    #time3=time.clock()
    #print(3,time3-time2)
    #########make the list of policy###############
    for x in range(0,16):
        for y in range(0,16):
            if [x,y] in map_:
               bestpolicy[x][y]=[] 
               bestpolicy[x][y].append(np.argmax(bestq[x][y]))
               for i in range(bestpolicy[x][y][0],4):
                   if bestpolicy[x][y][0]!=i:
                      if abs(bestq[x][y][bestpolicy[x][y][0]]-bestq[x][y][i])<0.5: 
                         bestpolicy[x][y].append(i)     
            else:
                bestpolicy[x][y]=-1
                policy[x][y]=-1
    #time4=time.clock()
    #print(4,time4-time3)
    ##############################################
    policy_conv=[]
    policy_conv_better=[]
    count=0      
    #########main loop##################       
    for t in range(1,500001):
         for i in range(1,num_agent+1):
             name='agent'+str(i)
             locals()[name].reset()
    ###########per episode########### 
         for i in range(1,1001):
             count+=1
    ##########per agent##############
             for agent_n in range (1,num_agent+1):
                 name='agent'+str(agent_n)
                 if locals()[name].done:
                     finish[agent_n]=1
                 else:
                     locals()[name].move()    
    ######compare the update data from agents to get the best master qsa#####
             #timedelay1=time.clock()
             if count%delay_step==0:
                 for agent_i in range(1,num_agent+1):
                     name='agent'+str(agent_i)
                     slave=locals()[name].output_qfunc()
                     for[x,y] in map_:
                        for ac in range(4):
                            if Q_master[x][y][ac]<=slave[x][y][ac]:
                               Q_master[x][y][ac]=slave[x][y][ac]
                     del  slave,ac,name
    ######copy the master qsa to slave ###########
                 for agent_i in range(1,num_agent+1):
                     name='agent'+str(agent_i)
                     locals()[name].qfunc=Q_master
                 count=0
             if 0 not in finish :
                 finish=0
                 finish=[1]        
                 break
             #timedelay2=time.clock()
    ######judge the end of training#########
         if (t%2000)==0:   
    #######judge the policy#########
             name='agent'+str(1)
             Q_master=locals()[name].qfunc
             n_better=0
             n=0
             for [x,y] in map_:             
                 policy[x][y]=[]                     
                 amax=np.argmax(Q_master[x][y])
                 if amax in bestpolicy[x][y]:
                     n+=1
                 for i in range(0,4):                         
                        if abs(Q_master[x][y][amax]-Q_master[x][y][i])<0.5: 
                           policy[x][y].append(i)                               
                 if bestpolicy[x][y]==policy[x][y]:
                    n_better+=1
             policy_conv.append(n)
             policy_conv_better.append(n_better)
             #time8=time.clock()
             #print(8,time8-time7)
             if n>=(len(map_)-1):
                 del n_better,n,amax,count,bestpolicy,policy
                 break         
    #######save convergence result################
    policy_conv=np.array(policy_conv)  
    policy_conv_better=np.array(policy_conv_better)
    wdir='converge_speed_ma_25/%dagent_%d/map%d_%d_conv.npy'%(num_agent,delay_step,a,b)
#    np.save(wdir,policy_conv)
    wdir='converge_speed_ma_25/%dagent_%d/map%d_%d_conv_better.npy'%(num_agent,delay_step,a,b)
#    np.save(wdir,policy_conv_better)
    time2=time.clock()        
    #print('map%d_%d is over,agent=%d,delay=%d,trail=%d,time=%f'%(a,b,num_agent,delay_step,t,time2-time1))
    return t/2000
#######main###########

delay_step=6000
sum_=0
for a in range(1,6):
    for b in range(1,6):
        num=50
        sum_+=train(a,b,num,delay_step)
print(sum_/25)
sum_=0
for a in range(1,6):
    for b in range(1,6):
        num=100
        sum_+=train(a,b,num,delay_step)
print(sum_/25)

# =============================================================================
# mistake=np.load('mistake2.npy')
# for [num_agent,delay_step,a,b] in mistake:
#     train(a,b,num_agent,delay_step)
# =============================================================================
# =============================================================================
# for delay in 4000,6000,8000,10000,12000:
#     for num in range(2,11):
#         for a in range(1,6):
#             for b in range(1,6):
#                 train(a,b,num,delay)
# =============================================================================

#time.sleep(10)
#os.system("shutdown")