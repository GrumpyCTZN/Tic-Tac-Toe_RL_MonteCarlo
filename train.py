import random as rnd
import state as st
def Training1():
    State1=st.P2Coordinate#[(1,1),(2,2)]
    State2=st.P1Coordinate#[(2,0),(0,0)]
    #print(State2)

    allCordinates=st.worldPositions#[(0,0),(1,1),(2,2),(2,0),(1,2)]
    tempState=State1+State2
    print(tempState)
    actionList = allCordinates.copy()
    #print(actionList)
    for cord in tempState:
        if cord in actionList:
            actionList.remove(cord)
    #print(tempState)
    #print(actionList)
            
    #done the below to denote self and opponent; basically encoding
    s1=State1.copy()
    s2=State2.copy()
    for i,(x,y) in enumerate(s1):
        x+=10
        y+=10
        s1[i]=[x,y]
    for i,(x,y) in enumerate(s2):
        x+=20
        y+=20
        s2[i]=[x,y]
    state=s1+s2
    #similarly action will be:
    for i,(x,y) in enumerate(actionList):
        x+=10
        y+=10
        actionList[i]=[x,y]
    #print(actionList)
    selection = rnd.choice(actionList)
    selection[0]-=10
    selection[1]-=10
    #print(selection)
    return selection

#now we do the picking portion and make a Q-value list too




#State: state of the tictactoe board
#Action: pick one free spot based on the output free spot

#Policy
#Return
#Q-value

