import random as rnd
import state as st
import main
import csv
import math
import json

decayRate=0.0005
epMin=0.05
epMax=1.0
constant=0.9
learningRate=0.1
def Training1(valid): #Always 'O'
    global decayRate
    global epMin
    global epMax
    global constant
    global learningRate
    epsilon=epMin+(epMax-epMin)*math.exp(-1*st.count*decayRate)
    State1=st.P1Coordinate#[(1,1),(2,2)]
    State2=st.P0Coordinate#[(2,0),(0,0)]

    allCordinates=st.worldPositions#[(0,0),(1,1),(2,2),(2,0),(1,2)]
    tempState=State1+State2
    actionList1 = allCordinates.copy()
    for cord in tempState:
        if cord in actionList1:
            actionList1.remove(cord)

    
            
    #done the below to denote self and opponent; basically encoding
    #similarly action will be:
    
    
    #selection
    
    
    st.returnValueList1.append(main.gamelogic(None,st.playerType[1],None))
    if(valid):
        st.stateList1.append(list(st.boardState1))
        if tuple(st.boardState1) not in st.Q_table1:
            st.Q_table1[tuple(st.boardState1)]=[0.0]*9
        if(actionList1):
            if rnd.random()<epsilon:
                selection = rnd.choice(actionList1)#encoded selection
            else:
                stateKey=tuple(st.stateList1[-1])
                if stateKey not in st.Q_table1:
                    st.Q_table1[stateKey]=[0.0]*9
                qValueList=st.Q_table1[stateKey]
                legalQVals=[(qValueList[encodeIndex(i,j)],[i,j]) for i,j in actionList1]
                selection=max(legalQVals,key=lambda x:x[0])[1]
        else: selection=[0,0] #default selection, not used at all
        st.action1.append(selection)
    else: selection=[0,0]
    if( main.gamelogic(True,None,None)): 
        st.returnValueList1.pop(0)
        for i in range(len(st.stateList1)):
            for j in range(i+1,len(st.returnValueList1)): 
                st.returnValueList1[i]+=st.returnValueList1[j]*(constant)**(j-i)
            st.sampleTrajectory1.append((st.stateList1[i],st.action1[i],st.returnValueList1[i]))
            x,y=st.action1[i][0],st.action1[i][1]
            val=st.Q_table1[tuple(st.stateList1[i])][x*3+y]
            st.Q_table1[tuple(st.stateList1[i])][x*3+y]=val+(st.returnValueList1[i]-val)*learningRate
                
        #print(f"Agent 2:{st.Q_table1}")
        #saveEpisodeData("episodeDataCompiledAI1.csv",1)    
        if st.count==st.totalSimulations:
            saveQTable(st.Q_table1,"Agent2Qtable.json")
    return selection

def Training0(valid):#Always 'X'
    global decayRate
    global epMin
    global epMax
    global constant
    global learningRate
    epsilon=epMin+(epMax-epMin)*math.exp(-1*st.count*decayRate)
    State1=st.P0Coordinate#[(1,1),(2,2)]
    State2=st.P1Coordinate#[(2,0),(0,0)]

    allCordinates=st.worldPositions#[(0,0),(1,1),(2,2),(2,0),(1,2)]
    tempState=State1+State2
    actionList0 = allCordinates.copy()
    for cord in tempState:
        if cord in actionList0:
            actionList0.remove(cord)
    
    
    
    st.returnValueList0.append(main.gamelogic(None,st.playerType[0],None)) #its recording return values with offset of 1
    if(valid):
        st.stateList0.append(list(st.boardState0))
        if tuple(st.boardState0) not in st.Q_table0:
            st.Q_table0[tuple(st.boardState0)]=[0.0]*9
        if(actionList0):
            if rnd.random()<epsilon:
                selection = rnd.choice(actionList0)#encoded selection
            else:
                stateKey=tuple(st.stateList0[-1])
                if stateKey not in st.Q_table0:
                    st.Q_table0[stateKey]=[0.0]*9
                qValueList=st.Q_table0[stateKey]
                legalQVals=[(qValueList[encodeIndex(i,j)],[i,j]) for i,j in actionList0]
                selection=max(legalQVals,key=lambda x:x[0])[1]
        else: selection=[0,0] #default selection, not used at all
        st.action0.append(selection)
    else: selection=[0,0]
    if( main.gamelogic(True,None,None)): 
        st.returnValueList0.pop(0)#fixed that offset here
        for i in range(len(st.returnValueList0)):
            for j in range(i+1,len(st.returnValueList0)): 
                st.returnValueList0[i]+=st.returnValueList0[j]*(constant)**(j-i)
            st.sampleTrajectory0.append((st.stateList0[i],st.action0[i],st.returnValueList0[i]))
            x,y=st.action0[i][0],st.action0[i][1]
            val=st.Q_table0[tuple(st.stateList0[i])][x*3+y]
            st.Q_table0[tuple(st.stateList0[i])][x*3+y]=val+(st.returnValueList0[i]-val)*learningRate
                
        #print(f"Agent 1:{st.Q_table0}")
        #saveEpisodeData("episodeDataCompiledAI0.csv",0) 
        if st.count==st.totalSimulations:
            saveQTable(st.Q_table0,"Agent1Qtable.json")   
    return selection

def clearBuffer():
    st.sampleTrajectory1.clear()
    st.returnValueList1.clear()
    st.stateList1.clear()
    st.action1.clear()
    st.sampleTrajectory0.clear()
    st.returnValueList0.clear()
    st.stateList0.clear()
    st.action0.clear()
    

def saveEpisodeData(filename,type):
    mode = 'w' if st.count == 0 else 'a'
    with open(filename,mode=mode,newline='') as file:
        writer = csv.writer(file)
        if  st.count==0:
            writer.writerow(['State','Action','Return'])
        if type==0:    
            for entry in st.sampleTrajectory0:
                writer.writerow(entry)
            writer.writerow([st.count,'-','-'])
        if type==1:
            for entry in st.sampleTrajectory1:
                writer.writerow(entry)
            writer.writerow([st.count,'-','-'])

def saveQTable(table,filename):
    trasnformedData={str(key):value for key,value in table.items()}
    with open(filename,'w') as file:
        json.dump(trasnformedData,file,indent=4)
    print(f"Q-Table saved to {filename}")
def decodeIndex(index):
    i=int(index/3)
    j=int(index%3)
    return i,j

def encodeIndex(x,y):
    return x*3+y
#now we do the picking portion and make a Q-value list too




#State: state of the tictactoe board
#Action: pick one free spot based on the output free spot

#Policy
#Return
#Q-value

