import random as rnd
import state as st
import main
import csv

def Training1(valid): #Always 'O'
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
    if(al):selectionEn = rnd.choice(al)
    else: selectionEn=[10,10]
    
    st.returnValueList1.append(main.gamelogic(None,st.playerType[1],None))
   
    if(valid):
        st.stateList1.append(list(st.SequentialCoordinate1))
        st.action1.append(selectionEn)
    constant=0.8
    if( main.gamelogic(True,None,None)): 
        st.returnValueList1.pop(0)
        for i in range(len(st.returnValueList1)):
            for j in range(i+1,len(st.returnValueList1)): 
                st.returnValueList1[i]+=st.returnValueList1[j]*(constant)**(j-i)
            st.sampleTrajectory1.append((st.stateList1[i],st.action1[i],st.returnValueList1[i]))
        saveEpisodeData("episodeDataCompiledAI1.csv",1)    
  
    selection=decodeStateData(selectionEn[0],selectionEn[1],player=True)
    return selection

def Training0(valid):#Always 'X'
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
    
    #selection
    if(al):selectionEn = rnd.choice(al)
    else: selectionEn=[10,10]
    
    st.returnValueList0.append(main.gamelogic(None,st.playerType[0],None)) #its recording return values with offset of 1
    if(valid):
        st.stateList0.append(list(st.SequentialCoordinate0))
        st.action0.append(selectionEn)
    constant=0.8
    if( main.gamelogic(True,None,None)): 
        st.returnValueList0.pop(0)#fixed that offset here
        for i in range(len(st.returnValueList0)):
            for j in range(i+1,len(st.returnValueList0)): 
                st.returnValueList0[i]+=st.returnValueList0[j]*(constant)**(j-i)
            st.sampleTrajectory0.append((st.stateList0[i],st.action0[i],st.returnValueList0[i]))
        saveEpisodeData("episodeDataCompiledAI0.csv",0)    
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


#now we do the picking portion and make a Q-value list too




#State: state of the tictactoe board
#Action: pick one free spot based on the output free spot

#Policy
#Return
#Q-value

