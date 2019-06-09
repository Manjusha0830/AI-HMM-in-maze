import sys
import random
import numpy as np
from math import  log

from decimal import Decimal
maze = [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,0,0,0,0,1,1,1],
        [1,1,1,1,0,1,1,0,1,1,1],
        [1,1,1,0,0,1,1,0,1,1,1],
        [1,1,1,1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1]
    ]




moves =['N','N','N','E','N']
senses =['-,-,-,-','-,-,-,-','-,-,o,-','-,-,-,-','-,-,o,o','-,-,o,-']


rowLen = len(maze)
colLen= len(maze[0])
sensesLen =len(senses)
movesLen =len(moves)

def random_free_place():
    x=-1
    y=-1
    while isObstacle(x,y) is False:
        x= random.uniform(0,rowLen)
        y= random.uniform(0,colLen)
    return (x,y)

def isObstacle(x,y):
    if x<0 or y<0 or x>=rowLen or y>=colLen or maze[x][y]==0:
        return True
    else:
        return False

    

#zDict =dict() #this will keep count of cells with different combination of W,N,E,S
mazeTransProb = np.zeros((sensesLen,rowLen,colLen))# stores prob that current square St is x,y after t moves
mazeCondEProb = np.zeros((sensesLen,rowLen,colLen))# stores prob of that Zt is Senses[i] given current square St is x,y
backwardProb = np.zeros((sensesLen,rowLen,colLen))
smoothingProb = np.zeros((sensesLen,rowLen,colLen))
entropyProb = np.zeros((sensesLen,rowLen,colLen))


    #(x,y) = random_free_place() this is required if we want a simulation from random place
def init():
    freeCells = 0
    total=0
    for row in range(0,rowLen):
        for col in range(0,colLen):
            if isObstacle(row,col) is False:#we will never be in obs cell
                freeCells = freeCells+1
    if(freeCells>0):
        for row in range(0,rowLen):
            for col in range(0,colLen):
                if isObstacle(row,col):#we will never be in obs cell
                    prob=0
                else:
                    prob = float(1.00)/float(freeCells)
                mazeTransProb[0][row][col]= prob
                total = total+prob
    #print(total)
    #print(freeCells)
    print('###############Initial Probablity Prior belief uniform############### ')
    printMatrix(mazeTransProb[0])#initial belief assuming uniform I can be in any of cell
    calcCondEProb(0) #Calc Conditional Probablity given first sense is senses[0]
    print('############### Posterior Probablity based on seeing first sense '+ senses[0]+ ' ############### ')
    printMatrix(mazeCondEProb[0])#initial belief assuming uniform I can be in any of cell
    
    
#
def probMove(dir, x1,y1,x2,y2):#prob of move from x1,y1 to x2,y2
    if isObstacle(x1,y1) or isObstacle(x2,y2):# you cannot move from or to an obstacle
        return 0
    if abs(x1-x2) + abs(y1-y2)>1:# you cannot move more than one move at a time or move diagnoally
        return 0
    if(dir=='N'):
        if abs(x2-x1)==1 and y1==y2:#move east or west
            return 0.1
        elif x2==x1 and y1-y2==1:#moving north
            return 0.8
        else:#move south or other direction
            return 0

    elif(dir=='E'):
        if abs(y2-y1)==1 and x1==x2:#move north or south
            return 0.1
        elif y2==y1 and x2-x1==1:#moving east
            return 0.8
        else:#move west or other direction
            return 0
    
    elif(dir=='W'):
        if abs(y2-y1)==1 and x1==x2:#move north or south
            return 0.1
        elif y2==y1 and x1-x2==1:#moving west
            return 0.8
        else:#move east or other direction
            return 0
    
    if(dir=='S'):
        if abs(x2-x1)==1 and y1==y2:#move east or west
            return 0.1
        elif x2==x1 and y2-y1==1:#moving south
            return 0.8
        else:#move north or other direction
            return 0

#
def calcCondEProb(s):
    sense = senses[s].split(',')
    total =0.0    
    for row in range(0,rowLen):
        for col in range(0,colLen):

            prob = mazeTransProb[s][row][col] #prob that I can be at row,col based on prev moves
            #west
            if isObstacle(row,col-1) and sense[0]=='-':#could not detect obstacle
                prob = prob*0.1 
            elif isObstacle(row,col-1) and sense[0]=='o':#could detect obstacle
                prob = prob*0.9 
            elif isObstacle(row,col-1) is False and sense[0]=='-':#could detect it is free
                prob = prob*0.95 
            elif isObstacle(row,col-1) is False and sense[0]=='o':#mistook free square as obstacle
                prob = prob*0.05 
            #north
            if isObstacle(row-1,col) and sense[1]=='-':#could not detect obstacle
                prob = prob*0.1 
            elif isObstacle(row-1,col) and sense[1]=='o':#could detect obstacle
                prob = prob*0.9 
            elif isObstacle(row-1,col) is False and sense[1]=='-':#could detect it is free
                prob = prob*0.95 
            elif isObstacle(row-1,col) is False and sense[1]=='o':#mistook free square as obstacle
                prob = prob*0.05 
            #east
            if isObstacle(row,col+1) and sense[2]=='-':#could not detect obstacle
                prob = prob*0.1 
            elif isObstacle(row,col+1) and sense[2]=='o':#could detect obstacle
                prob = prob*0.9 
            elif isObstacle(row,col+1) is False and sense[2]=='-':#could detect it is free
                prob = prob*0.95 
            elif isObstacle(row,col+1) is False and sense[2]=='o':#mistook free square as obstacle
                prob = prob*0.05 
            #south
            if isObstacle(row+1,col) and sense[3]=='-':#could not detect obstacle
                prob = prob*0.1 
            elif isObstacle(row+1,col) and sense[3]=='o':#could detect obstacle
                prob = prob*0.9 
            elif isObstacle(row+1,col) is False and sense[3]=='-':#could detect it is free
                prob = prob*0.95 
            elif isObstacle(row+1,col) is False and sense[3]=='o':#mistook free square as obstacle
                prob = prob*0.05 

            mazeCondEProb[s][row][col] = prob
            total = total+prob
    
    for row in range(0,rowLen):
        for col in range(0,colLen):
            mazeCondEProb[s][row][col] = mazeCondEProb[s][row][col]/total #ensure total sum of all prob is 1


#
def calcTransProb(m):
    total=0
    for x2 in range(0,rowLen):
        for y2 in range(0,colLen):
            prob = 0
            for x1 in range(0,rowLen):#instead of calculating for all positions we may just do for (x2-1,x2+1)
                for y1 in range(0,colLen):#instead of calculating for all positions we may just do for (y2-1,2+1)
                    prob = prob+(mazeCondEProb[m-1][x1][y1]*probMove(moves[m-1],x1,y1,x2,y2))
            mazeTransProb[m][x2][y2] = prob
            total = total+prob
    #print(total)
    for  row in range(0,rowLen):
        for col in range(0,colLen):
            mazeTransProb[m][row][col] = mazeTransProb[m][row][col]/total
    
def calcProbMatrices():
    
    for t in range(1,sensesLen):
        calcTransProb(t) #calc Tans Prob after mth move
        print('##############TRANSITION PROBABABILITY at t'+str(t)+' for move '+moves[t-1] )
        printMatrix(mazeTransProb[t])            
        calcCondEProb(t) #sense for sth time          
        print('##############EVIDENCE CONDITIONAL PROBABABILITY at'+str(t)+'Sense'+senses[t] )
        printMatrix(mazeCondEProb[t])
    for t in range(movesLen,-1,-1):
        calcBackwardProb(t)
        #print('##############Backwawrd Prob at '+str(t) )
        #printMatrix(backwardProb[t])
        calcSmoothing(t)
        print('##############Smoothing Prob at Move'+str(t) )
        printMatrix(smoothingProb[t])
    for t in range(0, sensesLen):    
        print('##############entrpoy Prob at '+str(t) )
        calcEntropy(t)
        
        
def calcEntropy(t):
    entropyval = 0.0
    p = 0.0
    #for t in range(0, sensesLen):
    for row in range(0,rowLen):
        for col in range(0,colLen):
            entropyProb[t][row][col] = mazeTransProb[t][row][col] - smoothingProb[t][row][col]
    
    for row in range(0,rowLen):
        for col in range(0,colLen):
            p = entropyProb[t][row][col]
            if(p>sys.float_info.min):
                entropyval = (-p*(log(p,2))) + entropyval
    print('entropy at '+str(t) +'is: ' + str(entropyval))
                
                
                
def printMatrix(array):
    for items in array:
                rowString =''
                for item in items:
                      rowString = rowString + str(round(item*100,2)) + ' ' 

                print(rowString)
                
def calcSmoothing(t):
    total=0.0
    for row in range(0,rowLen):
        for col in range(0,colLen):
            smoothingProb[t][row][col] = backwardProb[t][row][col]*mazeCondEProb[t][row][col]
            total=total+smoothingProb[t][row][col]
    max =0
    maxrow=-1
    maxcol=-1
    for row in range(0,rowLen):
        for col in range(0,colLen):
                smoothingProb[t][row][col] = smoothingProb[t][row][col]/total  
                if(max<smoothingProb[t][row][col]):
                    max= smoothingProb[t][row][col]
                    maxrow= row
                    maxCol= col
    #print('Max smoothing at '+str(t) + ' is '+ str(max*100) + ' at '+str(maxrow)+' ' +str(maxCol) )
                    
def calcBackwardProb(s):
    
    sense = senses[s].split(',')
    total =0.0    
    for x1 in range(0,rowLen):
        for y1 in range(0,colLen):
            cellProb=0
            for row in range(0,rowLen):
                for col in range(0,colLen):
                    prob =probMove(moves[s-1], x1,y1,row,col)
                    if(s==5):
                        prob =prob#multiply by 1
                    else:
                        prob = prob*backwardProb[s+1][row][col]
                    #west
                    if isObstacle(row,col-1) and sense[0]=='-':#could not detect obstacle
                        prob = prob*0.1 
                    elif isObstacle(row,col-1) and sense[0]=='o':#could detect obstacle
                        prob = prob*0.9 
                    elif isObstacle(row,col-1) is False and sense[0]=='-':#could detect it is free
                        prob = prob*0.95 
                    elif isObstacle(row,col-1) is False and sense[0]=='o':#mistook free square as obstacle
                        prob = prob*0.05 
                    #north
                    if isObstacle(row-1,col) and sense[1]=='-':#could not detect obstacle
                        prob = prob*0.1 
                    elif isObstacle(row-1,col) and sense[1]=='o':#could detect obstacle
                        prob = prob*0.9 
                    elif isObstacle(row-1,col) is False and sense[1]=='-':#could detect it is free
                        prob = prob*0.95 
                    elif isObstacle(row-1,col) is False and sense[1]=='o':#mistook free square as obstacle
                        prob = prob*0.05 
                    #east
                    if isObstacle(row,col+1) and sense[2]=='-':#could not detect obstacle
                        prob = prob*0.1 
                    elif isObstacle(row,col+1) and sense[2]=='o':#could detect obstacle
                        prob = prob*0.9 
                    elif isObstacle(row,col+1) is False and sense[2]=='-':#could detect it is free
                        prob = prob*0.95 
                    elif isObstacle(row,col+1) is False and sense[2]=='o':#mistook free square as obstacle
                        prob = prob*0.05 
                    #south
                    if isObstacle(row+1,col) and sense[3]=='-':#could not detect obstacle
                        prob = prob*0.1 
                    elif isObstacle(row+1,col) and sense[3]=='o':#could detect obstacle
                        prob = prob*0.9 
                    elif isObstacle(row+1,col) is False and sense[3]=='-':#could detect it is free
                        prob = prob*0.95 
                    elif isObstacle(row+1,col) is False and sense[3]=='o':#mistook free square as obstacle
                        prob = prob*0.05 
                    
                    cellProb = cellProb+prob
            backwardProb[s][x1][y1] = cellProb    
            total=total+cellProb
    max =0
    maxrow=-1
    maxcol=-1
    for row in range(0,rowLen):
        for col in range(0,colLen):
                backwardProb[s][row][col] = backwardProb[s][row][col]/total     
                if(max<backwardProb[s][row][col]):
                    max= backwardProb[s][row][col]
                    maxrow= row
                    maxCol= col
    #print('Max backward at '+str(s) + ' is '+ str(max*100) + ' at '+str(maxrow)+' ' +str(maxCol) )
    
   
              
     


def main():
    init()
    calcProbMatrices()
        
if __name__ == "__main__":
    main()     
