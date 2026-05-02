#tic tac toe using RL

#define the state
    #just gonna be a 3x3 grid with two sets of values. ([list of coordinates of your symbol already placed], [list of cordinates of oponent symbol already placed])
#define a ctions
    #pick any coordinate other than the ones already in the state

#define return(Gt) :
    #if it suceedes, 0
    #otherwise -1

#Q_value -> which ever state/action pair has the least return, we use q_value+(r_value-q_value)*learning rate


#Run it if the combination is not possible or win condition.

#The win conditions will be as follows.
#There must be a  formula to calculate this rather than having to list out all the possibilies on your own.

#2 diagonal + 6 horizontal/vertical
#for 2 diagonal : all cases simultaneously(x==y || x+y==2(0,1,2 system))
#for 3 horizontal: y=0, y=1, y=2 (all simultaneously)
#for 3 vertical: x=0, x=1, x=2 (all simultaneously)

#need a way to check all the conditions all at once. Maybe check all the squares and see if 3 of any of these exist?
#simultaneous need to check if win is possible.

#training is going to be tough. Best possible for both players having perfect game is a draw. reward system needs to be updated.
# -1 if loss, 0 if draw and 1 if win.
# so here, playerCoordinates and AIcoordinates will be the two things a model will look at for state.
#reward will be given accordingly. we have the code for knowing which state is draw win or loss
# action will firstly be randomly picking an open spot.
# we will refine this picking process with the help of value functions Q.

# we will run two opposing models against one another for training 


import tkinter as tk
from tkinter import ttk
import train as trn
import state as st
import time
state=st.playerType
currState=state[0]
allButtons=[]*9
moveDelay=0
episodeDelay=0
def game():
    global allButtons
    global slabel
    root =tk.Tk()
    root.title("TicTacToe Game")
    root.geometry("800x600")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    frame=ttk.Frame(root,padding="10")
    frame.grid(row=0,column=0)
    
    label= ttk.Label(frame,text="Tic Tac Toe",font=("Arial",20))
    label.grid(row=0,column=1,pady=10)
    slabel=ttk.Label(frame,text=f"{currState}'s Turn",font=("Arial",20))
    slabel.grid(row=4,column=1,pady=10)
    style=ttk.Style()
    style.configure("Special.TButton",padding=(0,50),font=("Arial",20))
    
    for i in range(3):
        for j in range(3):
            button = ttk.Button(frame,text="", width=10,style="Special.TButton")
            button.config(command = lambda btn=button,i=i,j=j:handleFirst(btn,i,j,slabel,root))
            button.grid(row=i+1,column=j,padx=10,pady=10)
            allButtons.append(button) 
            st.worldPositions.append([i,j])
    pressButton(root)
    root.mainloop()
     
def handleSwitching():
    global currState
    global state
    if(currState==state[0]): currState=state[1]
    elif(currState==state[1]): currState=state[0]
    else: currState=""
    return currState

def handleSecond(slabel,root):
    global state
    global currState
    global moveDelay
    #Training 1 -> 
    if(currState==state[1]):
        i,j=trn.Training1(True)
        button=allButtons[i*3+j]
        button.config(text='O')
        button.config(state="disabled")
        st.P1Coordinate.append([i,j])
        st.SequentialCoordinate1.append(trn.encodeStateData(i,j,player=True))
        st.SequentialCoordinate0.append(trn.encodeStateData(i,j,player=False))
        time.sleep(moveDelay)
        
    elif(currState==state[0]):
        i,j=trn.Training0(True)
        button=allButtons[i*3+j]
        button.config(text='X')
        button.config(state="disabled")
        st.P0Coordinate.append([i,j])
        st.SequentialCoordinate1.append(trn.encodeStateData(i,j,player=False))
        st.SequentialCoordinate0.append(trn.encodeStateData(i,j,player=True))
        time.sleep(moveDelay)
    handleSwitching()
    slabel.config(text=f"{currState}'s turn")
    root.update()
    
    
    moreMoves=gamelogic(slabel,None,root)
    if not moreMoves:pressButton(root)  
    else:
        trn.Training0(False)
        trn.Training1(False)
        st.count+=1
        if(st.count%1000 ==-0): print(st.count)
        time.sleep(episodeDelay)
        resetBoard(root)

def handleFirst (button,i,j,slabel,root):
        global state
        global currState
        global episodeDelay
        slabel.config(text=f"{currState}'s turn")
        if(currState==state[0]):
            button.config(text='X')
            button.config(state="disabled")
            st.P0Coordinate.append([i,j])
            st.SequentialCoordinate1.append(trn.encodeStateData(i,j,player=False))
            st.SequentialCoordinate0.append(trn.encodeStateData(i,j,player=True))
        elif(currState==state[1]):
            button.config(text='O')
            button.config(state="disabled")
            st.P1Coordinate.append([i,j])
            st.SequentialCoordinate1.append(trn.encodeStateData(i,j,player=True))
            st.SequentialCoordinate0.append(trn.encodeStateData(i,j,player=False))
            
        handleSwitching()
        slabel.config(text=f"{currState}'s turn")
        root.update()
        moreMoves=gamelogic(slabel,None,root)
        if not moreMoves:handleSecond(slabel,root)
        
        else:
            trn.Training0(False)
            trn.Training1(False)
            st.count+=1
            if(st.count%1000 ==-0): print(st.count)
            time.sleep(episodeDelay)
            resetBoard(root)

def pressButton(root):
    global allButtons
    global currState
    global moveDelay
    if st.count > st.totalSimulations:
        print("Done!")
        return
    if(st.count % 2 == 0):
        currState=state[0]
        i,j=trn.Training0(True)
    else:
        currState=state[1]
        i,j=trn.Training1(True)
    root.after(int(moveDelay*1000), lambda: allButtons[i*3+j].invoke())
    

def endgame(message,slabel,root):
    global allButtons
    slabel.config(text=message)
    for button in allButtons:
        button.config(state="disabled")
    root.update()
    
def gamelogic(slabel,player,root):
    P0count=[0]*8
    P1count=[0]*8
    global state
    for r,c in st.P0Coordinate:
        if(r==c):
            P0count[0]+=1
        if(r+c==2):
            P0count[1]+=1
        for i in range(3):
            if(r==i): P0count[i+2]+=1
        for i in range(3):
            if(c==i): P0count[i+5]+=1
    for r,c in st.P1Coordinate:
        if(r==c):
            P1count[0]+=1
        if(r+c==2):
            P1count[1]+=1
        for i in range(3):
            if(r==i): P1count[i+2]+=1
        for i in range(3):
            if(c==i): P1count[i+5]+=1
    if any(score == 3 for score in P0count):
        if(slabel):
            if(type(slabel)!=bool):
                endgame(f"{state[0]} Won",slabel,root)
            return True
        if player == state[1]:
            return -1
        elif player == state[0]:
            return 1
        

    if any(score == 3 for score in P1count):
        if(slabel):
            if(type(slabel)!=bool):
                endgame(f"{state[1]} Won",slabel,root)
            return True
        if player == state[0]:
            return -1
        elif player == state[1]:
            return 1
        
    if(len(st.P0Coordinate)+len(st.P1Coordinate)==9):
        if(slabel):
            if(type(slabel)!=bool):
                endgame("Draw",slabel,root)
            return True
        if player==state[0] or player==state[1]:
            return 0.5
        
    if slabel: return False  
    else: return -1   
 
def resetBoard(root):
    global allButtons
    global currState
    global slabel
    for button in allButtons:
        button.config(state="normal",text="")
        
    st.P0Coordinate.clear()
    st.P1Coordinate.clear()
    st.SequentialCoordinate1.clear()
    st.SequentialCoordinate0.clear()
    trn.clearBuffer()
    slabel.config(text=f"{currState}'s Turn")
    pressButton(root)
    
        
    return False
 
        
if __name__=="__main__":
    game()