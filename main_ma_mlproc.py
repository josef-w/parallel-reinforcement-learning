#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 14:02:57 2018

@author: shuyanwang
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 16:15:59 2018

@author: shuyanwang
"""
from agent import agent
import numpy as np
import time
import matplotlib.pyplot as plt
import multiprocessing as mp
# =============================================================================
# time1=time.clock()
# a=1
# b=1
# Q_master=np.zeros([16,16,4])
# terminal_trail=np.zeros([6,9])
# delay_step=1000
# num_agent=4
# =============================================================================
##############################
def compare_data(master,slave,map_):
    for[x,y] in map_:
       for a in range(4):
           if master[x][y][a]<=slave[x][y][a]:
               master[x][y][a]=slave[x][y][a]
def train(q,a,b,num_agent,delay_step):
##########set the programe information####
    time1=time.clock()
    wdir='best_value/q_map%d_%d.npy'%(a,b)
    map_info='map/map%d_%d.npy'%(a,b)
    map_=np.load(map_info)
    map_=map_.tolist()
    epsilon=0.1
    agent_info={"learning_rate":0.1,"discount":0.95}
    bestq= np.load(wdir)
    bestpolicy=np.zeros([16,16,1],dtype=int)
    bestpolicy=bestpolicy.tolist()
    policy=np.zeros([16,16,1],dtype=int)
    policy=policy.tolist()

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
    ##############################################
    erro=[]
    policy_conv=[]
    policy_conv_better=[]
    count=0 
    #########initialize multi-agent################
    for i in range(1,num_agent+1):  
        name='agent'+str(i)  
        locals()[name]=agent(agent_info,map_info)            
     
    #########main loop##################       
    for t in range(1,2001):
         for i in range(1,num_agent+1):
             name='agent'+str(i)
             locals()[name].reset()
    ###########per episode########### 
         for i in range(1,1001):
             count+=1
             for agent_i in range (1,num_agent+1):
                 name='agent'+str(agent_i)
                 if locals()[name].done:
                     pass
                 else:
                     locals()[name].move()
    ######compare the update data from agents to get the best master qsa#####
             if count%delay_step==0:
                 for agent_i in range(1,num_agent+1):
                     name='agent'+str(agent_i)
                     slave=locals()[name].output_qfunc()
                     compare_data(Q_master,slave,map_)
    ######copy the master qsa to slave ###########
                 for agent_i in range(1,num_agent+1):
                     name='agent'+str(agent_i)
                     locals()[name].qfunc=Q_master
                 count=0
    ######judge the end of training#########
         if (t%2000)==0:   
    #######judge the policy#########
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
             if n_better==175:
                 break         
    #######save convergence result################
    q.put(Q_master)
#    policy_conv=np.array(policy_conv)  
#    policy_conv_better=np.array(policy_conv_better)
# =============================================================================
#     wdir='converge_speed_ma/4agent_1000/map%d_%d_conv.npy'%(a,b)
#     np.save(wdir,policy_conv)
#     wdir='converge_speed_ma/4agent_1000/map%d_%d_conv_better.npy'%(a,b)
#     np.save(wdir,policy_conv_better)
#     #global terminal_trail
#     terminal_trail[a][b]=t 
# =============================================================================
    time2=time.clock()        
    print('map%d_%d is over,trail=%d,time=%f'%(a,b,t,time2-time1))
#######main###########
if __name__=='__main__':
    time1=time.clock()
    a=1
    b=1
    Q_master=np.zeros([16,16,4])
    terminal_trail=np.zeros([6,9])
    delay_step=1000
    num_agent=3
    q=mp.Queue()
    p1=mp.Process(target=train,args=(q,a,b,num_agent,delay_step))
    p1.start()
    res=q.get()
    #for a in range(1,3):
    #    for b in range(1,9):
    
    train(a,b,num_agent,delay_step)
    
    ###########################
    #wdir='converge_speed_ma/4agent_1000/terminal_trail.npy'
    #np.save(wdir,terminal_trail)
    time2=time.clock()
    print(time2-time1)
