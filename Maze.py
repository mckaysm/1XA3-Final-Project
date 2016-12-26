#Maze.py
#Sean McKay

#Green is the start, red is the end, and yellow is the key
#Blue squares are the path to the key, red squares are the path to the finish


from random import *
from graphics import *

class Mystack:
    def __init__(self):
        self.stack = []
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        if self.stack != []:
            return self.stack.pop()
    def isEmpty(self):
        return len(self.stack) == 0
    def size(self):
        return len(self.stack)
    
class Cell:
    def __init__(self):
        #Walls
        self.N = True
        self.S = True
        self.E = True
        self.W = True
        self.V = False
        #First, last, and key
        self.first = False
        self.last = False
        self.key = False

    def hasAllWalls(self):
        return self.N and self.S and self.E and self.W


class Maze:
    def __init__(self, n):
        '''Makes the maze'''
        #The grid
        self.grid = [[Cell() for i in range(n)] for j in range(n)]
        self.cellStack = Mystack()
        self.visited = []
        self.path = []
        self.endPath = []
        self.keyPath = []
        #Current x and y coordinates
        X = 0
        Y = 0
        #Starting x and y coordinates
        self.startX = 0
        self.startY = 0
        #Ending x and y coordinates
        self.endX = 0
        self.endY = 0
        #x and y coordinate of the key
        self.keyX = 0
        self.keyY = 0
        
        #Size of the grid
        self.size = n
        
        self.visitedCells = 0
        self.totalCells = n ** 2
        self.cellSize = 800 / n

        while self.visitedCells <= self.totalCells:
            #Current cell
            cell = self.grid[X][Y]
            #Generate a list of valid neighbours
            neighbourlist = self.neighbours(n, X, Y)
            if neighbourlist != []:

                #Mark current cell as visited
                cell.V = 'True'
                
                #Push the current cell to the stack 
                self.cellStack.push((X, Y))
                
                #Randomly pick a neighbour from the list of neighbours
                neighbour = choice(neighbourlist)
                cellneighbour = self.grid[neighbour[1]][neighbour[2]]
                
                #Tear down walls of the current cell and the neighbour you move to
                if neighbour[0] == 'N':
                    cell.N = False
                    cellneighbour.S = False
                elif neighbour[0] == 'S':
                    cell.S = False
                    cellneighbour.N = False
                elif neighbour[0] == 'E':
                    cell.E = False
                    cellneighbour.W = False
                elif neighbour[0] == 'W':
                    cell.W = False
                    cellneighbour.E = False
                    
                #Set the current position equal to the next cell
                X = neighbour[1]
                Y = neighbour[2]
                
                #Increase visited cells by 1
                self.visitedCells += 1
                
            else:
                if self.cellStack.isEmpty():
                    break
                else:
                    #Pop the last cell from the stack and set the current X and Y to that coordinate
                    lastcell = self.cellStack.stack.pop()
                    X = lastcell[0]
                    Y = lastcell[1]
                    
        #Randomly pick a cell to be the start and end and key
        self.startX = randrange(0, n)
        self.startY = randrange(0, n)
        
        self.endX = randrange(0,n)
        self.endY = randrange(0,n)

        self.keyX = randrange(0, n)
        self.keyY = randrange(0, n)
        #make sure start, end, and key don't have overlapping coordinates
        if (self.endX, self.endY) in ((self.startX, self.startY), (self.keyX, self.keyY)) or (self.startX, self.startY) == (self.keyX, self.keyY):
            while (self.endX, self.endY) in ((self.startX, self.startY), (self.keyX, self.keyY)) or (self.startX, self.startY) == (self.keyX, self.keyY):
                self.endX = randrange(0,n)
                self.endY = randrange(0,n)
                self.endX = randrange(0,n)
                self.endY = randrange(0,n)

        #Set booleans for first, last, and key
        self.grid[self.startX][self.startY].first = True
        self.grid[self.endX][self.endY].last = True
        self.grid[self.keyX][self.keyY].key = True
        

    def draw(self, win):
        '''Draws the walls, start, end, key, and paths'''
        for x in range(self.size):
            for y in range(self.size):
                cell = self.grid[x][y]
                s = self.cellSize
                #Draw all the walls
                if cell.N:
                    wall = Line(Point(x * s + 5, y * s + s + 5), Point(x * s + s + 5, y * s + s + 5))
                    wall.setFill('Black')
                    wall.draw(win)
                if cell.S:
                    wall = Line(Point(x * s + 5, y * s + 5), Point(x * s + s + 5, y * s + 5))
                    wall.setFill('Black')
                    wall.draw(win)
                if cell.E:
                    wall = Line(Point(x * s + s + 5, y * s + s + 5), Point(x * s + s + 5, y * s + 5))
                    wall.setFill('Black')
                    wall.draw(win)
                if cell.W:
                    wall = Line(Point(x * s + 5, y * s + s + 5), Point(x * s + 5, y * s + 5))
                    wall.setFill('Black')
                    wall.draw(win)
                #Draw the path from start to key in blue, and key to finish in yellow
                if (x, y) in self.keyPath or (x, y) in self.endPath:
                    square = Rectangle(Point(x * s + s + 5 - s / 5, y * s + s + 5 - s / 5), Point(x * s + 5 + s / 5, y * s + 5 + s / 5))
                    if (x,y) in self.keyPath:
                        square = Rectangle(Point(x * s + s + 5 - s / 5, y * s + s + 5 - s / 5), Point(x * s + 5 + s / 5, y * s + 5 + s / 5))
                        square.setFill('Blue')
                        square.draw(win)
                    if (x,y) in self.endPath:
                        square = Rectangle(Point(x * s + s + 5 - s / 3, y * s + s + 5 - s / 3), Point(x * s + 5 + s / 3, y * s + 5 + s / 3))
                        square.setFill('Brown')
                        square.draw(win)
                #Draw the start, end and key
                if cell.last or cell.first or cell.key:
                    square = Rectangle(Point(x * s + s + 5 - s / 10, y * s + s + 5 - s / 10), Point(x * s + 5 + s / 10, y * s + 5 + s / 10))
                    if cell.first:
                        square.setFill('Green')
                    elif cell.last:
                        square.setFill('Red')
                    else:
                        square.setFill('Yellow')
                    square.draw(win)

                    
                        
                    

    def explore(self, x, y):
        '''Searches all paths by recursively calling the function
           with different coordinates until it finds the end coordinate.
           from there the path to the end coordinate is passed up the tree
           and stored in a list'''
        if (x, y) == (self.endX, self.endY):
            self.path.append((x, y))
            return True
        if ((x, y) in self.visited):
            return False
        self.visited.append((x, y))
        if (x - 1 >= 0) and not self.grid[x][y].W:
            if self.explore(x - 1, y):
                self.path.append((x, y))
                return True
        if (x + 1 < self.size) and not self.grid[x][y].E:
            if self.explore(x + 1, y):
                self.path.append((x, y))
                return True
        if (y + 1 < self.size) and not self.grid[x][y].N:
            if self.explore(x, y + 1):
                self.path.append((x, y))
                return True
        if (y - 1 >= 0) and not self.grid[x][y].S:
            if self.explore(x, y - 1):
                self.path.append((x, y))
                return True
            

    
    def neighbours(self, n, x, y):
        '''Returns a list of valid neighbours'''
        nb = []
        #North
        if y + 1 < n  and self.grid[x][y + 1].hasAllWalls():
            nb.append(['N', x, y + 1])
        #South
        if y - 1 >= 0 and self.grid[x][y - 1].hasAllWalls():
            nb.append(['S', x, y - 1])
        #East
        if x + 1 < n and self.grid[x + 1][y].hasAllWalls():
            nb.append(['E', x + 1, y])
        #West
        if x - 1 >= 0 and self.grid[x - 1][y].hasAllWalls():
            nb.append(['W', x - 1, y])
        return nb



def Main():
    #Make the maze
    'CHANGE SIZE OF MAZE HERE'
    m = Maze(5)
    'CHANGE SIZE OF MAZE HERE'
    #Flip end and key coordinates
    m.endX, m.endY, m.keyX, m.keyY = m.keyX, m.keyY, m.endX, m.endY
    #Find the path from the start to the key
    m.explore(m.startX, m.startY)
    #Assign that path to the keypath
    m.keyPath = m.path
    m.keyPath.reverse()
    #Clear the path and visited cells
    m.path = []
    m.visited = []
    #Flip end and key coordinates again
    m.endX, m.endY, m.keyX, m.keyY = m.keyX, m.keyY, m.endX, m.endY
    #Find the path from the key to the end
    m.explore(m.keyX, m.keyY)
    #Assign that path to the keypath
    m.endPath = m.path
    m.endPath.reverse()
    #Draw the maze
    win = GraphWin("Maze", 810, 810)
    m.draw(win)
    #Print the trace
    print('Path from the start to the key: ', end = '')
    for (x, y) in m.keyPath:
        print ((x + 1, y + 1),'', end = '')
    print()
    print('Path from the key to the end: ', end = '')
    for (x, y) in m.endPath:
        print ((x + 1, y + 1),'', end = '')
    
Main()
            
            


        
                
        
