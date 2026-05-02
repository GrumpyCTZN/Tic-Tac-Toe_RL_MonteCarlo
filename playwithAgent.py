import tkinter as tk
from tkinter import ttk
import json
import time
import random
state=["Player","AI"]
currState=state[0]
winnerState=state[0]
PlayerCoordinate=[]
AICoordinate=[]
delay=1
worldPositions=[]
worldState=[0]*9
def game():
    global allButtons
    root =tk.Tk()
    root.title("TicTacToe Game")
    root.geometry("800x600")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    frame=ttk.Frame(root,padding="10")
    frame.grid(row=0,column=0)
    
    label= ttk.Label(frame,text="Tic Tac Toe",font=("Arial",20))
    label.grid(row=0,column=1,pady=10)
    allButtons=[]*9
    slabel=ttk.Label(frame,text=f"{currState}'s Turn",font=("Arial",20))
    slabel.grid(row=4,column=1,pady=10)
    style=ttk.Style()
    style.configure("Special.TButton",padding=(0,50),font=("Arial",20))
    
    for i in range(3):
        for j in range(3):
            button = ttk.Button(frame,text="", width=10,style="Special.TButton")
            button.config(command = lambda btn=button,i=i,j=j:handlePress(btn,i,j,slabel,root))
            button.grid(row=i+1,column=j,padx=10,pady=10)
            allButtons.append(button) 
            worldPositions.append([i,j])
    handleOrder(root,slabel)
    root.mainloop()

def handleSwitching():
    global currState
    global state
    if(currState==state[0]): currState=state[1]
    elif(currState==state[1]): currState=state[0]
    else: currState=""
    return currState

def handleOrder(root,slabel):
    if(winnerState!=currState):handleSwitching()
    slabel.config(text=f"{currState}'s Turn")
    #time.sleep(delay)
    resetBoard(root)
    randomFunction(root)
    
def randomFunction(root):
    if(currState==state[0]):
        return
    elif(currState==state[1]):
        handleAI(root)
    else: return

def handleAI(root):
    
    state=tuple(worldState)
    
    validIndices = [i for i, val in enumerate(worldState) if val == 0]
    
    if not validIndices:
        return
    
    if state not in Q_table:
        maxIndex=random.choice(validIndices)
    else:
        epsilon=0.05
        listOfMoves=Q_table[state]
        if random.random()<epsilon:
            maxIndex=random.choice(listOfMoves)
        else:
            maskedMoves = [listOfMoves[i] if i in validIndices else -float('inf') for i in range(9)]
            maxVal=max(maskedMoves)
            maxIndex=listOfMoves.index(maxVal)
    #time.sleep(delay)   
    root.after(100,lambda: allButtons[maxIndex].invoke())
    
def handlePress (button,i,j,slabel,root):
    global state
    global delay
    global currState
    if(currState==state[0]):
        button.config(text='X')
        button.config(state="disabled")
        PlayerCoordinate.append([i,j])
        worldState[encodeIndex(i,j)]=2
        root.update()
        
    if(currState==state[1]):
        button.config(text='O')
        button.config(state="disabled")
        worldState[encodeIndex(i,j)]=1
        AICoordinate.append([i,j])
        time.sleep(delay)
        root.update()
           
        
    
    noMoreMoves=gamelogic(slabel)
    if not noMoreMoves:
        currState=handleSwitching()
        slabel.config(text=f"{currState}'s turn")
        root.update() 
        randomFunction(root)
    else:
        root.update()
        time.sleep(delay) 
        handleOrder(root,slabel)
    

def endgame(message,slabel):
    global allButtons
    slabel.config(text=message)
    for button in allButtons:
        button.config(state="disabled")

def gamelogic(slabel):
    Pcount=[0]*8
    AIcount = [0]*8
    global state
    global winnerState
    for r,c in PlayerCoordinate:
        if(r==c):
            Pcount[0]+=1
        if(r+c==2):
            Pcount[1]+=1
        for i in range(3):
            if(r==i): Pcount[i+2]+=1
        for i in range(3):
            if(c==i): Pcount[i+5]+=1
    for r,c in AICoordinate:
        if(r==c):
            AIcount[0]+=1
        if(r+c==2):
            AIcount[1]+=1
        for i in range(3):
            if(r==i): AIcount[i+2]+=1
        for i in range(3):
            if(c==i): AIcount[i+5]+=1
    if any(score == 3 for score in Pcount):
        endgame(f"{state[0]} Won",slabel)
        winnerState=state[0]
        return True

    if any(score == 3 for score in AIcount):
        endgame(f"{state[1]} Won",slabel)
        winnerState=state[1]
        return True

    if(len(PlayerCoordinate)+len(AICoordinate)==9):
        endgame("Draw",slabel)
        return True
        
    return False     
def loadQTable(filename):
    try:
        with open(filename,'r') as file:
            strQtable=json.load(file)
            
        qTable={eval(k): v for k,v in strQtable.items()}
        
        print(f"Sucessfully loaded{len(qTable)} states from {filename}")
        return qTable
    except FileNotFoundError:
        print(f"File {filename} not found. Starting withh an empty Q-table.")
        return {}
    except Exception as e:
        print(f"Error loading Q-Table: {e}")
        return {}
    
Q_table=loadQTable("Qtable.json")
def decodeIndex(index):
    i=int(index/3)
    j=int(index%3)
    return i,j

def encodeIndex(x,y):
    return x*3+y      


def resetBoard(root):
    global PlayerCoordinate
    global AICoordinate
    global worldState
    for button in allButtons:
        button.config(state="normal",text="")
        
    PlayerCoordinate.clear()
    AICoordinate.clear()
    worldState=[0]*9

    return 
if __name__=="__main__":
    game()