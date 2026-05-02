import random as rnd
import state as st
import main
import csv
import math
import json

decayRate=0.001
epMin=0.1
epMax=1.0
epsilon=epMin+(epMax-epMin)*math.exp(-1*st.count*decayRate)

def Training1(valid): #Always 'O'
    global epsilon
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
    al=actionList1.copy()
    for i,(x,y) in enumerate(al):
        al[i]=encodeStateData(x,y,player=True)
    
    #selection
    
    
    st.returnValueList1.append(main.gamelogic(None,st.playerType[1],None))
    if(valid):
        st.stateList1.append(list(st.SequentialCoordinate1))
        if(al):
            if rnd.random()<epsilon:
                selectionEn = rnd.choice(al)#encoded selection
            else:
                stateKey=tuple(st.stateList1[-1])
                qValueList=st.Q_table1[stateKey]
                legalQVals=[(qValueList[encodeIndex(i,j)],[i,j]) for i,j in al]
                selectionEn=decodeIndex(max(legalQVals,key=lambda x:x[0])[1])
        else: selectionEn=[10,10] #default selection, not used at all
        st.action1.append(selectionEn)
    else: selectionEn=[10,10]
    constant=0.8
    learningRate=0.1
    if( main.gamelogic(True,None,None)): 
        st.returnValueList1.pop(0)
        for i in range(len(st.stateList1)):
            for j in range(i+1,len(st.returnValueList1)): 
                st.returnValueList1[i]+=st.returnValueList1[j]*(constant)**(j-i)
            st.sampleTrajectory1.append((st.stateList1[i],st.action1[i],st.returnValueList1[i]))
            if tuple(st.stateList1[i]) not in st.Q_table1:
                st.Q_table1[tuple(st.stateList1[i])]=[0]*9
            x,y=decodeStateData(st.action1[i][0],st.action1[i][1],player=True)
            val=st.Q_table1[tuple(st.stateList1[i])][x*3+y]
            st.Q_table1[tuple(st.stateList1[i])][x*3+y]=val+(st.returnValueList1[i]-val)*learningRate
                
        #print(f"Agent 2:{st.Q_table1}")
        #saveEpisodeData("episodeDataCompiledAI1.csv",1)    
        if st.count==st.totalSimulations:
            saveQTable(st.Q_table1,"Agent2Qtable.json")
    selection=decodeStateData(selectionEn[0],selectionEn[1],player=True)
    return selection

def Training0(valid):#Always 'X'
    global epsilon
    State1=st.P0Coordinate#[(1,1),(2,2)]
    State2=st.P1Coordinate#[(2,0),(0,0)]

    allCordinates=st.worldPositions#[(0,0),(1,1),(2,2),(2,0),(1,2)]
    tempState=State1+State2
    actionList0 = allCordinates.copy()
    for cord in tempState:
        if cord in actionList0:
            actionList0.remove(cord)

    
            
    #done the below to denote self and opponent; basically encoding
    #similarly action will be:
    al=actionList0.copy()
    for i,(x,y) in enumerate(al):
        al[i]=encodeStateData(x,y,player=True) #always 1 for now
    
    
    
    st.returnValueList0.append(main.gamelogic(None,st.playerType[0],None)) #its recording return values with offset of 1
    if(valid):
        st.stateList0.append(list(st.SequentialCoordinate0))
        if(al):
            if rnd.random()<epsilon:
                selectionEn = rnd.choice(al)#encoded selection
            else:
                stateKey=tuple(st.stateList0[-1])
                qValueList=st.Q_table0[stateKey]
                legalQVals=[(qValueList[encodeIndex(i,j)],[i,j]) for i,j in al]
                selectionEn=decodeIndex(max(legalQVals,key=lambda x:x[0])[1])
        else: selectionEn=[10,10] #default selection, not used at all
        st.action0.append(selectionEn)
    else: selectionEn=[10,10]
    constant=0.9
    learningRate=0.05
    if( main.gamelogic(True,None,None)): 
        st.returnValueList0.pop(0)#fixed that offset here
        for i in range(len(st.returnValueList0)):
            for j in range(i+1,len(st.returnValueList0)): 
                st.returnValueList0[i]+=st.returnValueList0[j]*(constant)**(j-i)
            st.sampleTrajectory0.append((st.stateList0[i],st.action0[i],st.returnValueList0[i]))
            if tuple(st.stateList0[i]) not in st.Q_table0:
                st.Q_table0[tuple(st.stateList0[i])]=[0]*9
            x,y=decodeStateData(st.action0[i][0],st.action0[i][1],player=True)
            val=st.Q_table0[tuple(st.stateList0[i])][x*3+y]
            st.Q_table0[tuple(st.stateList0[i])][x*3+y]=val+(st.returnValueList0[i]-val)*learningRate
                
        #print(f"Agent 1:{st.Q_table0}")
        #saveEpisodeData("episodeDataCompiledAI0.csv",0) 
        if st.count==st.totalSimulations:
            saveQTable(st.Q_table0,"Agent1Qtable.json")   
    selection=decodeStateData(selectionEn[0],selectionEn[1],player=True)
    return selection


def encodeStateData(i,j,player):
    if player == False: return i+20,j+20
    elif player== True: return i+10,j+10
    else: return i,j
def decodeStateData(i,j,player):
    if player == False: return i-20,j-20
    elif player== True: return i-10,j-10
    else: return i,j
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
    i+=10
    j+=10
    return i,j

def encodeIndex(x,y):
    x-=10
    y-=10
    return x*3+y
#now we do the picking portion and make a Q-value list too




#State: state of the tictactoe board
#Action: pick one free spot based on the output free spot

#Policy
#Return
#Q-value

