import random as rnd
import state as st
import main
import csv
import os

def Training1(valid):
    State1=st.P2Coordinate#[(1,1),(2,2)]
    State2=st.P1Coordinate#[(2,0),(0,0)]

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
        al[i]=encodeStateData(x,y,st.playerType[1])
    #print(al)
    
    #selection
    if(al):selectionEn = rnd.choice(al)
    else: selectionEn=[10,10]
    
    #print(st.stateList)
    #print(st.SequentialCoordinate)
   
    if(valid):
        st.stateList1.append(list(st.SequentialCoordinate1))
        st.returnValueList1.append(main.gamelogic(None,st.playerType[1],None))
        st.action1.append(selectionEn)
        #print(st.stateList)
    #print(main.gamelogic(True,None))
    learningRate=0.8
    if( main.gamelogic(True,None,None)): 
        
        for i in range(len(st.returnValueList1)):
            for j in range(i+1,len(st.returnValueList1)): 
                st.returnValueList1[i]+=st.returnValueList1[j]*(learningRate)**(j-i)
            st.sampleTrajectory1.append((st.stateList1[i],st.action1[i],st.returnValueList1[i]))
        #saveEpisodeData("episodeDataCompiled")    
        st.count+=1
        print(f"Number 1:{st.sampleTrajectory1}")
  
    selection=decodeStateData(selectionEn[0],selectionEn[1],st.playerType[1])
    return selection

def Training0(valid):
    State1=st.P1Coordinate#[(1,1),(2,2)]
    State2=st.P2Coordinate#[(2,0),(0,0)]

    allCordinates=st.worldPositions#[(0,0),(1,1),(2,2),(2,0),(1,2)]
    tempState=State1+State2
    actionList2 = allCordinates.copy()
    for cord in tempState:
        if cord in actionList2:
            actionList2.remove(cord)

    
            
    #done the below to denote self and opponent; basically encoding
    #similarly action will be:
    al=actionList2.copy()
    for i,(x,y) in enumerate(al):
        al[i]=encodeStateData(x,y,st.playerType[1]) #always 1 for now
    #print(al)
    
    #selection
    if(al):selectionEn = rnd.choice(al)
    else: selectionEn=[10,10]
    
    #print(st.stateList)
    #print(st.SequentialCoordinate)
   
    if(valid):
        st.stateList0.append(list(st.SequentialCoordinate0))
        st.returnValueList0.append(main.gamelogic(None,st.playerType[0],None))
        st.action0.append(selectionEn)
        #print(st.stateList)
    #print(main.gamelogic(True,None))
    learningRate=0.8
    if( main.gamelogic(True,None,None)): 
        
        for i in range(len(st.returnValueList0)):
            for j in range(i+1,len(st.returnValueList0)): 
                st.returnValueList0[i]+=st.returnValueList0[j]*(learningRate)**(j-i)
            st.sampleTrajectory0.append((st.stateList0[i],st.action0[i],st.returnValueList0[i]))
        #saveEpisodeData("episodeDataCompiled")    
        st.count+=1
        print(f"Number 2:{st.sampleTrajectory0}")
        print(st.count)
    selection=decodeStateData(selectionEn[0],selectionEn[1],st.playerType[1])
    return selection


def encodeStateData(i,j,k):
    if k == st.playerType[0]: return i+20,j+20
    elif k== st.playerType[1]: return i+10,j+10
    else: return i,j
def decodeStateData(i,j,k):
    if k == st.playerType[0]: return i-20,j-20
    elif k== st.playerType[1]: return i-10,j-10
    else: return i,j
'''
def saveEpisodeData(filename):
    file_exists=os.path.isfile(filename)
    with open(filename,mode='a',newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['State','Action','Return'])
            
        for entry in st.sampleTrajectory:
            writer.writerow(entry)
        writer.writerow([st.count,'-','-'])
'''
def clearBuffer():
    st.sampleTrajectory1.clear()
    st.returnValueList1.clear()
    st.stateList1.clear()
    st.action1.clear()
    st.sampleTrajectory0.clear()
    st.returnValueList0.clear()
    st.stateList0.clear()
    st.action0.clear()
#now we do the picking portion and make a Q-value list too




#State: state of the tictactoe board
#Action: pick one free spot based on the output free spot

#Policy
#Return
#Q-value

